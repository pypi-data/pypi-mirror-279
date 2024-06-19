.. _cli_devices_list:

qbraid devices list
====================

Get list of qBraid Quantum Devices.

.. code-block:: bash

    qbraid devices list


Examples
---------

Returns list of qBraid device IDs along with corresponding device status.

.. code-block:: console

    $ qbraid devices list
    Device status updated 0 minutes ago

    Device ID                           Status
    ---------                           ------
    aws_oqc_lucy                        ONLINE
    aws_ionq_aria2                      OFFLINE
    aws_rigetti_aspen_m3                ONLINE
    ibm_q_brisbane                      ONLINE
    ...


.. seealso::

    - `qBraid-SDK devices <https://docs.qbraid.com/en/latest/sdk/devices.html>`_
    - `qBraid Lab quantum devices sidebar <https://docs.qbraid.com/projects/lab/en/latest/lab/quantum_devices.html>`_