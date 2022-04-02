#Makefile

install:
	poetry install

build:
	poetry build

publish:
	poetry publish --dry-run

lint:
	poetry run flake8 mc_optimiser

reps:
	poetry show --tree

test:
	poetry run mypy mc_optimiser
	poetry run coverage run -m pytest

coverage:
	poetry run coverage xml

covhtml:
	poetry run coverage run -m pytest
	rm -r htmlcov
	poetry run coverage html
	open htmlcov/index.html

package-install:
	pip3 install --force-reinstall