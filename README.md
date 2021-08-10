# pytemplate

A bare-bones Python package that serves as a template for other Python packages.
The `pytemplate` package merely exposes a few relatively useless functions, but
it serves to illustrate how tests, documentation, CI etc. should be structured
for Kinaxis repositories.

## Documentation

In-depth guides for setting up various parts of the repository, including ci and
documentation, can be found at
[http://docs.rubikloudcorp.com/pytemplate](http://docs.rubikloudcorp.com/pytemplate)


# Development

## Python

Python 2 support for Kinaxis projects has been deprecated since 2020, and any ongoing
development should not support it except in the most extenuating circumstances. To
keep up with new language features while maintaining stability, we officially target
python at one major version behind the most recent stable major version. As of
April 2021, the latest stable major version is python 3.9, so this repository is
targeted at python 3.8.


## Docker

python:3.8-slim is provided as the base image, as it is the latest version of python we
currently support and the -slim image contains a basic set of tools (e.g. bash)
above and beyond a base alpine image. This can be replaced with
rubikloud/multi-python in the case that multiple python versions are required. If
spark is required, py3-spark is a python 3.7 image that includes
spark HDFS connectors for GCS, Azure Blobs, and S3.

## Setting up the development environment

Just run `docker-compose run shell`. That's your entire development environment!

## Setting up pre-commit hooks

```
pip install pre-commit
pre-commit install
```

Hooks can be modified in .pre-commit-config.yaml and run with `pre-commit run`.

## Running tests

From inside the docker shell, run `nox --list` to see all possible nox sessions.
To run tests using Python3.8 for example, run:
```
nox -s tests-3.8 --envdir /nox
```
To run tests in all python versions:
```
nox -s tests --envdir /nox
```
> Note: use of `--envdir /nox` is optional, but highly recommended when
running tests in a docker container on OSX. Otherwise the read/write
speed to the default `.nox` folder will be *very* slow.

## Releasing new versions

When you think a **master commit** (don't do this on non-master commits unless
you know what you're doing) is ready to be released, go to the [Github releases
page](https://github.com/rubikloud/pytemplate/releases) and create a new
release. **Please make sure to add a detailed description of what this version
adds to Pytemplate**.

Once the release is drafted, it will trigger the [Github actions release workflow](.github/workflows/pythonpublish.yml)
which will publish a new pypi package. You can confirm that the workflow ran successfully by going to our internal
[PyPi repository](https://pypicloud.rubikloudcorp.com/) and check that the new package with the right version is there.

## Docker-Sync (optional)

You may optionally use Docker-Sync to speed up your development on docker for mac.
This will improve the read/write speed for all files in the repository.
Docker-Sync uses `unison` to provide fast two-way synchronization of your
local files to a docker volume. Using Docker-Sync is significantly
faster then using a traditional bind-mount docker volume on Mac OS.

Install [docker-sync](http://docker-sync.io/):
```
gem install docker-sync --user-install
```

Start the Docker-Sync container. This may take a little while the first time
(especially if you have a lot of temporary data in your local directory).
Once it is completed you will have a docker volume `pytemplate-sync` that
contains your local code.
```
docker-sync start
```
Now Docker-Sync will continue to sync your local directory with
the docker volume.

Start the development containers using the regular docker-compose file,
PLUS the docker-compose-sync overrides.
```
docker-compose -f docker-compose.yml -f docker-compose-sync.yml run shell
```

To stop Docker-Sync and cleanup the `pytemplate-sync` volume, run:
```
docker-sync clean
```
