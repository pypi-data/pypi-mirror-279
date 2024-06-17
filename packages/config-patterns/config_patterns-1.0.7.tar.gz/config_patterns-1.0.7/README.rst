
.. .. image:: https://readthedocs.org/projects/config_patterns/badge/?version=latest
    :target: https://config_patterns.readthedocs.io/index.html
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/config_patterns-project/actions/workflows/main.yml/badge.svg
    :target: https://github.com/MacHu-GWU/config_patterns-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/config_patterns-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/config_patterns-project

.. image:: https://img.shields.io/pypi/v/config_patterns.svg
    :target: https://pypi.python.org/pypi/config_patterns

.. image:: https://img.shields.io/pypi/l/config_patterns.svg
    :target: https://pypi.python.org/pypi/config_patterns

.. image:: https://img.shields.io/pypi/pyversions/config_patterns.svg
    :target: https://pypi.python.org/pypi/config_patterns

.. image:: https://img.shields.io/pypi/dm/config_patterns.svg
    :target: https://pypi.python.org/pypi/config_patterns

.. image:: https://img.shields.io/badge/release_history!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/config_patterns-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/config_patterns-project

------

.. .. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: https://config_patterns.readthedocs.io/index.html

.. .. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://config_patterns.readthedocs.io/py-modindex.html

.. .. image:: https://img.shields.io/badge/Link-Source_Code-blue.svg
    :target: https://config_patterns.readthedocs.io/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/config_patterns-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/config_patterns-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/config_patterns-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/config_patterns#files


Welcome to ``config_patterns`` Documentation
==============================================================================
.. image:: https://github.com/MacHu-GWU/config_patterns-project/assets/6800411/0cfdeee0-6740-4522-b2e9-a17e51facba9

``config_patterns`` is a Python library that brings config management best practices for production-ready application.

1. `Hierarchy Json Pattern for Config Management <https://github.com/MacHu-GWU/config_patterns-project/blob/main/example/separate_and_merge_non_sesitive_and_sensitive_data_example.ipynb>`_: allows you to define a hierarchy structure of your config data model, and inherit global config values if a specific config value is not defined.
2. `Separate and Merge Non-Sensitive Data and Secret Data <https://github.com/MacHu-GWU/config_patterns-project/blob/main/example/separate_and_merge_non_sesitive_and_sensitive_data_example.ipynb>`_: allows you to manage non-sensitive config data and sensitive config data separately and merge them together.
3. `Multi Environment Json <https://github.com/MacHu-GWU/config_patterns-project/blob/main/example/multi_env_json/multi_environment_config.ipynb>`_: allows you to manage configs for multi-environment deployment application.
4. `Multi Environment Config Management - SSM Backend <https://github.com/MacHu-GWU/config_patterns-project/blob/main/example/multi_env_json/multi_environment_config_with_ssm_backend.ipynb>`_: a production ready solution using AWS Parameter Store as the backend for multi-environment config management.
5. `Multi Environment Config Management - S3 Backend <https://github.com/MacHu-GWU/config_patterns-project/blob/main/example/multi_env_json/multi_environment_config_with_s3_backend.ipynb>`_: a production ready solution using AWS S3 as the backend for multi-environment config management.

.. _install:

Install
------------------------------------------------------------------------------

``config_patterns`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install config_patterns

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade config_patterns
