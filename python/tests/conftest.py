"""
    conftest is the fixture list for pytest
    the fixtures themselves are in a separate directory structure underneath fixtures/ and should be imported here
    Thanks to: https://gist.github.com/peterhurford/09f7dcda0ab04b95c026c60fa49c2a68
"""
from glob import glob


def refactor(string: str) -> str:
    return string.replace("/", ".").replace("\\", ".").replace(".py", "")


pytest_plugins = [
    refactor(fixture) for fixture in glob("tests/fixtures/*.py") if "__" not in fixture
]
