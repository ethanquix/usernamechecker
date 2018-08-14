all: re

gen:
		rm -rf dist
		python setup.py sdist bdist_wheel

upload:
		twine upload dist/*

install:
		pip install dist/*.whl --upgrade

clean:
		rm -rf build
		rm -rf dist
		rm -rf usercheck.egg-info/

re:	clean gen

check:
	python setup.py check -r -s
