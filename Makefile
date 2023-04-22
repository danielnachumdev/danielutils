.PHONY: clean all test build

all: build

build:
	python ./publish.py
test:
	pytest
	pylint ./danielutils/
clean:
	del *.txt *.json *.png *.csv
