import pytest
from lnmetrics_api import LNMetricsClient


@pytest.fixture(scope="session", autouse=True)
def client():
    return LNMetricsClient(service_url="https://api.lnmetrics.info/query")


@pytest.fixture(scope="session", autouse=True)
def sync_client():
    return LNMetricsClient(service_url="https://api.lnmetrics.info/query", sync=True)
