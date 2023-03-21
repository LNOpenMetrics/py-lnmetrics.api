"""
Python 3 Open LN metrics API that provide an easy access to
Open LN metrics services.

author: https://github.com/vincenzopalazzo
"""
import logging
from typing import Any, Dict, Optional, Union

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.requests import log as requests_logger

from lnmetrics_api.queries.queries import LOCAL_SCORE_OUTPUT
from .queries import GET_NODE, GET_NODES, GET_METRIC_ONE


class LNMetricsClient:
    """
    LNMetrics Client implementation
    """

    def __init__(
        self, service_url: str, timeout: int = 40, log_level=logging.WARNING
    ) -> None:
        transport = AIOHTTPTransport(url=service_url)
        requests_logger.setLevel(log_level)
        self.client = Client(
            transport=transport,
            fetch_schema_from_transport=True,
            execute_timeout=timeout,
        )

    def call(self, query, variables: Optional[Dict] = None) -> Dict:
        """Generic method to make a query to the Graphql Server"""
        return self.client.execute(query, variable_values=variables)

    @staticmethod
    def __unwrap_error(query_name: str, payload: dict) -> dict:
        if "error" in payload:
            raise Exception(f"{payload['error']}")
        assert query_name in payload
        return payload[query_name]

    def get_node(self, network: str, node_id: str) -> dict:
        """Retrieval the node information for {node_id} on the {network}"""
        # TODO: adding query
        query = gql(GET_NODE)
        variables = {"network": network, "node_id": node_id}
        resp = self.call(query, variables=variables)
        return LNMetricsClient.__unwrap_error("getNode", resp)

    def get_nodes(self, network: str) -> dict:
        """get the list of all the nodes on the server"""
        query = gql(GET_NODES)
        variables = {
            "network": network,
        }
        resp = self.call(query, variables=variables)
        return LNMetricsClient.__unwrap_error("getNodes", resp)

    def cast_to_int_or_none(self, value: Optional[int]) -> Optional[int]:
        if value is None:
            return value
        return int(value)

    def get_metric_one(
        self,
        network: str,
        node_id: str,
        first: Optional[int] = None,
        last: Optional[int] = None,
    ) -> dict:
        """Get the metrics collected during the time between [first and last]

        :param network: The network where we want to collect the data
        :param node_id: the node pub key of the lightnign network node
        :param first: the first timestamp where the user is interested about
        :param last: the last timestamp where the user is interested (not must that 6h from the first)
        :return a JSON response that contains the PageInfo to implement the iteration, if the user want get more metrics
        """
        query = gql(GET_METRIC_ONE)
        variables = {
            "network": network,
            "node_id": node_id,
            "first": self.cast_to_int_or_none(first),
            "last": self.cast_to_int_or_none(last),
        }
        resp = self.call(query, variables=variables)
        return LNMetricsClient.__unwrap_error("metricOne", resp)

    def get_local_score_output(self, network: str, node_id: str) -> Dict[str, Any]:
        """Return the Local Score Output"""
        query = gql(LOCAL_SCORE_OUTPUT)
        variables = {
            "network": network,
            "node_id": node_id,
        }
        resp = self.call(query, variables=variables)
        return LNMetricsClient.__unwrap_error("getMetricOneResult", resp)
