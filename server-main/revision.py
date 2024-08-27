# TODO: rewrite in BASH

import subprocess
from sys import argv

args = " ".join(argv[1:])
process = subprocess.Popen(
    [
        # "docker-compose",
        # "exec",
        # "server-main",
        "alembic",
        "revision",
        "--autogen",
        "-m",
        f'"{args}"',
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)
stdout, stderr = process.communicate()

print(stdout.decode())

if stderr:
    print(stderr.decode())
    print(
        """
Maybe db container doesn't run? Run `ss -tunlp` to check your ports
and `docker ps` to check docker containers.
"""
    )
