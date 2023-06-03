.PHONY: clean all pytest build pylint mypy

all: build

build:
	python ./publish.py
pytest:
	pytest -c pytest.ini
pylint:
	pylint --rcfile .pylintrc ./danielutils/
mypy:
	mypy --config-file mypy.ini ./danielutils/
clean:
	del *.txt *.json *.png *.csv
