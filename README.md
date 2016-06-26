# gitdl

Download zips of github repositories easily.

## Installation

Clone the repository and cd to it. Then do:
```
$ python setup.py install
```

## Usage

The point of `gitdl` is to quickly get something from GitHub.

### Download a repo with the best match

```
$ gitdl bootstrap
```

This will search for bootstrap, and find the best match and download the
zip for it.

### Download an exact repo

```
$ gitdl -e nvbn/thefuck
```

When `gitdl` is passed with `-e` it expects a {author}/{repo} format to
download the exact repo from GitHub.

### Search for a repo

```
$ gitdl search "intermediate python"
```

This will search GitHub and present the results in a tabular format.

## Development

### Testing

To run the tests:

```
$ py.test
```

To run the tests with coverage:

```
$ py.test --cov
```
