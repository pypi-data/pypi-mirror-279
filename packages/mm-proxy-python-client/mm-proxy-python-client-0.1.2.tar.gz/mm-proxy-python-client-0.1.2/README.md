[![pipeline status](https://gitlab.com/coopdevs/odoo-somconnexio-python-client/badges/master/pipeline.svg)](https://gitlab.com/coopdevs/odoo-somconnexio-python-client/commits/master)
[![coverage report](https://gitlab.com/coopdevs/odoo-somconnexio-python-client/badges/master/coverage.svg)](https://gitlab.com/coopdevs/odoo-somconnexio-python-client/commits/master)

:warning: WORK IN PROGRESS :warning:

This library is a Python wrapper for accessing Somconnexio's Odoo (Odoo v12 with customizations).
More info about the customizations in [SomConnexio Odoo module](https://gitlab.com/coopdevs/odoo-somconnexio).

## Resources

* AssetConsumption - Asset consumption


## Installation

```commandline
$ pip install mm-proxy-python-client
```

## Configuration Environment

You need define the mm-proxy basic autenthication user and password and the host URL as environment variables. You need to define:

```
MM_PROXY_BASEURL=<YOUR MM-PROXY HOST>/api
MM_PROXY_USER=<YOUR MM-PROXY BASIC AUTH USER>
MM_PROXY_PASSWORD=<YOUR MM-PROXY BASIC AUTH PASSWORD>
```

If this envvars are not defined, a exception will be raised with the name of the envvar not defined.


## Usage

#### Get mobile consumption

```python
>>> from mm_proxy_python_client.resources.mobile_consumption import MobileConsumption
>>>
>>> consumption = MobileConsumption.get(asset_id="", phone_number="666888999", start_date="2023-12-01", end_date="2023-13-31")
>>> consumption.asset_id
123
>>> consumption.tariffs[0].dataTotal
"10240"
```


## Development

### Setup environment

1. Install `pyenv`
```sh
curl https://pyenv.run | bash
```
2. Build the Python version
```sh
pyenv install  3.8.13
```
3. Create a virtualenv
```sh
pyenv virtualenv 3.8.13 mm-proxy-python-client
```
4. Install dependencies
```sh
pyenv exec pip install -r requirements-dev.txt
```
5. Install pre-commit hooks
```sh
pyenv exec pre-commit install
```

### Test the HTTP request

We are using the HTTP recording plugin of Pytest: [pytest-recording](https://pytest-vcr.readthedocs.io/).

With VRC we can catch the HTTP responses and then, execute the tests using them.

To actually call the mm-proxy local client in order to create or rewrite cassettes using the next pyenv commands, we need to first change the `conftest.py` file and temporally provide the actual mm-proxy user and password.

```
monkeypatch.setenv("MM_PROXY_PASSWORD", "<ACTUAL_MM_PROXY_PASSWORD>")
```
⚠️
**Do not commit this change!**

To add a new test:

* Expose the needed envvars. Look for them at the [Configuration Environment section](#configuration-environment)
* Execute the tests using `pytest` command:
* If you are writing a new test that is making requests, you should run:

```
$ pytest --record-mode=once path/to/your/test
```

* You might need to record requests for an specific tests. In that case make sure to only run the tests affected and run

```
$ pytest --record-mode=rewrite path/to/your/test
```

* Add the new `cassetes` to the commit and push them.
* The CI uses the cassetes to emulate the HTTP response in the test.

### Run test suite

```commandline
$ tox
```

### Formatting

We use [pre-commit](https://pre-commit.com/) to execute [Flake8](https://github.com/pycqa/flake8), [yamllint](https://github.com/adrienverge/yamllint.git) (for the cassetes) and [Black](https://github.com/psf/black) as formatter.


### Release process

Update CHANGELOG.md following this steps:

1. Add any entries missing from merged merge requests.
1. Duplicate the `[Unreleased]` header.
1. Replace the second `Unreleased` with a version number followed by the current date. Copy the exact format from previous releases.

Then, you can release and publish the package to PyPi:

1. Update the `__version__` var in `__init__.py` matching the version you specified in the CHANGELOG.
1. Open a merge request with these changes for the team to approve
1. Merge it, add a git tag on that merge commit and push it.
1. Once the pipeline has successfully passed, go approve the `publish` step.
