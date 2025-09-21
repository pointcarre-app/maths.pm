

# Installing Python, the clean way

The following instructions are valid for MacOS and Linux. For Windows, please refer to the specific `pyenv` installation instructions.
{: .pm-subtitle}



[TOC]

## Why installing `Pyenv` ?

> `pyenv` is a tool to manage multiple Python versions, while maintaining a consistent and clean installation process. The source code is available [here](https://github.com/pyenv/pyenv).

**Kind remainder**: it's always a bad idea to interact with the system Python version. Python is used by most of the OS, updating some libraries (or any other operation)might break the system.
{: .alert .alert-warning .alert-soft}

## Installing `pyenv` 

### MacOS

In a terminal, run the following commands: `brew update && brew install pyenv`


### Linux

- Informations about the installation are available on the official [Github page](https://github.com/pyenv/pyenv).
- 💡 Following the [Berkeley tutorial](https://ggkbase-help.berkeley.edu/how-to/install-pyenv/)



## Installing (preferably) `Python 3.13.5` using `pyenv`

- Is is the last stable version as of 2025/06/11. 
- In a terminal, just run: `pyenv install 3.13.5`


## Virtual environment setup


### Create a specific virtual environment with the specified version (in the repo-folder)

```
# Path to installed Python binary
 ~/.pyenv/versions/3.10.1/bin/python -m venv env
```


## Activate / deactivate the virtual environment

```
source env/bin/activate
deactivate
```

## Check correct pip3 used
```
which pip3 
# path should be from the just installed and activated environment
# example: /Users/selim/repos/pca/env/bin/pip3
```

## Install requirements

```
pip3 install -r requirements.txt
```