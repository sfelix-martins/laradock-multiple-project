## Laradock Multiple Env

Script to helps the use of multiple projects on Laradock.

![](https://github.com/sfelix-martins/laradock-multiple-env/workflows/Python%20package/badge.svg)

## Pre-requisites

- Python >= 2.7
- [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation)

## Installation

Clone the project inside laradock project folder and access the cloned folder:

```shell script
git clone https://github.com/sfelix-martins/laradock-multiple-env.git multiple-env
cd multiple-env
```

Install the project dependencies from `requirements.txt`:

```shell script
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Configuration

Copy the file `Projects.yml.example` to `Projects.yml`:

```shell script
cp Projects.yml.example Projects.yml
```

Set your projects configs on `Projects.yml` file.

```yaml
# Project name
laravel_project:
  # Environment vars that will override the `.env` vars from laradock
  env:
    - PHP_VERSION: 7.3
  # The containers that will be executed
  services:
    - nginx
    - mysql
    - mailhog
```

## Usage

After configure your projects on `Projects.yml` file you can execute the script
`laradock` passing the project name on first param:

```shell script
./laradock up laravel_project
```

Wait the process finish and your laradock should be started with your chosen
project definitions.

**WARNING:** Remember back to laradock root folder to execute other default docker commands. E.g:

```shell script
cd ..
docker-compose exec --user=laradock workspace bash
```
