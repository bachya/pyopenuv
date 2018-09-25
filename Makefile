coverage:
	pipenv run py.test -s --verbose --cov-report term-missing --cov-report xml --cov=pyopenuv tests
init:
	pip install --upgrade pip pipenv
	pipenv lock
	pipenv install --dev
lint:
	pipenv run flake8 pyopenuv
	pipenv run pydocstyle pyopenuv
	pipenv run pylint pyopenuv
publish:
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine upload dist/*
	rm -rf dist/ build/ .egg pyopenuv.egg-info/
test:
	pipenv run py.test
