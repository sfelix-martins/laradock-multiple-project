## Laradock Multiple Env

Script to helps the use of multiple projects on Laradock.

## Pre-requisites

- Python >= 2.7
- [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation)

## Installation

Clone the project inside laradock project folder and access the cloned folder:

```sh
git clone https://github.com/sfelix-martins/laradock-multiple-env.git multiple-env
cd multiple-env
```

## Configuration

Copy the file `Projects.yml.example` to `Projects.yml`:

```sh
cp Projects.yml.example Projects.yml
```

Set your projects configs on `Projects.yml` file.

```yml
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
`upenv` passing the project name on first param:

```sh
./upenv laravel_project
```

Wait the process finish and your laradock should be started with your chosen
project definitions.

**WARNING:** Remember back to laradock root folder to execute other default docker commands. E.g:

```sh
cd ..
docker-compose exec --user=laradock workspace bash
```
