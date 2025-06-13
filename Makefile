.PHONY: run clean

run: 
	python3 source/simulation/main.py

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -rf {} +

install:
ifeq ($(shell uname),Linux)
	sudo apt update
	sudo apt install -y python3-simpy3
endif
	pip3 install -r requirements.txt
