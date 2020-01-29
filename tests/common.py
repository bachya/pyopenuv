"""Define common test utilities."""
import os

TEST_ALTITUDE = "1609.3"
TEST_API_KEY = "12345"
TEST_LATITUDE = "51.528308"
TEST_LONGITUDE = "-0.3817803"


def load_fixture(filename):
    """Load a fixture."""
    path = os.path.join(os.path.dirname(__file__), "fixtures", filename)
    with open(path, encoding="utf-8") as fptr:
        return fptr.read()
