.. _cli:

qbraid
=======

A qBraid CLI command has the following structure:

.. code-block:: console

   $ qbraid <command> <subcommand> [options and parameters]

For example, to list installed environments, the command would be:

.. code-block:: console

   $ qbraid envs list

To view help documentation, use one of the following:

.. code-block:: console

   $ qbraid help
   $ qbraid <command> help
   $ qbraid <command> <subcommand> help


To get the version of the qBraid CLI:

.. code-block:: console

   $ qbraid --version


Commands
---------

+---------------------------------------+---------------------------------------------------+
| ``qbraid configure``                  | Update or add qbraidrc config values.             |
+---------------------------------------+---------------------------------------------------+
| ``qbraid credits``                    | Get number of qBraid credits remaining            |
+---------------------------------------+---------------------------------------------------+

.. toctree::
   :maxdepth: 1

   configure
   credits

Subgroups
----------
+---------------------------------------+---------------------------------------------------+
| ``qbraid envs``                       | Manage qBraid environments.                       |
+---------------------------------------+---------------------------------------------------+
| ``qbraid kernels``                    | Manage qBraid kernels.                            |
+---------------------------------------+---------------------------------------------------+
| ``qbraid devices``                    | Manage qBraid Quantum Devices.                    |
+---------------------------------------+---------------------------------------------------+
| ``qbraid jobs``                       | Manage qBraid Quantum Jobs.                       |
+---------------------------------------+---------------------------------------------------+


.. toctree::
   :maxdepth: 1

   envs
   kernels
   devices
   jobs