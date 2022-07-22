.PHONY: clean all deps pypi-test test install
.PHONY: lint pypi pypi-test release

all: deps develop test lint

deps:
	. venv/bin/activate && pip install --upgrade pip
	. venv/bin/activate && pip install -r requirements.txt

venv:
	virtualenv venv

test:
	. venv/bin/activate && pytest -s
	. venv/bin/activate && ./smallscheme/main.py fact.scm
	. venv/bin/activate && ./smallscheme/main.py -t tests.scm

lint:
	. venv/bin/activate && pycodestyle smallscheme

develop:
	. venv/bin/activate && python setup.py develop

clean:
	rm -rf *.egg-info dist .pytest_cache *.html venv

pypi-test:
	. venv/bin/activate && twine upload -r testpypi dist/*.tar.gz

pypi:
	. venv/bin/activate && twine upload -r smallscheme dist/*.tar.gz

pip-docker-test:
	docker build -t smallscheme-pip-test -f Dockerfile.piptest .

build-docker-test:
	docker build -t smallscheme -f Dockerfile.build .

alltests: test lint build-docker-test

release:
	./bumpver
	. venv/bin/activate && python setup.py sdist
