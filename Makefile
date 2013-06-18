PY ?= python
SRC_PATH ?= underscore/
TEST_PATH ?= tests/
PYTHONPATH:=$(TEST_PATH):$(SRC_PATH):$(PYTHONPATH)

install: clean
	env PYTHONPATH=$(PYTHONPATH) $(PY) setup.py install

test: clean
	env PYTHONPATH=$(PYTHONPATH) $(PY) setup.py nosetests

coverage: clean
	env PYTHONPATH=$(PYTHONPATH) $(PY) setup.py nosetests --with-coverage --cover-package=underscore --cover-html

clean:
	find . -name "*pyc" -delete
