zip: ## builds a zip bundle for qgis
	python3 zip_plugin.py

test:
	@echo "#### Python tests"
	QT_QPA_PLATFORM=offscreen pytest --cov