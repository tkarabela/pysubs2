.PHONY: test doc clean build upload installdeps

test:
	pytest
	mypy --strict
	ruff check

doc:
	cd docs; $(MAKE) html

clean:
	cd docs; $(MAKE) clean

build:
	python3 -m build

upload:
	python3 -m twine upload dist/*

installdeps:
	python3 -m pip install --upgrade pip build twine
	python3 -m pip install -r requirements-dev.txt
