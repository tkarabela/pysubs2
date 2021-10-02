test:
	pytest

doc:
	cd docs; $(MAKE) html

clean:
	cd docs; $(MAKE) clean
