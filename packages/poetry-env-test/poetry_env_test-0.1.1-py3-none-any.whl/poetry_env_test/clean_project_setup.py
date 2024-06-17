import os
import logging
import subprocess
from poetry_env_test.utils.utils import unset_python_path, run_command


def clean_project():
    unset_python_path()

    logging.info("Removing existing Poetry environment")
    if not run_command("poetry env remove $(poetry env info --path)"):
        return

    logging.info("Reinstalling dependencies with Poetry")
    if not run_command("poetry install"):
        return

    logging.info("Environment setup completed successfully")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    clean_project()
