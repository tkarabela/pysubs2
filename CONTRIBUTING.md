# How to contribute to pysubs2

pysubs2 is an open-source project - your feedback and contributions are welcome! 

## I want to request a feature, report a bug, have a general question

Please open an issue at [GitHub Issues page](https://github.com/tkarabela/pysubs2/issues).

## I want to contribute code

For more substantial patches, please open a [GitHub Issue](https://github.com/tkarabela/pysubs2/issues)
to discuss your proposed changes to make sure we're on the same page and that your patch is a good fit
for the library.

To contribute code, first create a GitHub fork of [tkarabela/pysubs2](https://github.com/tkarabela/pysubs2),
add your commits in a feature branch, and open a pull request against the `master` branch.

If relevant, do not hesitate to add tests demonstrating your feature.
Your branch should pass all tests with no errors or warnings:

```sh
pip install -r requirements-dev.txt
pytest
```

Your branch should also pass Ruff and strict MyPy checks with no errors:

```sh
mypy --strict
ruff check
```
