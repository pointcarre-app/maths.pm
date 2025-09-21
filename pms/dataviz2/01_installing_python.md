

# Installing Python, the clean way

The following instructions are valid for MacOS and Linux. For Windows, please refer to the specific `pyenv` installation instructions.
{: .pm-subtitle}



[TOC]

## Why installing `Pyenv` ?

> `pyenv` is a tool to manage multiple Python versions, while maintaining a consistent and clean installation process. The source code is available [here](https://github.com/pyenv/pyenv).


> `conda` is a tool that we don't recommend to use, as it's more complex to manage than `pyenv`.

**Kind remainder**: it's always a bad idea to interact with the system Python version. Python is used by most of the OS, updating some libraries (or any other operation)might break the system.
{: .alert .alert-warning .alert-soft}

## Installing `pyenv` 

### MacOS

In a terminal, run the following commands: 

```bash
brew update
brew install pyenv
```


### Linux

- ℹ️ **FYI:** Informations about the installation available on the official [Github page](https://github.com/pyenv/pyenv).
- 💡 **Recommendation:** Following the [Berkeley tutorial](https://ggkbase-help.berkeley.edu/how-to/install-pyenv/)



### Windows

Use the `pyenv-win` installer. The instructions are available on Github, in the [repository page](https://github.com/pyenv-win/pyenv-win).

### After the OS specific installation



- A folder at root level named `.pyenv` should have been created
- To refer this folder you, can use `~/.pyenv` (**and you should**)



## `Python 3.13.5` using `pyenv`

> It's preferable to install this version, as it's important for the students to use the same version as the one used in the course, in particular, using different versions in the same course could lead to unexpected errors and issues, **with the risk of being very time consuming to solve**. If **you're very familiar** with Python installation and version management, feel free to do as you're used to.

`3.13.5` is the last stable version as of 2025/06/11.  In a terminal, just run: 

```bash
pyenv install 3.13.5
```




Nevertheless, independently of your easy with Python installation, you should use a version statisfying `>=3.12`, and preferably `>=3.13`. **Not following those rules could lead to unexpected errors and issues, with the risk of being very time consuming to solve.**
{: .alert .alert-warning .alert-soft}


## Virtual environment setup


### Folder creation

- Create a new folder for the virtual environment and `cd` into it. In this example, the folder is called `dataviz-course`.



```bash
 mkdir dataviz-course
 cd dataviz-course
```


### Creating the virtual environment

- We will create a specific virtual environment with the specified version in the `dataviz-course` folder. 
- The trick is that we will use an absolute path to the python binary to create the virtual environment: therefore there cannot be any ambiguity about the interpreter used to create the virtual environment.
- The newly created environment will be called `env` and created thank to the built-in `venv` module.

> This usage of absolute path is 100% consistent with *The Zen of Python*: *In the face of ambiguity, refuse the temptation to guess.*


```bash
# Creating the virtual environment
# using the absolute path to the python binary
# that we previously installed with Python
 ~/.pyenv/versions/3.15.3/bin/python -m venv env
```


## Interacting with the virtual environment


The two following commands should be run from the folder containing the virtual environment, i.e. containing the `env` folder.
{: .alert .alert-success .alert-soft}

### Activating the virtual environment


```bash
source env/bin/activate
```


### Deactivating the virtual environment

```bash
deactivate
```


## Check correct `pip3` / `pip` / `python3` / `python` are used

- You should run those command from the folder containing the virtual environment, i.e. containing the `env` folder, after activating the virtual environment.

```bash
which pip3 
# path should be from the just installed and activated environment
# example: /Users/elliot/repos/dataviz-course/env/bin/pip3
```


- Also for an extra security: 

```bash
which pip
# path should be from the just installed and activated environment
# example: /Users/elliot/repos/dataviz-course/env/bin/pip
```

- Still a bit more of extra security:

```bash
which python3
# path should be from the just installed and activated environment
# example: /Users/elliot/repos/dataviz-course/env/bin/python3
```


- Finally, because *Defensive programming* is our best friend:


```bash
which python3
# path should be from the just installed and activated environment
# example: /Users/elliot/repos/dataviz-course/env/bin/python3
```



## Install requirements

```bash
pip3 install -r requirements.txt
```