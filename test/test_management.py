import pytest

from nameko_management import Management


class ServiceWithManagement(object):
    name = "service"
    management = Management()


@pytest.fixture
def config():
    return {
    }


@pytest.fixture
def container(container_factory, config):
    return container_factory(ServiceWithManagement, config)


def test_management(container):
    assert True is True
