from os import getenv
from urllib.parse import urljoin

import pytest


def test_mock_get_virtual_meters_general_info(mocker, iccpro):
    m = mocker.patch("requests.Session.request")

    iccpro.get_virtual_meters_general_info()

    m.assert_called_once_with(
        "GET",
        urljoin(getenv("iccpro_host"), "iccpro/api/virtualmeters"),
    )


@pytest.mark.skipif(not getenv("iccpro_host"), reason="Missing config")
def test_get_virtual_meters_general_info(iccpro):
    assert iccpro.get_virtual_meters_general_info()
