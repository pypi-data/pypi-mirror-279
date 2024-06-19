.. _cli_configure:

qbraid configure
=================

Update or add qbraidrc config/credential values.

.. code-block:: bash

    qbraid configure


The qbraid configure command streamlines the setup of your qBraid CLI installation
by allowing you to manage and save frequently used credentials and configurations directly
from your preferred terminal. Upon executing ``qbraid configure``, the CLI will prompt you
for necessary credentials and configuration details. Unless a specific profile is designated,
these details are automatically stored under the ``[default]`` section in your local ``qbraidrc``
file. This file is located in the ``.qbraid`` folder within your home directory.


Examples
---------

.. code-block:: console

    $ qbraid configure
    email [None]: contact@qbraid.com
    api-key [None]: 1234567890


This input will result in the following configuration in ``~/.qbraid/qbraidrc``:


.. code-block:: bash

    [default]
    url = https://api.qbraid.com/api
    email = contact@qbraid.com
    api-key = 1234567890


.. image:: ../_static/api-key.png
    :align: right
    :width: 300px
    :alt: Access key
    :target: javascript:void(0);

Get API key
---------------

To use certain qBraid CLI and `qBraid-SDK <https://docs.qbraid.com/en/latest/sdk/overview.html>`_ features locally (outside of `qBraid Lab <https://docs.qbraid.com/projects/lab/en/latest/lab/overview.html>`_), you must add your account credentials.
Use the following steps to retrieve your API key:

1. Create a qBraid account or log in to your existing account by visiting `account.qbraid.com <https://account.qbraid.com>`_.

2. Copy your API Key token from the left side of your `account page <https://account.qbraid.com>`_.

.. seealso::

    - `qBraid User Guide: Account <https://docs.qbraid.com/projects/lab/en/latest/lab/account.html>`_