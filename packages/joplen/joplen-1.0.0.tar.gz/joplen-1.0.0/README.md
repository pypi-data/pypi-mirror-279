# README

## Installation

NOTE: `pip install -e .` will only work if you have setuptools v64 or higher and pip version 24 or higher.

```bash
conda create --prefix ./my_env python=3.10
conda activate ./my_env
conda config --set env_prompt '(my_env) '

pip install -r requirements.txt
pip install -e .
```

JAX must be installed manually according to [this link](https://github.com/google/jax/discussions/16380) because the installation is hardware-dependent.
Please follow [these instructions](https://jax.readthedocs.io/en/latest/installation.html) to install JAX.

## Usage

Each module has example usage.
You can run them by executing the module as a script.
Note that single-task JOPLEn is much more modular than the multitask implementation.
This is for practical reasons, but there's no reason it couldn't be made more modular.

```bash
python -m JOPLEn.singletask # single-task joplen
python -m JOPLEn.multitask # multi-task joplen
python -m JOPLEn.competing # Friedman ensemble refitting
```
