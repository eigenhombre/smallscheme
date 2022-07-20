.PHONY: clean all deps pypi-test test install
.PHONY: lint pypi pypi-test release

all: deps test lint install

deps:
	. venv/bin/activate && pip install --upgrade pip
	. venv/bin/activate && pip install -r requirements.txt

venv:
	virtualenv venv

test:
	. venv/bin/activate && pytest

lint:
	. venv/bin/activate && pycodestyle smallscheme

install:
	. venv/bin/activate && python setup.py install

clean:
	rm -rf *.egg-info dist .pytest_cache *.html venv

pypi-test:
	. venv/bin/activate && twine upload -r testpypi dist/*.tar.gz

pypi:
	. venv/bin/activate && twine upload -r smallscheme dist/*.tar.gz

release:
	./bumpver
	. venv/bin/activate && python setup.py sdist
