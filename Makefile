install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt
lint:
	pylint --disable=R,C example.py src

test:
	python -m pytest -vv --cov tests
