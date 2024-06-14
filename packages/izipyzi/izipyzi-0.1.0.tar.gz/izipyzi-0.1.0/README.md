# izipyzi

## Project files

### `.commitlintrc.json` and `.releaserc.json`

These files are used by `semantic-release` to determine the type of the next release. The `.commitlintrc.json` file is used to lint the commit messages. The `.releaserc.json` file is used to determine the version of the next release based on the commit messages. To lint commit messages, this project uses the default configuration of `@commitlint/config-conventional`.

### `.python-version` file

The `.python-version` file contains the python version used in this project. This project has been built with using `pyenv` as python version manager.

### `.pre-commit-config.yaml` file

This file is used by `pre-commit` to determine the hooks that will be run before each commit. The hooks are defined in the `hooks` section of the file. The hooks are run in the order they are defined in the file.

### `.github/workflows` folder

This repository uses Github Actions for CI/CD. CI is composed of `Lint` with pre-commit and `Test` with pytest. Release is composed of `Lint`, `Test`, `Release` with semantic-release.

- Lint is done with [pre-commit](https://pre-commit.com/). To run lint locally, run `pre-commit run --all-files`.
- Test is done with [pytest](https://docs.pytest.org/en/8.0.x/). To run test locally, run `pytest`. Or poetry run `pytest` if you use poetry as package manager.
- Release is done with [semantic-release](https://github.com/semantic-release/semantic-release)
