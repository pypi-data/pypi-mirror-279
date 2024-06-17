# goshawk

[![Release](https://img.shields.io/github/v/release/ebrassell/goshawk)](https://img.shields.io/github/v/release/ebrassell/goshawk)
[![Build status](https://img.shields.io/github/actions/workflow/status/ebrassell/goshawk/main.yml?branch=main)](https://github.com/ebrassell/goshawk/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/ebrassell/goshawk/branch/main/graph/badge.svg)](https://codecov.io/gh/ebrassell/goshawk)
[![Commit activity](https://img.shields.io/github/commit-activity/m/ebrassell/goshawk)](https://img.shields.io/github/commit-activity/m/ebrassell/goshawk)
[![License](https://img.shields.io/github/license/ebrassell/goshawk)](https://img.shields.io/github/license/ebrassell/goshawk)

SQL Model Management for Humans

- **Github repository**: <https://github.com/ebrassell/goshawk/>
- **Documentation** <https://ebrassell.github.io/goshawk/>

## Getting started with Goshawk

### Installation

We recommend installing with [pipx](https://pipx.pypa.io/stable/)

```bash
pipx install gohawk
```

Or install with pip (you should always use a virtual environment)

```bash
pip install gohawk
```

Verify your installation

```bash
goshawk view-model-tree --schemas-only
```

This will display the DAG of the included sample schema

Set MODELS_PATH env var to the folder containing your models.

```bash
`-- models <-set MODELS_PATH to the path to this folder
     -- mydatabase
         -- schema_1
             -- model_1a.sql
             -- model_1b.sql
         -- schema_2
             -- model_2a.sql
             -- model_2b.sql

export MODELS_PATH=models
```

### Create a dev environemnt

```bash
goshawk init-env [envname]
```

### Test your changes (using your dev environment)

```bash
goshawk deploy-models --test --db-env [envname]
```

### Deploy your changes to your dev environment

```bash
goshawk deploy-models --test --db-env [envname]
```

### Destroy your dev environemnt

```bash
goshawk destroy-env [envname]
```
