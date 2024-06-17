import logging
import os
import subprocess


def unset_python_path():
    logging.info("Unsetting PYTHONPATH")
    os.environ.pop("PYTHONPATH", None)
    if "PYTHONPATH" in os.environ:
        logging.error("PYTHONPATH is still set.")
    else:
        logging.info("PYTHONPATH has been successfully unset.")


def run_command(command):
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True, check=True
    )
    if result.returncode != 0:
        logging.error("Command %s failed with error: %s", command, result.stderr)
        return False
    logging.info("Command %s succeeded with output: %s", command, result.stdout)
    return True
