import os
import logging
import subprocess
from poetry_env_test.utils.utils import unset_python_path, run_command


def backup_dependencies(file_path="dependencies_backup.json"):
    result = subprocess.run(
        f"poetry export -f json -o {file_path}",
        shell=True,
        capture_output=True,
        text=True,
        check=True,
    )
    if result.returncode != 0:
        logging.error("Failed to backup dependencies: %s", result.stderr)
        return False
    logging.info("Dependencies backed up to %s", file_path)
    return True


def restore_dependencies(file_path="dependencies_backup.json"):
    if not os.path.exists(file_path):
        logging.error("Backup file %s does not exist.", file_path)
        return False
    result = subprocess.run(
        ("poetry install --dev --remove-untracked --file %s", file_path),
        shell=True,
        capture_output=True,
        text=True,
        check=True,
    )
    if result.returncode != 0:
        logging.error("Failed to restore dependencies: %s", result.stderr)
        return False
    logging.info("Dependencies restored from backup")
    return True


def clean_project():
    unset_python_path()

    logging.info("Backing up current dependencies")
    if not backup_dependencies():
        return

    logging.info("Removing existing Poetry environment")
    if not run_command("poetry env remove $(poetry env info --path)"):
        return

    logging.info("Reinstalling dependencies with Poetry")
    if not run_command("poetry install"):
        logging.info("Restoring dependencies from backup")
        restore_dependencies()
        return

    logging.info("Environment setup completed successfully")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    clean_project()
