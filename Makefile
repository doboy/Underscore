install:
	python setup.py install

test:
	python setup.py nosetests

coverage:
	python setup.py nosetests --with-coverage --cover-package=underscore --cover-html

