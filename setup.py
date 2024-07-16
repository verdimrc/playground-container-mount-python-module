import os
from setuptools import find_packages, setup

_repo: str = "playground-container-mount-python-module"
_pkg: str = "haha"
_version = "0.0.1"


def read_lines(fname: str) -> list[str]:
    """Read the content of a file.

    You may use this to get the content of, for e.g., requirements.txt, VERSION, etc.
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).readlines()

setup(
    name=_pkg,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    version=_version,
    description="Example to mount Python module to container",
    long_description="".join(read_lines("README.md")),
    author="Verdi March",
    url=f"https://github.com/verdimrc/playground-container-mount-python-module/",
    download_url="",
    project_urls={
        "Bug Tracker": f"https://github.com/verdimrc/playground-container-mount-python-module/issues/",
        "Source Code": f"https://github.com/verdimrc/playground-container-mount-python-module/",
    },
    license="MIT License",
    keywords="word1 word2 word3",
    platforms=["any"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.10.0",
)
