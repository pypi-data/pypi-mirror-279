import pytest
import sys

from ..lib.FTPconnector import FTPconnector

import logging

logger = logging.getLogger(__name__)

@pytest.fixture(
    name="FTPconnector"
)
def make_FTPconnector():
    return FTPconnector(
        host="ftp.us.debian.org",
        )

def test_connect(FTPconnector):
    FTPconnector.connect()
    assert FTPconnector.ftp is not None

