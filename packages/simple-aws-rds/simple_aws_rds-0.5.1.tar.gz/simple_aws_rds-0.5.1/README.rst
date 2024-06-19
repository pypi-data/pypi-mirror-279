
.. image:: https://readthedocs.org/projects/simple-aws-rds/badge/?version=latest
    :target: https://simple-aws-rds.readthedocs.io/index.html
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/simple_aws_rds-project/workflows/CI/badge.svg
    :target: https://github.com/MacHu-GWU/simple_aws_rds-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/simple_aws_rds-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/simple_aws_rds-project

.. image:: https://img.shields.io/pypi/v/simple_aws_rds.svg
    :target: https://pypi.python.org/pypi/simple_aws_rds

.. image:: https://img.shields.io/pypi/l/simple_aws_rds.svg
    :target: https://pypi.python.org/pypi/simple_aws_rds

.. image:: https://img.shields.io/pypi/pyversions/simple_aws_rds.svg
    :target: https://pypi.python.org/pypi/simple_aws_rds

.. image:: https://img.shields.io/badge/Release_History!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/simple_aws_rds-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/simple_aws_rds-project

------

.. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: https://simple-aws-rds.readthedocs.io/en/latest/

.. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://simple-aws-rds.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Source_Code-blue.svg
    :target: https://simple-aws-rds.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/simple_aws_rds-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/simple_aws_rds-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/simple_aws_rds-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/simple_aws_rds#files


Welcome to ``simple_aws_rds`` Documentation
==============================================================================
.. image:: https://simple-aws-rds.readthedocs.io/en/latest/_static/simple_aws_rds-logo.png
    :target: https://simple-aws-rds.readthedocs.io/en/latest/

Pythonic AWS RDS boto3 API, for human.

Usage:

.. code-block:: python

    from simple_aws_rds.api import RDSDBInstance, RDSDBSnapshot
    from boto_session_manager import BotoSesManager

    bsm = BotoSesManager()

    # get db instance by id
    db_inst = RDSDBInstance.from_id(bsm, "my-db-identifier")
    # get db instance by tag key value pair, it returns a iter proxy that may have multiple db instance
    db_inst = RDSDBInstance.from_tag_key_value(bsm, key="Env", value="prod").one_or_none()
    db_inst = RDSDBInstance.query(bsm, filters=..., db_instance_identifier=...).all()

    print(db_inst.id)
    print(db_inst.status)
    print(db_inst.instance_class)
    print(db_inst.instance_create_time)
    print(db_inst.engine)
    print(db_inst.engine_version)
    print(db_inst.endpoint)
    print(db_inst.port)
    print(db_inst.hosted_zone_id)
    print(db_inst.vpc_id)
    print(db_inst.subnet_ids)
    print(db_inst.security_groups)
    print(db_inst.availability_zone)
    print(db_inst.publicly_accessible)
    print(db_inst.tags)
    print(db_inst.data)

    print(db_inst.is_available())
    print(db_inst.is_stopped())
    print(db_inst.is_ready_to_start())
    print(db_inst.is_ready_to_stop())


.. _install:

Install
------------------------------------------------------------------------------

``simple_aws_rds`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install simple_aws_rds

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade simple_aws_rds