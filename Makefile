install:
	pip3 install -r ./requirements.pip

test:
	pytest ./src/tests

lint:
	pylint --recursive=y ./
