from __future__ import annotations

import dataclasses
import datetime as dt
import random
import warnings
from functools import cached_property
from typing import Any, Dict, List, Literal, Mapping, Optional, Sequence, Union, final
from urllib.parse import urlparse

import grpc
import grpc.experimental
from google.protobuf import timestamp_pb2

from chalk import DataFrame, EnvironmentId
from chalk._gen.chalk.auth.v1.agent_pb2 import CustomClaim
from chalk._gen.chalk.auth.v1.permissions_pb2 import Permission
from chalk._gen.chalk.common.v1 import online_query_pb2
from chalk._gen.chalk.common.v1.online_query_pb2 import GenericSingleQuery
from chalk._gen.chalk.engine.v1 import query_server_pb2
from chalk._gen.chalk.engine.v1.query_server_pb2_grpc import QueryServiceStub
from chalk._gen.chalk.server.v1.auth_pb2_grpc import AuthServiceStub
from chalk._gen.chalk.server.v1.team_pb2 import CreateServiceTokenRequest, CreateServiceTokenResponse
from chalk._gen.chalk.server.v1.team_pb2_grpc import TeamServiceStub
from chalk.client import ChalkAuthException, FeatureReference
from chalk.client.models import BulkOnlineQueryResponse, BulkOnlineQueryResult, OnlineQuery
from chalk.client.serialization.protos import OnlineQueryConverter
from chalk.config.auth_config import load_token
from chalk.features._encoding.json import FeatureEncodingOptions
from chalk.features._encoding.outputs import encode_outputs
from chalk.features.feature_set import is_feature_set_class
from chalk.importer import CHALK_IMPORT_FLAG
from chalk.parsed._proto.utils import datetime_to_proto_timestamp, value_to_proto
from chalk.utils import df_utils
from chalk.utils.df_utils import record_batch_to_arrow_ipc
from chalk.utils.grpc import AuthenticatedChalkClientInterceptor, TokenRefresher, UnauthenticatedChalkClientInterceptor
from chalk.utils.string import removeprefix


@dataclasses.dataclass
class ParsedUri:
    uri_without_scheme: str
    use_tls: bool


@final
class ChalkGRPCClient:
    def __init__(
        self,
        environment: Optional[EnvironmentId] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        api_server: Optional[str] = None,
        additional_headers: Optional[List[tuple[str, str]]] = None,
        environment_id: Optional[EnvironmentId] = None,
        query_server: Optional[str] = None,
        _skip_api_server: bool = False,
    ):
        """
        :param environment_id: ID of the Chalk environment to connect to. If omitted, this is pulled from the current Chalk project config.
        :param client_id: Client ID used to authenticate. If omitted, this is pulled from the current Chalk project config.
        :param client_secret: Client secret used to authenticate. If omitted, this is pulled from the current Chalk project config.
        :param api_server: URI of the Chalk API server used for authentication/metadata.
        :param additional_headers: Additional client metadata to send with GRPC requests.
        :param query_server: Hardcoded URI for Chalk query server, if available.
        :param _skip_api_server: Omits the auth handshake with the API server. Primarily for internal use/testing -- if used in production, this client will simply fail to connect.
        If True then query_server must be provided & point to localhost/127.0.0.1.
        """
        if environment is not None and environment_id is not None:
            raise ValueError("Both environment and environment_id specified; only pass one.")

        if environment_id is not None:
            environment = environment_id

        # deprecating this.
        del environment_id

        if CHALK_IMPORT_FLAG.get() is True:
            raise RuntimeError(
                "Attempting to instantiate a Chalk client while importing source modules is forbidden. "
                + "Please exclude this file from import using your `.chalkignore` file "
                + "(see https://docs.chalk.ai/cli/apply), or wrap this query in a function that is not called upon import."
            )
        additional_headers_nonempty: List[tuple[str, str]] = [] if additional_headers is None else additional_headers
        token_config = load_token(
            client_id=client_id,
            client_secret=client_secret,
            active_environment=environment,
            api_server=api_server,
            skip_cache=False,
        )
        if token_config is None:
            raise ChalkAuthException()

        channel_options: List[tuple[str, str | int]] = [
            ("grpc.max_send_message_length", 1024 * 1024 * 100),  # 100MB
            ("grpc.max_receive_message_length", 1024 * 1024 * 100),  # 100MB
            # https://grpc.io/docs/guides/performance/#python
            (grpc.experimental.ChannelOptions.SingleThreadedUnaryStream, 1),
        ]

        token_refresher: Optional[TokenRefresher]
        if _skip_api_server:
            if query_server is None:
                raise ValueError("If skipping API server auth, query_server URI must be provided. ]]")
            elif not (query_server.startswith("localhost") or query_server.startswith("127.0.0.1")):
                warnings.warn(
                    "Skipping API server auth should only be enabled if query_server URI is localhost. It will fail to authenticate against a production engine."
                )
            self._environment_id = token_config.activeEnvironment
            if self._environment_id is None or self._environment_id == "":
                raise ValueError("No environment specified")
            token_refresher = None
            self._server_channel: Optional[grpc.Channel] = None
        else:
            server_host: str = token_config.apiServer or "api.chalk.ai"
            for pfx in [
                "https://",
                "http://",
                "www.",
            ]:
                server_host = removeprefix(server_host, pfx)

            _unauthenticated_server_channel: grpc.Channel = (
                grpc.insecure_channel(
                    target=server_host,
                    options=channel_options,
                )
                if server_host.startswith("localhost") or server_host.startswith("127.0.0.1")
                else grpc.secure_channel(
                    target=server_host,
                    credentials=grpc.ssl_channel_credentials(),
                    options=channel_options,
                )
            )

            self._auth_stub: AuthServiceStub = AuthServiceStub(
                grpc.intercept_channel(
                    _unauthenticated_server_channel,
                    UnauthenticatedChalkClientInterceptor(
                        server="go-api",
                        additional_headers=additional_headers_nonempty,
                    ),
                )
            )

            token_refresher: Optional[TokenRefresher] = TokenRefresher(
                auth_stub=self._auth_stub,
                client_id=token_config.clientId,
                client_secret=token_config.clientSecret,
            )

            t = token_refresher.get_token()

            self._environment_id = token_config.activeEnvironment or t.primary_environment
            if self._environment_id is None or self._environment_id == "":
                raise ValueError("No environment specified")

            if self._environment_id not in t.environment_id_to_name:
                lower_env_id = self._environment_id.lower()
                valid = [eid for eid, ename in t.environment_id_to_name.items() if ename.lower() == lower_env_id]
                if len(valid) > 1:
                    raise ValueError(f"Multiple environments with name {self._environment_id}: {valid}")
                elif len(valid) == 0:
                    raise ValueError(f"No environment with name {self._environment_id}: {t.environment_id_to_name}")
                else:
                    self._environment_id = valid[0]

            self._server_channel: Optional[grpc.Channel] = grpc.intercept_channel(
                _unauthenticated_server_channel,
                AuthenticatedChalkClientInterceptor(
                    refresher=token_refresher,
                    server="go-api",
                    environment_id=self._environment_id,
                    additional_headers=additional_headers_nonempty,
                ),
            )

            query_server = query_server or t.grpc_engines.get(self._environment_id, None)
        engine_headers = additional_headers_nonempty + [("x-chalk-deployment-type", "engine-grpc")]
        interceptors: List[grpc.UnaryUnaryClientInterceptor] = []
        if token_refresher is not None:
            interceptors.append(
                AuthenticatedChalkClientInterceptor(
                    refresher=token_refresher,
                    environment_id=self._environment_id,
                    server="engine",
                    additional_headers=engine_headers,
                )
            )
        else:
            interceptors.append(
                UnauthenticatedChalkClientInterceptor(
                    server="engine", additional_headers=engine_headers + [("x-chalk-env-id", self._environment_id)]
                )
            )

        self._engine_channel: Optional[grpc.Channel] = None
        if query_server is not None:
            parsed_uri = self._parse_uri_for_engine(query_server_uri=query_server)
            self._engine_channel = grpc.intercept_channel(
                grpc.secure_channel(
                    target=parsed_uri.uri_without_scheme,
                    credentials=grpc.ssl_channel_credentials(),
                    options=channel_options,
                )
                if parsed_uri.use_tls
                else grpc.insecure_channel(
                    target=parsed_uri.uri_without_scheme,
                    options=channel_options,
                ),
                *interceptors,
            )

    @classmethod
    def _parse_uri_for_engine(cls, query_server_uri: str) -> ParsedUri:
        """
        If the scheme is provided, base TLS off of that (http = no tls, https = tls)
        If there is no scheme, default to TLS EXCEPT for localhost/private-vpc uris.
        """
        url_parsed = urlparse(query_server_uri)
        if url_parsed.scheme == "http":
            use_tls = False
        elif url_parsed.scheme == "https":
            use_tls = True
        elif url_parsed.scheme == "" and any(
            query_server_uri.startswith(pfx) for pfx in ["localhost", "127.0.0.1", "10."]
        ):
            use_tls = False
        else:
            use_tls = True
        uri_without_scheme = removeprefix(query_server_uri, url_parsed.scheme + "://")
        return ParsedUri(uri_without_scheme=uri_without_scheme, use_tls=use_tls)

    def __enter__(self):
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
        if self._server_channel is not None:
            self._server_channel.close()
        if self._engine_channel is not None:
            self._engine_channel.close()

    @cached_property
    def _team_stub(self):
        if self._server_channel is None:
            raise RuntimeError("Unable to connect to API server.")
        return TeamServiceStub(self._server_channel)

    @cached_property
    def _query_stub(self) -> QueryServiceStub:
        if self._engine_channel is None:
            raise ValueError(f"No engine channel available for environment {self._environment_id}")
        return QueryServiceStub(self._engine_channel)

    def ping_engine(self, num: Optional[int] = None) -> int:
        if num is None:
            num = random.randint(0, 999)
        response = self._query_stub.Ping(query_server_pb2.PingRequest(num=num))
        return response.num

    def online_query(
        self,
        input: Union[Mapping[FeatureReference, Any], Any],
        output: Sequence[FeatureReference] = (),
        now: Optional[dt.datetime] = None,
        staleness: Optional[Mapping[FeatureReference, str]] = None,
        tags: Optional[List[str]] = None,
        correlation_id: Optional[str] = None,
        query_name: Optional[str] = None,
        query_name_version: Optional[str] = None,
        include_meta: bool = False,
        meta: Optional[Mapping[str, str]] = None,
        explain: Union[bool, Literal["only"]] = False,
        store_plan_stages: bool = False,
        encoding_options: Optional[FeatureEncodingOptions] = None,
        required_resolver_tags: Optional[List[str]] = None,
        planner_options: Optional[Mapping[str, Union[str, int, bool]]] = None,
        request_timeout: Optional[float] = None,
    ) -> Any:
        raise NotImplementedError(
            "Online Query not yet implemented for GRPC, use the Bulk Query Endpoint (ChalkGRPCClient.online_query_bulk(...)) with one row of inputs instead."
        )

    def online_query_bulk(
        self,
        input: Union[Mapping[FeatureReference, Sequence[Any]], DataFrame],
        output: Sequence[FeatureReference] = (),
        now: Optional[Sequence[dt.datetime]] = None,
        staleness: Optional[Mapping[FeatureReference, str]] = None,
        tags: Optional[List[str]] = None,
        correlation_id: Optional[str] = None,
        query_name: Optional[str] = None,
        query_name_version: Optional[str] = None,
        include_meta: bool = False,
        meta: Optional[Mapping[str, str]] = None,
        explain: Union[bool, Literal["only"]] = False,
        store_plan_stages: bool = False,
        encoding_options: Optional[FeatureEncodingOptions] = None,
        required_resolver_tags: Optional[List[str]] = None,
        planner_options: Optional[Mapping[str, Union[str, int, bool]]] = None,
        request_timeout: Optional[float] = None,
    ) -> BulkOnlineQueryResult:
        stub = self._query_stub
        request = self._make_query_bulk_request(
            input=input,
            output=output,
            now=now,
            staleness=staleness,
            tags=tags,
            correlation_id=correlation_id,
            query_name=query_name,
            query_name_version=query_name_version,
            include_meta=include_meta,
            meta=meta,
            explain=explain,
            store_plan_stages=store_plan_stages,
            encoding_options=encoding_options,
            required_resolver_tags=required_resolver_tags,
            planner_options=planner_options,
        )
        response = stub.OnlineQueryBulk(request, timeout=request_timeout)
        return OnlineQueryConverter.online_query_bulk_response_decode(response)

    def multi_query(
        self,
        queries: List[OnlineQuery],
        correlation_id: Optional[str] = None,
        query_name: Optional[str] = None,
        query_name_version: Optional[str] = None,
        include_meta: bool = False,
        meta: Optional[Mapping[str, str]] = None,
        explain: Union[bool, Literal["only"]] = False,
        store_plan_stages: bool = False,
        encoding_options: Optional[FeatureEncodingOptions] = None,
        required_resolver_tags: Optional[List[str]] = None,
        planner_options: Optional[Mapping[str, Union[str, int, bool]]] = None,
        request_timeout: Optional[float] = None,
    ) -> BulkOnlineQueryResponse:
        """Execute a series of independent requests in parallel."""
        requests: List[GenericSingleQuery] = []
        for query in queries:
            # NOTE: This assumed every request is a 'bulk' request.
            request = self._make_query_bulk_request(
                input=query.input,
                output=query.output,
                now=None,
                staleness=query.staleness,
                tags=query.tags,
                correlation_id=correlation_id,
                query_name=query_name,
                query_name_version=query_name_version,
                include_meta=include_meta,
                meta=meta,
                explain=explain,
                store_plan_stages=store_plan_stages,
                encoding_options=encoding_options,
                required_resolver_tags=required_resolver_tags,
                planner_options=planner_options,
            )
            requests.append(GenericSingleQuery(bulk_request=request))
        stub = self._query_stub
        response = stub.OnlineQueryMulti(
            online_query_pb2.OnlineQueryMultiRequest(
                queries=requests,
            ),
            timeout=request_timeout,
        )
        return OnlineQueryConverter.online_query_multi_response_decode(response)

    def _make_query_bulk_request(
        self,
        input: Union[Mapping[FeatureReference, Sequence[Any]], DataFrame],
        output: Sequence[FeatureReference] = (),
        now: Optional[Sequence[dt.datetime]] = None,
        staleness: Optional[Mapping[FeatureReference, str]] = None,
        tags: Optional[List[str]] = None,
        correlation_id: Optional[str] = None,
        query_name: Optional[str] = None,
        query_name_version: Optional[str] = None,
        include_meta: bool = False,
        meta: Optional[Mapping[str, str]] = None,
        explain: Union[bool, Literal["only"]] = False,
        store_plan_stages: bool = False,
        encoding_options: Optional[FeatureEncodingOptions] = None,
        required_resolver_tags: Optional[List[str]] = None,
        planner_options: Optional[Mapping[str, Union[str, int, bool]]] = None,
    ) -> online_query_pb2.OnlineQueryBulkRequest:
        if isinstance(input, DataFrame):
            import pyarrow as pa

            inputs_table: pa.Table = input.to_pyarrow()
            input_batch = df_utils.pa_table_to_recordbatch(inputs_table)
        else:
            import pyarrow as pa

            encoded_inputs = {str(k): v for k, v in input.items()}
            input_batch = pa.RecordBatch.from_pydict(encoded_inputs)
        inputs_bytes = record_batch_to_arrow_ipc(input_batch)
        outputs, _ = encode_outputs(output)

        extra_headers = {}
        if query_name is not None:
            extra_headers["x-chalk-query-name"] = query_name

        now_proto: Optional[List[timestamp_pb2.Timestamp]] = None
        if now is not None:
            now_proto = []
            for ts in now:
                if ts.tzinfo is None:
                    ts = ts.astimezone(tz=dt.timezone.utc)
                now_proto.append(datetime_to_proto_timestamp(ts))

        staleness_encoded = {}
        if staleness is not None:
            for k, v in staleness.items():
                if is_feature_set_class(k):
                    for f in k.features:
                        staleness_encoded[f.root_fqn] = v
                else:
                    staleness_encoded[k] = v

        context_options_dict: Dict[str, Any] = {
            "store_plan_stages": store_plan_stages,
        }
        context_options_dict.update(**(planner_options or {}))
        context_options_proto = {k: value_to_proto(v) for k, v in context_options_dict.items()}
        return online_query_pb2.OnlineQueryBulkRequest(
            inputs_feather=inputs_bytes,
            outputs=[online_query_pb2.OutputExpr(feature_fqn=o) for o in outputs],
            now=now_proto,
            staleness=staleness_encoded,
            context=online_query_pb2.OnlineQueryContext(
                environment=self._environment_id,
                tags=tags,
                required_resolver_tags=required_resolver_tags,
                correlation_id=correlation_id,
                query_name=query_name,
                query_name_version=query_name_version,
                options=context_options_proto,
            ),
            response_options=online_query_pb2.OnlineQueryResponseOptions(
                include_meta=include_meta,
                explain=online_query_pb2.ExplainOptions() if explain else None,
                encoding_options=online_query_pb2.FeatureEncodingOptions(
                    encode_structs_as_objects=encoding_options.encode_structs_as_objects if encoding_options else False
                ),
                metadata=meta,
            ),
            body_type=online_query_pb2.FEATHER_BODY_TYPE_RECORD_BATCHES,
        )

    def create_service_token(
        self,
        name: str,
        permissions: List[Permission],
        customer_claims: Optional[Dict[str, List[str]]] = None,
    ) -> CreateServiceTokenResponse:
        """Create a service token with a given set of permissions and claims.

        Parameters
        ----------
        name
            The name of your service token.
        permissions
            The permissions that you want your token to have.
        customer_claims
            The customer claims that you want your token to have.
        Returns
        -------
        CreateServiceTokenResponse
            A service token response, including a `client_id` and `client_secret` with
            the specified permissions and customer claims.

        Examples
        --------
        >>> from chalk.client import Permission
        >>> client = ChalkGRPCClient(client_id='test', client_secret='test_secret')
        >>> client.create_service_token(permissions=[Permission.PERMISSION_QUERY_ONLINE])
        """
        return self._team_stub.CreateServiceToken(
            CreateServiceTokenRequest(
                name=name,
                permissions=permissions,
                customer_claims=None
                if customer_claims is None
                else [CustomClaim(key=key, values=values) for key, values in customer_claims.items()],
            )
        )
