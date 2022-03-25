"""
Python 3 Open LN metrics API that provide an easy access to
Open LN metrics services.

author: https://github.com/vincenzopalazzo
"""
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from .queries import GET_NODE, GET_NODES, GET_METRIC_ONE


class LNMetricsClient:
    """
    LNMetrics Client implementation
    """

    def __init__(self, service_url: str) -> None:
        transport = AIOHTTPTransport(url=service_url)
        self.client = Client(transport=transport, fetch_schema_from_transport=True)

    def call(self, query, variables: dict = None) -> dict:
        """Generic method to make a query to the Graphql Server"""
        return self.client.execute(query, variable_values=variables)

    def get_node(self, network: str, node_id: str) -> dict:
        """Retrieval the node information for {node_id} on the {network}"""
        # TODO: adding query
        query = gql(GET_NODE)
        variables = {"network": network, "node_id": node_id}
        return self.call(query, variables=variables)

    def get_nodes(self, network: str) -> dict:
        """get the list of all the nodes on the server"""
        query = gql(GET_NODES)
        variables = {
            "network": network,
        }
        return self.call(query, variables=variables)

    def get_metric_one(
        self, network: str, node_id: str, first: int = None, last: int = None
    ) -> dict:
        """get the list of metrics of the {node_id}, with the possibility to filter by the period {first} {last}"""
        query = gql(GET_METRIC_ONE)
        variables = {
            "network": network,
            "node_id": node_id,
            "first": first,
            "last": last,
        }
        return self.call(query, variables=variables)
