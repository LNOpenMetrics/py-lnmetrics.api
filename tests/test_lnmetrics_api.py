import time
import logging
from lnmetrics_api import LNMetricsClient
from datetime import datetime, timedelta


def test_get_nodes_call(client: LNMetricsClient) -> None:
    """Test GetNodes call"""
    response = client.get_nodes(network="bitcoin")
    logging.debug(f"Response {response}")
    assert "errors" not in response


def test_get_node_call(client: LNMetricsClient) -> None:
    """Test GetNodes call"""
    response = client.get_nodes(network="bitcoin")
    for node in response:
        response = client.get_node(network="bitcoin", node_id=node["node_id"])
        logging.debug(f"Node: {response}")
        assert response is not None


def test_get_metric_one(client: LNMetricsClient) -> None:
    """Get the metrics from one node"""
    response = client.get_nodes(network="bitcoin")
    node = response[0]
    last_update = datetime.fromtimestamp(node["last_update"])
    first = last_update.replace(minute=0, second=0, microsecond=0) - timedelta(hours=4)
    response = client.get_metric_one(
        network="bitcoin",
        node_id=node["node_id"],
        first=first.timestamp(),
        last=last_update.timestamp(),
    )
    logging.debug(response)
    assert response is not None


def test_get_metric_one_paginator(client: LNMetricsClient) -> None:
    """Get the metrics from one node with paginator"""
    response = client.get_nodes(network="bitcoin")
    node = response[0]
    last_update = datetime.fromtimestamp(node["last_update"])
    first = last_update - timedelta(hours=24)
    last = last_update - timedelta(hours=24 - 6)
    response = client.get_metric_one(
        network="bitcoin",
        node_id=node["node_id"],
        first=time.mktime(first.timetuple()),
        last=time.mktime(last.timetuple()),
    )
    logging.debug(response)

    assert "page_info" in response
    page_info = response["page_info"]
    has_next = page_info["hash_next_page"]
    counting_request = 1
    while has_next:
        first = page_info["start"]
        last = page_info["end"]
        response = client.get_metric_one(
            network="bitcoin",
            node_id=node["node_id"],
            first=first,
            last=last,
        )
        assert response is not None
        counting_request += 1
        assert "page_info" in response
        page_info = response["page_info"]
        has_next = page_info["hash_next_page"]
    # TODO: check why this fails
    # assert counting_request == 4
