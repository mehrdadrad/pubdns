.PHONY: docs

DEPS = \
	dnspython \
	requests \
	flake8 \
	mock \
	setuptools \
	sphinx \
	twine \
	detox \

test:
	detox

setup-dev-env:
	pip install --upgrade $(DEPS)

flake8:
	flake8 --ignore=F401 ./pubdns

publish:
	python setup.py sdist --formats=gztar
	twine upload dist/*
	rm -fr build dist .egg requests.egg-info

docs:
	cd docs && make html
