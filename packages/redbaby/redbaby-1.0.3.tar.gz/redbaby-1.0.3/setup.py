import shlex
import subprocess

import setuptools


def read_multiline_as_list(file_path: str) -> list[str]:
    with open(file_path, "r") as fh:
        contents = fh.read().split("\n")
        if contents[-1] == "":
            contents.pop()
        return contents


def get_version() -> str:
    raw_git_cmd = "git describe --tags"
    git_cmd = shlex.split(raw_git_cmd)
    fmt_cmd = shlex.split("cut -d '-' -f 1,2")
    git = subprocess.Popen(git_cmd, stdout=subprocess.PIPE)
    cut = subprocess.check_output(fmt_cmd, stdin=git.stdout)
    ret_code = git.wait()
    assert ret_code == 0, f"{raw_git_cmd!r} failed with exit code {ret_code}."
    return cut.decode().strip()


with open("README.md", "r") as fh:
    long_description = fh.read()
requirements = read_multiline_as_list("requirements.txt")


setuptools.setup(
    name="redbaby",
    version=get_version(),
    description="Mini reimplementation of REDB, baby redb, redbaby.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Nei Cardoso de Oliveira Neto",
    author_email="nei@teialabs.com",
    url="https://github.com/teialabs/redbaby",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    python_requires=">=3.11",
)
