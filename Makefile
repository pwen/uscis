reqs:
	rm -f requirements*.txt
	pipenv lock -r --dev-only > requirements-dev.txt
	pipenv lock -r > requirements.txt
