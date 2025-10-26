

# Installing Python, the clean way

We'll focus on `pyenv` for python version management. The following instructions are valid for MacOS and Linux. For Windows, please refer to the specific `pyenv` installation instructions.
{: .pm-subtitle}



[TOC]





## Installing `pyenv` 


### Why install `pyenv`?

> `pyenv` is a tool to manage multiple Python versions, while maintaining a consistent and clean installation process. The source code is available [here](https://github.com/pyenv/pyenv).


> `conda` is a tool that we do not recommend to use, as it is more complex to manage than `pyenv`.

**Kind reminder**: it is always a bad idea to interact with the system Python version. Python is used by most of the OS, updating some libraries (or any other operation) might break the system.
{: .alert .alert-warning .alert-soft}


### MacOS

In a terminal, run the following commands: 

```bash
brew update
brew install pyenv
```


### Linux

- ℹ️ **FYI:** Information about the installation available on the official [Github page](https://github.com/pyenv/pyenv).
- 💡 **Recommendation:** Following the [Berkeley tutorial](https://ggkbase-help.berkeley.edu/how-to/install-pyenv/)



### Windows

Use the `pyenv-win` installer. The instructions are available on Github, in the [repository page](https://github.com/pyenv-win/pyenv-win).

### After the OS specific installation



- A folder at root level named `.pyenv` should have been created
- To refer to this folder, you can use `~/.pyenv` (**and you should**)



## `Python 3.13.5` using `pyenv`

> It is preferable to install this version, as it is important for the students to use the same version as the one used in the course, in particular, using different versions in the same course could lead to unexpected errors and issues, **with the risk of being very time consuming to solve**. If **you are very familiar** with Python installation and version management, feel free to do as you are used to.

`3.13.5` is the latest stable version as of 2025/06/11.  In a terminal, just run: 

```bash
pyenv install 3.13.5
```




Nevertheless, independently of your ease with Python installation, you should use a version satisfying `>=3.12`, and preferably `>=3.13`. **Not following those rules could lead to unexpected errors and issues, with the risk of being very time consuming to solve.**
{: .alert .alert-warning .alert-soft}


## Virtual env setup (UNIX based OS)


We'll rely on the built-in `venv` module to create a virtual environment. The following instructions are valid for UNIX based OS (such as MacOS and Linux). If you use Windows, please refer to the [specific instructions](https://docs.python.org/3/library/venv.html) from the official Python documentation.

### Folder creation

- Create a new folder for the virtual environment and `cd` into it. In this example, the folder is called `dataviz-course`.


```bash
 mkdir dataviz-course
 cd dataviz-course
```


### Creating the virtual environment

- We will create a specific virtual environment with the specified version in the `dataviz-course` folder. 
- The trick is that we will use an absolute path to the python binary to create the virtual environment: therefore there cannot be any ambiguity about the interpreter used to create the virtual environment.
- The newly created environment will be called `env` and created thanks to the built-in `venv` module.

> This usage of absolute path is 100% consistent with *The Zen of Python*: *In the face of ambiguity, refuse the temptation to guess.*


```bash
# Creating the virtual environment
# using the absolute path to the python binary
# that we previously installed with pyenv
 ~/.pyenv/versions/3.13.5/bin/python -m venv env
```


## Interacting with the virtual env


The two following commands should be run from the folder containing the virtual environment, i.e. containing the `env` folder.
{: .alert .alert-success .alert-soft}

### Activating the virtual env


```bash
source env/bin/activate
```


### Deactivating the virtual env

```bash
deactivate
```


## Aliases & defensive programming

You should run these commands from the folder containing the virtual environment, i.e. containing the `env` folder, after activating the virtual environment. The goal is to ensure that the correct `pip3` / `pip` / `python3` / `python` are used (i.e. that the aliases are correct).


### Is `pip3` alias correct ?

```bash
which pip3 
# path should be from the just installed and activated environment
# example: /Users/elliot/repos/dataviz-course/env/bin/pip3
```

### Is `pip` alias correct ?

Also for an extra security: 

```bash
which pip
# path should be from the just installed and activated environment
# example: /Users/elliot/repos/dataviz-course/env/bin/pip
```

### Is `python3` alias correct ?

Still a bit more of extra security:

```bash
which python3
# path should be from the just installed and activated environment
# example: /Users/elliot/repos/dataviz-course/env/bin/python3
```


### Is `python` alias correct ?

Finally, because *Defensive programming* is our best friend:


```bash
which python
# path should be from the just installed and activated environment: this was the last one!
# example: /Users/elliot/repos/dataviz-course/env/bin/python
```



## Installing JupyterLab globally


We'll install JupyterLab globally so it's available across all projects (also because it's easier to manage).

### MacOS

```bash
brew install jupyterlab
```

### Linux

Below, different instructions for different Linux distributions are listed. Using Ubuntu, we recommend to use the 2️⃣ method.
{: .alert .alert-warning .alert-soft}

1️⃣ Using pip with the pyenv-managed Python:

```bash
~/.pyenv/versions/3.13.5/bin/pip install jupyterlab
```

2️⃣ Alternatively, on Ubuntu/Debian:

```bash
sudo apt update
sudo apt install python3-pip
pip3 install --user jupyterlab
```

3️⃣ On Fedora/RHEL/CentOS:

```bash
sudo dnf install python3-pip
pip3 install --user jupyterlab
```

### Windows

We recommend following the instructions from the [official repository](https://github.com/jupyterlab/jupyterlab-desktop). Also the official JupyterLab installation documentation for version `4.4.x` is available [here](https://jupyterlab.readthedocs.io/en/stable/install/installation.html) (last stable version as of 2024/09/15).

## Register the virtual env

**We need to register the virtual environment with JupyterLab to be able to use it in JupyterLab.**

### Ensuring we are in the correct folder

**You need to access the folder containing the virtual environment, i.e. containing the `env` folder, after activating the virtual environment.**

```bash
# Make sure to be in the folder containing the virtual environment
# by running the following command:
cd dataviz-course
```

### Activating the virtual environment

```bash
# Make sure your virtual environment is activated 
# by running the following command:
source env/bin/activate
```

### Installing `ipykernel`


```bash
# Install `ipykernel`
pip3 install ipykernel==6.30.1
```


### Registering the virtual environment with JupyterLab

```bash
# Register the environment as a kernel
python -m ipykernel install --user --name=env --display-name="dataviz-env"
```



After installing `ipykernel` in your virtual environment, register it as a kernel for JupyterLab:
Now you can start JupyterLab from anywhere and select the `dataviz-env` kernel to use your project's virtual environment.

```bash
# Start JupyterLab 
jupyter lab 
```

This command should also work:

```bash
jupyter-lab
```



## Installing the libraries for the course

**Make sure to be in the folder containing the virtual environment, i.e. containing the `env` folder, after activating the virtual environment.**

```bash
# ensuring to be in the correct folder
cd dataviz-course
# activating the virtual environment
source env/bin/activate
# installing the libraries
pip3 install matplotlib==3.10.5
pip3 install ipykernel==6.30.1
pip3 install numpy==2.3.2
pip3 install pandas==2.3.2
pip3 install bokeh==3.8.0
pip3 install geopandas==1.1.1
pip3 install statsmodels==0.14.5
```


