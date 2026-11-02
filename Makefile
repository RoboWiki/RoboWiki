.PHONY: validate test release id

validate:
	python -m pipeline validate

test:
	python -m pytest -q

id:
	python tools/id_registry.py --check

release:
	python tools/export_data.py --out dist
