test:
	nosetests-3.4
	nosetests-2.7

doc:
	cd docs; $(MAKE) html

clean:
	cd docs; $(MAKE) clean
