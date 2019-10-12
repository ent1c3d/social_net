import os
import time

from contextlib import contextmanager
from invoke import task


PYTHON_VERSION = "python3.6"

ENVIRONMENT = {
}


def docker_compose_cmd(param_str):
    docker_compose_file = "-f docker-compose.yml"
    return f"docker-compose {docker_compose_file} {param_str}"


class Venv:
    """Misc. commands for handling virtual envs"""

    cur_dir = os.path.dirname(os.path.abspath(__file__))
    _dir = os.path.join(cur_dir, ".venv")
    _activate_path = os.path.join(_dir, "bin", "activate")
    _activate = ". {}".format(_activate_path)
    _build = "virtualenv --python={} {}".format(PYTHON_VERSION, _dir)

    @classmethod
    def _setup_venv(cls, c):
        """Setup virtualenv for local Python runs"""
        if not os.path.exists(cls._dir):
            c.run(cls._build)

    @classmethod
    @contextmanager
    def virtualenv(cls, c):
        cls._setup_venv(c)
        with c.cd(cls.cur_dir), c.prefix(cls._activate):
            c.run("pip install --upgrade pip")
            c.run(f"pip install -r requirements.txt")
            yield


@task
def start_docker(c, build=False):
    cmd = "up -d"
    if build:
        cmd += " --build"
    cmd = docker_compose_cmd(cmd)
    try:
        c.run(cmd, env=ENVIRONMENT)
        time.sleep(5)
    except:
        stop_docker(c)

@task
def stop_docker(c):
    cmd = docker_compose_cmd("down --remove-orphans")
    c.run(cmd, env=ENVIRONMENT)

@task
def restart(c, build=False):
    stop_docker(c)
    start_docker(c, build=build)

@contextmanager
def _with_docker(c):
    try:
        start_docker(c)
        yield
    finally:
        stop_docker(c)

@task
def execute_bot(c):
    with Venv.virtualenv(c):
        c.run(f"python -m bot.client", env=ENVIRONMENT)

@task
def migrate(c):
    with Venv.virtualenv(c):
        c.run(f"python manage.py migrate", env=ENVIRONMENT)


@task
def set_env(c):
    for k, v in ENVIRONMENT.items():
        print(f"export {k}={v}")

