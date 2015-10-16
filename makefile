test:
	nosetests3
	nosetests

doc:
	cd docs; $(MAKE) html

clean:
	cd docs; $(MAKE) clean
