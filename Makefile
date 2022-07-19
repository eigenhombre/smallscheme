.PHONY: clean all deps pypi-test test install

all: deps test install

venv:
	virtualenv venv

test:
	. venv/bin/activate && pytest

install:
	. venv/bin/activate && python setup.py install

clean:
	rm -rf *.egg-info dist .pytest_cache *.html venv

pypi-test:
	. venv/bin/activate && twine upload -r testpypi dist/*.tar.gz

deps:
	. venv/bin/activate && pip install --upgrade pip
	. venv/bin/activate && pip install -r requirements.txt

release:
	./bumpver
	. venv/bin/activate && python setup.py sdist

