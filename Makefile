build:
	pipenv install --dev
	pipenv run python -m build

install-pkg:
	pipenv run python -m pip install dist/iam_minify-0.0.1-py3-none-any.whl --force-reinstall