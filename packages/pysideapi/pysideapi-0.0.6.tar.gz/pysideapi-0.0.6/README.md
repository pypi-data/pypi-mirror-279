pysideapi
===================================

`Py Side Api` is a python library of data pipelines that generates customer relevant notifications based on their
account movements and balance. It uses [pipeforge](https://globaldevtools.bbva.com/bitbucket/projects/KZDJA/repos/aif_pipeforge/browse) framework.

A settings file and table definitions file are needed for executing relevant_facts:
* Settings example: can be found at `tests.settings.testing.py` in this repository.
* Table definitions example: can be found at `tests.settings.tables.datio.py` in this repository.

The settings file is configured by an environment variable:

```bash
export PF_SETTINGS = 'tests.settings.testing'
````

The setting `TABLES_SETTINGS` point to table definition file module.

Modules
--------

* `jira`: module that defines tasks to be executed by dataproc jobs and return codes.
* `dictionary`: module that contains some small ML models integrated in relevant facts as names detector model.
* `dictamen`: this module includes some notebooks with code examples of using relevant_facts library.

HOW TO USE IT LOCALLY
---------------------

Dataproc PySpark projects use [Kaa](https://globaldevtools.bbva.com/bitbucket/projects/PRDSS/repos/python_workflow_library/browse) library for workflow purposes.

The proposed Python workflow consists of the following stages:

1. Dependencies installation.
2. Tests with coverage support.
3. Linter.
4. Artifact generation.

All of the stages listed above are accessible through a custom script named `kaa`.

### Environment set up

Export the following variables:
