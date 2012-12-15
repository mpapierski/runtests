runtests
---------------

Run your tests in multiple configurations!

Specify multiple environment variables, installation and cleanup scripts and *runtests* will automagically run your test script in a configuration matrix!

Just add a configuration file to your repo, and just execute *runtests*.

You may use it in your CI. Just point the "build" script to execute *runtests*. I found this tool quite helpful using my Integrity CI app.

# Example

## Python (.runtests.yml):

	env:
	  - DATABASE_URL: "postgresql://localhost/testdb"
	  - DATABASE_URL: "sqlite://"
	  - DATABASE_URL: "mysql://localhost/testdb"
	before_script:
	  - "virtualenv venv"
	  - "source venv/bin/activate"
	  - "pip install -r requirements.txt"
	after_script:
	  - "rm -rf venv"
	script:
	  - nosetests -v

This configuration will run 3 tests in this order:

	# Test 1
	virtualenv venv
	source venv/bin/activate
	pip install -r requirements.txt
	export DATABASE_URL="postgresql://localhost/testdb"
	nosetests -v
	rm -rf venv	
	export DATABASE_URL="sqlite://"
	# Test 2
	virtualenv venv
	source venv/bin/activate
	pip install -r requirements.txt
	export DATABASE_URL="postgresql://localhost/testdb"
	nosetests -v
	rm -rf venv	
	export DATABASE_URL="mysql://localhost/testdb"
	# Test 3
	virtualenv venv
	source venv/bin/activate
	pip install -r requirements.txt
	export DATABASE_URL="postgresql://localhost/testdb"
	nosetests -v
	rm -rf venv

Run it with:

	runtests -c .runtests.yml

If any of the commands exits with non-zero, the whole build configuration is skipped.

If any of the *scripts* in the matrix exists with non-zero then the whole *runtests* exits with non-zero.

# TODO

- Specify language (Python - automate virtualenv before each test), and versions (py2.5, py2.6, py3.x, etc.).

