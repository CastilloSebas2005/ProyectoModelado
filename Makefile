run: 
	python3 source/simulation/main.py

runSlow:
	python3 source/simulation/main.py --duration 50 --slow --sleeptime 0.5 --runs 2

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -rf {} +

install:
ifeq ($(shell uname),Linux)
	sudo apt update
	sudo apt install -y python3-simpy3
	sudo apt install -y python3-numpy
	sudo apt install -y python3-scipy
else #for windows or other O.S
	pip3 install -r source/requirements.txt
endif
