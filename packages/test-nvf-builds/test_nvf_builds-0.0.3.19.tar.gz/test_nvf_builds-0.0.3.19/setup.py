import os
import re

from setuptools import find_packages, setup


def read_version():
    init_py = os.path.join(os.path.dirname(__file__), 'oasysnow', '__init__.py')
    with open(init_py) as f:
        for line in f:
            match = re.match(r"^__version__ = ['\"]([^'\"]*)['\"]", line)
            if match:
                return match.group(1)
    raise RuntimeError("Unable to find version string in my_package/__init__.py")


setup(
    package_dir={"oasysnow": "oasysnow"},
    version=read_version(),
    packages=find_packages(
        where=".",
        include=[
            "*",
        ],
        exclude=["tests", "tests.*"],
    ),
    package_data={
        "": ["*.npz"],
    },
    include_package_data=True,
)
