import glob
import os
import re

import nox
from pycobertura import Cobertura

nox.options.error_on_missing_interpreters = True


@nox.session(python=["3.8"], reuse_venv=True)
def tests(session):
    session.install(".[tests]")
    session.run(
        "pytest",
        "tests",
        "--cov=pytemplate",
        f"--cov-report=html:htmlcov-py{session.virtualenv.interpreter}",
        f"--cov-report=xml:currentcov/coverage-py{session.virtualenv.interpreter}.xml",
        f"--junitxml=junit-py{session.virtualenv.interpreter}.xml",
    )


@nox.session(python="3.8", reuse_venv=True)
def linter(session):
    session.install("pre-commit")
    session.run("pre-commit", "run")


@nox.session(python="3.8", reuse_venv=True)
def docs(session):
    package_name = "pytemplate"
    html_path = "docs/_build/html"
    s3_path = "s3://docs.rubikloudcorp.com/pytemplate/"

    session.install(".[docs]")

    session.log("Generating documentation...")
    session.run("sphinx-apidoc", "-M", "-f", "-e", "-P", "-o", "docs", package_name)
    session.run("sphinx-build", "-b", "html", "docs", html_path)

    if "publish" in session.posargs:
        session.log("Publishing documentation...")
        session.run("aws", "s3", "rm", "--recursive", s3_path)
        session.run("aws", "s3", "cp", "--recursive", html_path, s3_path)


@nox.session(python="3.8", reuse_venv=True)
def coverage(session, tolerance=0.002):
    failure = False
    reports = glob.glob("currentcov/*.xml")
    if not reports:
        failure = True
        status = "Missing code coverage report"

    for report in reports:
        report = re.sub(r".*cov", "cov", report)
        match = re.search(r"coverage-py(?P<python_version>\d\.\d).xml", report)
        if not match:
            status = "Coverage file name ({name}) is weird".format(name=report)
            failure = True
            break
        python_version = match["python_version"]
        exists = os.path.isfile(f"mastercov/{report}")
        if exists:
            master_rate = Cobertura(f"mastercov/{report}").line_rate()
            current_rate = Cobertura(f"currentcov/{report}").line_rate()
            delta = current_rate - master_rate

            status = "Coverage of {:.2%} ({:+.2%}) for Python {}".format(
                current_rate, delta, python_version
            )
            session.log(status)
            if abs(delta) > tolerance and delta < 0:
                failure = True
                break
        else:
            status = "No master code coverage found for Python {}".format(
                python_version
            )
            session.log(status)

    with open("coverage_status", "w") as fo:
        fo.write(status)

    if failure:
        session.error(status)
