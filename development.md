

## Deploy to pypi

```bash
$ rm -rf dist/
$ python setup.py clean sdist bdist_wheel
$ twine upload dist/*
```

