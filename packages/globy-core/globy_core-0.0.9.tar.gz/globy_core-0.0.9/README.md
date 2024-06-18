# Globy Core

### Building the package
```bash
python3 -m build .
```

### Publishing the package to Globy artifactory ("globy-dev")
```bash
python3 -m twine upload -r globy-dev dist/*
```

### Updating the Globy core package in your python environment
```bash
pip install --upgrade globy-core --index-url http://localhost:8080
```

### Upgrading locally
```bash
pip install globy_core-0.0.6-py3-none-any.whl  --upgrade
```
