import pkgutil
import sys
import os
import logging


def check_dependencies(directories=None):
    if directories is None:
        directories = [
            "/Users/administrator/Code/python/phd/src",
            "/Users/administrator/Code/python/phd",
        ]

    logging.basicConfig(level=logging.INFO)
    for directory in directories:
        if not os.path.isdir(directory):
            logging.error("The directory %s does not exist.", directory)
            continue

        logging.info("Checking dependencies in directory %s", directory)
        for _, modname, ispkg in pkgutil.iter_modules([directory]):
            logging.info(
                "    Found module/submodule %s (is a package: %s)", modname, ispkg
            )


def print_python_path():
    print("\nCurrent PYTHONPATH:")
    for path in sys.path:
        if sys.path == "":
            print("    (empty)")
        print(path)


def check_env_info():
    print("\nPoetry Environment Info:")
    os.system("poetry env info")


if __name__ == "__main__":
    check_dependencies()
    print_python_path()
    check_env_info()
