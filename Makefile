.PHONY: clean all tests build

all: build

build:
	python ./publish.py

clean:
	del *.txt *.json *.png *.csv