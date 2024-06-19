# find-and-replace

Python package and pre-commit-hook for finding and replacing string(s) in file(s).

## Prerequisite

pre-commit install
pre-commit install -t pre-push

The above will make sure precommit will be run automatically on push

## Installation as a pip package

This is an easy to use package which is already available here https://pypi.org/project/find-and-replace-template-commit-check/:

![package to use](./assets/pypi-package.png "Title")

You can install the package via pip:

```bash
pip install find-and-replace-strings
```
In case if you want to use it from the root folder in source:

```
 python -m find_and_replace_strings -h
```

## Usage as a pre commit hook

To use this package, you need to add it to your pre-commit configuration file (.pre-commit-config.yaml). Here's an example:

For config mod

```
repos:
  - repo: https://github.com/opencepk/find-and-replace
    rev: v0.0.1
    hooks:
    - id: find-and-replace-strings
      name: find-and-replace-strings
      description: Find and replace strings
      entry: find-and-replace-strings
      language: python
      pass_filenames: true
      exclude_types:
        - binary
      files: README.md
      verbose: true

```

and for direct mode

```
repos:
  - repo: https://github.com/opencepk/find-and-replace
    rev: v0.0.1
    hooks:
    - id: find-and-replace-strings
      name: find-and-replace-strings
      description: Find and replace strings
      entry: find-and-replace-strings
      language: python
      pass_filenames: true
      exclude_types:
        - binary
      args: ["--find", "search_string", "--replacement", "replacement_string"]
      files: README.md
      verbose: true
```

Please note you also have a choice of
files: '.*\.md$'
or
files: .

In this configuration, the find-and-replace hook is set to read search and replacement strings from a file (.project-properties.json by default which should be defined in the root of the project you want to use this package). You can also specify the search and replacement strings directly in the args field (which is not a suggested way).

## Run tests

```
python -m unittest tests.test_main

```

## How to run it using installed python package

```
  pip install find-and-replace-strings
   find-and-replace --config .find-and-replace.json README1.md README2.md
```

also if you prefer to use a direct mod

```
find-and-replace-strings --find "old_string" --replacement "new_string"  README1.md README2.md
```

## If you need more help with the flags and usage of them

```
find-and-replace-strings -h
usage: find-and-replace-strings [-h] [--config CONFIG] [--find] [--replacement]
                                [files ...]

Perform find and replace operations on one or more target files. By default, the script
reads the search and replacement entries (strings) from a JSON file. You can also
specify the search and replacement strings directly as command line args by setting the
--find "search_string" and --replacement "replacement_string" argument options.

positional arguments:
  files            File(s) on which to perform search and replace

options:
  -h, --help       show this help message and exit
  --config CONFIG  PATH to JSON config file containing find and replacement entries
  --find           String to find in files
  --replacement    String to replace with in files

```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the terms of the MIT license.

## Building and Publishing

To build and publish it to pypi run

```
bash assets/publish.sh
```

## Reference Info

- https://www.gnu.org/prep/standards/html_node/Option-Table.html#Option-Table
- https://setuptools.pypa.io/en/latest/userguide/declarative_config.html
- https://packaging.python.org/guides/distributing-packages-using-setuptools/
- https://autopilot-docs.readthedocs.io/en/latest/license_list.html
- https://pypi.org/classifiers/
