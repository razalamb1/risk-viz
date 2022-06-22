"""Test combining Google Maps and NPR data."""

from src.heat_maps import access_api
from dotenv import load_dotenv
import os

load_dotenv()


def test_get_line():
    """Test function getting line objects."""
    token = os.environ.get("TOKEN")
    data = access_api(
        columns=["BPHIGH_CrudePrev"],
        state="California",
        county="Alameda",
        token=token,
    )
    assert data["features"][0]["type"]
    pass
