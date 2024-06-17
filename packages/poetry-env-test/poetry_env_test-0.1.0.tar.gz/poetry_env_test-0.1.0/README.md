# poetry-env-test

`poetry-env-test` is a Python package designed to manage and verify Python project environments using Poetry. This package provides tools to clean and set up project environments, check dependencies, and backup and restore dependency configurations.

## Features

- **Clean Project Environment**: Unset `PYTHONPATH`, remove existing Poetry environments, and reinstall dependencies.
- **Check Project Setup**: Verify the presence and structure of project dependencies.
- **Backup and Restore Dependencies**: Backup current dependencies to a file and restore them if needed.

## Installation

To install `poetry-env-test`, you need to have Poetry installed. You can install Poetry by following the [official installation guide](https://python-poetry.org/docs/#installation).

Then, you can add `poetry-env-test` to your project using the following command:

```bash
poetry add poetry-env-test
```

Usage

Command Line Interface

This package provides several CLI commands that can be used to manage your project environment.

Check Project Setup

To check the project setup and verify dependencies:

```sh
poetry run check-project-setup
```

Clean Project Setup

To clean the project setup by unsetting `PYTHONPATH`, removing existing Poetry environments, and reinstalling dependencies:

```sh
poetry run clean-project-setup
```

Backup Dependencies

To backup the current dependencies to a file:

```sh
poetry run backup-dependencies
```

## Contributing

Contributions are welcome! Please follow these steps to contribute:

	1.	Fork the repository.
	2.	Create a new branch for your feature or bugfix.
	3.	Commit your changes.
	4.	Push the branch to your fork.
	5.	Create a pull request.

Please ensure your code follows the project’s coding standards and includes appropriate tests.

License

This project is licensed under the MIT License. See the LICENSE file for details.

## Authors

	Carrow Morris-Wiltshire - visit my [website](carrow.me.uk")

## Acknowledgments
    GPT-4o assisted in making this package. So thank you to all of the contributers to the platforms that LLMs are trained on as well as GPT-4o (if you are reading this).