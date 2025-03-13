"""Trigger and track Jenkins builds based on GitHub push events."""

from os import getenv

from jenkins import Jenkins
from jenkins import JenkinsException
from tenacity import retry
from tenacity import retry_if_exception
from tenacity import retry_if_result
from tenacity import wait_fixed


JOB_NAME = getenv("JOB_NAME")

jenkins = Jenkins(
    getenv("JENKINS_URL"),
    username=getenv("JENKINS_USER"),
    password=getenv("JENKINS_PASSWORD"),
)


def on_github_push(event):
    if not event.data.get("ref") == "refs/heads/main":
        print("not main")
        return

    _must_build(JOB_NAME, event.data.get("after"))


# Retry until build is successful.
@retry(
    retry=(
        retry_if_result(lambda r: r != "SUCCESS") | retry_if_exception(JenkinsException)
    )
)
def _must_build(job_name, sha):
    build_number = jenkins.get_job_info(job_name)["nextBuildNumber"]

    build_id = jenkins.build_job(job_name, {"sha": sha})

    print(f"job {job_name}(sha={sha}) started: build id {build_id}, #{build_number}")

    return _track(job_name, build_number)


# Retry until there is a result.
@retry(
    wait=wait_fixed(3),
    retry=(retry_if_result(lambda r: not r) | retry_if_exception(JenkinsException)),
)
def _track(job_name, build_number):
    bi = jenkins.get_build_info(job_name, build_number)
    if bi.get("building"):
        print(f"build {build_number} is building")
        return ""

    result = bi.get("result")

    print(f"build {build_number} finished with result {result}")

    return result
