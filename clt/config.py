import os
import sys

def get_config() -> dict:
    """Read the configuration file and return a dictionary of the values."""
    config = {}
    try:
        filename = os.path.join(os.path.dirname(__file__), "app.cfg")
        with open(filename, mode="rb") as config_file:
            exec(compile(config_file.read(), filename, "exec"), config)
    except OSError as e:
        print("Error reading configuration file:", e)
        sys.exit(1)
    return config

def generate_pypi_readme(config: dict) -> str:
    """Generate the PyPI README string from the template README file."""
    readme = ""
    try:
        filename = os.path.join(os.path.dirname(__file__), "README.md.tmpl")
        with open(filename, mode="r") as readme_file:
            readme = readme_file.read()
        return readme.format(**config)
    except OSError as e:
        print("Error reading template README file:", e)
        sys.exit(1)