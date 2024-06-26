build:
	rm -rf dist/*
	pipenv install --dev
	pipenv run python -m build

install-pkg:
	pipenv run python -m pip install dist/iam_minify-0.0.4-py3-none-any.whl --force-reinstall

test:
	pipenv run python -m pytest tests/*
