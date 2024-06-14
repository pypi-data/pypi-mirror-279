
.. .. image:: https://readthedocs.org/projects/simple_aws_ec2/badge/?version=latest
    :target: https://simple_aws_ec2.readthedocs.io/index.html
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/simple_aws_ec2-project/workflows/CI/badge.svg
    :target: https://github.com/MacHu-GWU/simple_aws_ec2-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/simple_aws_ec2-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/simple_aws_ec2-project

.. image:: https://img.shields.io/pypi/v/simple_aws_ec2.svg
    :target: https://pypi.python.org/pypi/simple_aws_ec2

.. image:: https://img.shields.io/pypi/l/simple_aws_ec2.svg
    :target: https://pypi.python.org/pypi/simple_aws_ec2

.. image:: https://img.shields.io/pypi/pyversions/simple_aws_ec2.svg
    :target: https://pypi.python.org/pypi/simple_aws_ec2

.. image:: https://img.shields.io/badge/Release_History!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/simple_aws_ec2-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/simple_aws_ec2-project

------


.. .. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: https://simple_aws_ec2.readthedocs.io/index.html

.. .. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://simple_aws_ec2.readthedocs.io/py-modindex.html

.. .. image:: https://img.shields.io/badge/Link-Source_Code-blue.svg
    :target: https://simple_aws_ec2.readthedocs.io/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/simple_aws_ec2-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/simple_aws_ec2-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/simple_aws_ec2-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/simple_aws_ec2#files


Welcome to ``simple_aws_ec2`` Documentation
==============================================================================
Simple AWS EC2 dev tool.

Requires Python3.7+

Usage:

.. code-block:: python

    import boto3
    from simple_aws_ec2.api import Ec2Instance, Image

    ec2_client = boto3.client("ec2")

    # get ec2 by id
    ec2_inst = Ec2Instance.from_id(ec2_client, "i-1a2b3c")
    # get ec2 by running code from inside of ec2
    ec2_inst = EC2Instance.from_ec2_inside(ec2_client)
    # get ec2 by it's name, it returns a iter proxy that may have multiple ec2
    ec2_inst = EC2Instance.from_ec2_name(ec2_client, "my-server").one_or_none()
    # get ec2 by tag key value pair, it returns a iter proxy that may have multiple ec2
    ec2_inst = EC2Instance.from_tag_key_value(ec2_client, key="Env", value="prod").one_or_none()
    ec2_inst = EC2Instance.query(ec2_client, filters=..., instnace_ids=...).all()

    print(ec2_inst.id)
    print(ec2_inst.status)
    print(ec2_inst.public_ip)
    print(ec2_inst.private_ip)
    print(ec2_inst.vpc_id)
    print(ec2_inst.subnet_id)
    print(ec2_inst.security_groups)
    print(ec2_inst.image_id)
    print(ec2_inst.instance_type)
    print(ec2_inst.key_name)
    print(ec2_inst.tags)
    print(ec2_inst.data)

    print(ec2_inst.is_running()
    print(ec2_inst.is_stopped()
    print(ec2_inst.is_pending())
    print(ec2_inst.is_shutting_down()
    print(ec2_inst.is_stopping()
    print(ec2_inst.is_terminated()

    print(ec2_inst.is_ready_to_start()
    print(ec2_inst.is_ready_to_stop()

    ec2_inst.start_instance()
    ec2_inst.stop_instance()
    ec2_inst.terminate_instance()

    # the following methods has to be called on a running ec2 instance
    # it use the EC2 metadata api
    # https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instancedata-data-retrieval.html
    print(EC2Instance.get_ami_id())
    print(EC2Instance.get_instance_id())
    print(EC2Instance.get_instance_type())
    print(EC2Instance.get_local_hostname())
    print(EC2Instance.get_local_ipv4())
    print(EC2Instance.get_public_hostname())
    print(EC2Instance.get_public_ipv4())
    print(EC2Instance.get_security_groups()

    # AMI Image API
    image = Image.from_id(ec2_client, "ami-1a2b3c")
    image = Image.from_ec2_inside(ec2_client)

    image_list = Image.query(ec2_client).all()

    image_list = Image.query(ec2_client, owners=["self"]).all()

    print(image.image_type_is_machine())
    print(image.image_type_is_kernel())
    print(image.image_type_is_ramdisk())
    print(image.is_pending())
    print(image.is_available())
    print(image.is_invalid())
    print(image.is_deregistered())
    print(image.is_transient())
    print(image.is_failed())
    print(image.is_error())
    print(image.image_root_device_type_is_ebs())
    print(image.image_root_device_type_is_instance_store())
    print(image.image_virtualization_type_is_hvm())
    print(image.image_virtualization_type_is_paravirtual())
    print(image.image_boot_mode_is_legacy_bios())
    print(image.image_boot_mode_is_uefi())
    print(image.image_boot_mode_is_uefi_preferred())

    image = Image.from_image_name(ec2_client, "my-image").all()

    image_list = Image.from_tag_key_value(ec2_client, key="Env", value="dev").all()

    image.deregister()


.. _install:

Install
------------------------------------------------------------------------------

``simple_aws_ec2`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install simple_aws_ec2

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade simple_aws_ec2