# construct-tracker
Track and measure constructs, concepts or categories in text documents


# Installation

```bash
pip install construct-tracker
```

# Quick usage






## Releasing a new version

- Create an API Token on [Pypi](https://pypi.org/).
- Create a [new release](https://github.com/danielmlow/construct-tracker/releases/new) on Github. 
Create a new tag in the form ``*.*.*``.


`pyproject.toml` has the requirements

<!-- tutorial to create package: https://www.youtube.com/watch?v=2goLiz4vTss -->

```
conda activate construct_poetry
pip install poetry # create file with dependencies
poetry config virtualenvs.in-project true
poetry lock
poetry install
poetry config pypi-token.pypi API_token
poetry build
poetry publish
```

To reflect any new changes in pypi, change the version number in pyproject.toml
```
poetry build
poetry publish
```
