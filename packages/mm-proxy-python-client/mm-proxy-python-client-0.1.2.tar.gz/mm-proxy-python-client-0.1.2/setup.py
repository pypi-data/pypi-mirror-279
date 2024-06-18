# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from mm_proxy_python_client import __version__

with open("README.md") as f:
    README = f.read()


VERSION = __version__


setup(
    name="mm-proxy-python-client",
    version=VERSION,
    author="SomConnexió",
    author_email="gerard.funosas@somconnexio.coop",
    maintainer="Gerard Funosas",
    url="https://git.coopdevs.org/coopdevs/som-connexio/masmovil/mm-proxy-python-client",  # noqa
    description="Python wrapper for SomConnexio's MM Proxy (using REST API)",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("tests", "docs")),
    include_package_data=True,
    zip_safe=False,
    install_requires=["requests"],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        "Operating System :: POSIX :: Linux",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3",
    ],
)
