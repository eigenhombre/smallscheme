.PHONY: clean all deps pypi-test test install

all: deps test install

test:
	pytest

install:
	python setup.py install

clean:
	rm -rf *.egg-info dist .pytest_cache *.html

pypi-test:
	twine upload -r testpypi dist/*.tar.gz

deps:
	pip install --upgrade pip
	pip install -r requirements.txt

release:
	./bumpver
	python setup.py sdist

