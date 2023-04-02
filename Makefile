.PHONY: clean all tests build

all: tests build

tests:

build:
	python ./publish.py

clean:
	del *.txt *.json *.png *.csv