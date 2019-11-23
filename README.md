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
  # The server definitions to point domain to folder
  server:
    name: laravelproject.test
    root: Projects/laravel/laravelproject.test/public
```

### Server Definitions

On server config section you must define the server `name` and `root`.

The `name` are the site domain.

The `root` are the folder that contains your site code.
 
E.g.: If your folder structure look like this:   

```
+ laradock
+ Projects
    + site-1
        + laravel-api # This folder contains a laravel API, for example
```

Your `server` definitions section for your project in `Projects.yml` file should look like:

```yaml
server:
    name: laravelapi.test
    root: Projects/site-1/laravel-api/public
```

Don't forget put the domain in your `hosts` file:

```
127.0.0.1  laravelapi.test
``` 

**IMPORTANT:** To the server definitions works correctly, you must assert that:
- Exists only one web server container in your `services` section. You must choose `nginx`, `apache2` or `caddy`.
- If your `services` section has no one web server container nothing will happens.  

## Usage

After configure your projects on `Projects.yml` file you can execute the script
`laradock` passing the project name on first param:

```shell script
./laradock up laravel_project
```

Wait the process finish and your laradock should be started with your chosen
project definitions.

Call the `exec` command to access the `workspace` container:

```shell script
./laradock exec laravel_project
```
