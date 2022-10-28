install:
	pip3 install -r ./requirements.pip

test:
	pytest ./src/tests

lint:
	pylint --recursive=y ./

authen:
	open http://localhost:8080/
	python3 -m flask --app ./src/auth-server/app run -p 8080

run:
	python3 ./src/bot.py
