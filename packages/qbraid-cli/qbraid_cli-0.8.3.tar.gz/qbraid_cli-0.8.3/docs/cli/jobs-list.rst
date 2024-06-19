.. _cli_jobs_list:

qbraid jobs list
=================

Get list of qBraid Quantum Jobs.

.. code-block:: bash

    qbraid jobs list


Examples
---------

Returns list of qBraid job IDs along with corresponding job status.

.. code-block:: console

    $ qbraid jobs list
    Displaying 10 most recent jobs:

    Job ID                                              Submitted                  Status
    ------                                              ---------                  ------
    aws_oqc_lucy-exampleuser-qjob-zzzzzzz...            2023-05-21T21:13:47.220Z   QUEUED
    ibm_q_oslo-exampleuser-qjob-xxxxxxx...              2023-05-21T21:13:48.220Z   RUNNING
    ...


.. seealso::

    - :ref:`qbraid jobs enable<cli_jobs_enable>`
    - :ref:`qbraid jobs disable<cli_jobs_disable>`
    - `qBraid-SDK jobs <https://docs.qbraid.com/en/latest/sdk/jobs.html>`_
    - `qBraid Lab quantum jobs <https://docs.qbraid.com/projects/lab/en/latest/lab/quantum_jobs.html>`_