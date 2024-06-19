***************
The Scotty tool
***************

Scotty
======

``SimpleCore™ open technology tool for you`` or short ``Scotty`` is a tool used to
operate with the SimpleCore™ BSP, helping to download sources and build BSP images. It
relies on docker to provide a reproducible build environment.

``Scotty`` can either be used as a single command to build a full image or as a
helper to setup Yocto sources and open a shell with a Yocto environment.

Getting started
---------------

The scotty tool relies on a docker container to embed as much as possible the
software dependencies it relies on. As a consequence, you will need to make sure
to install `Docker<https://www.docker.com/>` on your system and make sure your
user has rights to use docker.
The scotty tool also needs `OpenSSL<https://www.openssl.org/>` to function properly.

On Ubuntu 20.04 platforms, they can be installed with following commands::

    $ sudo apt install docker.io openssl
    $ sudo gpasswd -a ${USER} docker

In addition, if you plan to use QEMU images, it is advised to make sure the
current user is able to use `KVM <https://www.linux-kvm.org/page/Main_Page>`_,
having write permissions to ``/dev/kvm``. On Ubuntu 20.04, this can be done by
adding your user to the ``kvm`` group, with the following command::

    $ sudo gpasswd -a ${USER} kvm

.. note::
    After adding your user to the docker or kvm group with the ``gpasswd``
    command, you will need to open a new session to apply your new privileges.

Installing the scotty tool can be easily done with ``pip``

.. code:: shell

  pip install --user avnet-scotty

upgrading an existing installation can be done with

.. code:: shell

  pip install --user --upgrade avnet-scotty

.. important::

  On Ubuntu 20.04 you might be affected by `this bug <https://bugs.launchpad.net/ubuntu/+source/bash/+bug/1588562>`_,
  so ``${HOME}/.local/bin`` is not part of the standard search path.

  This can be fixed by running

  .. code-block:: console

    echo 'export PATH="$(systemd-path user-binaries):$PATH"' >> ~/.bashrc

  .. note::

    A reboot is required for the setting to become effective.

  You can also install ``scotty`` with

  .. code-block:: console

    sudo pip install avnet-scotty

  but that requires you to have ``sudo`` rights on your system.


Alternatively, the current development version can be obtained by cloning
`<https://github.com/avnet-embedded/simplecore-tools>`_.

.. admonition:: Potential pitfall
  :class: ATTENTION

  If you are facing the following issue

  .. code-block:: text

    Error response from daemon: Head "https://ghcr.io/v2/avnet-embedded/scotty/manifests/2023.10": denied: denied
    scotty failed on line 157
  
  please run

  .. code-block:: console

    docker logout ghcr.io

  on your computer.

  To fix it permantely, please create a personal access token, as described at :ref:`sources/simplecore-distro/docs/simpleswitch/tutorial-base-images/container-helper/ghcr:Github container registry (GHCR)`
  with at least ``read:packages`` permissions.

  And re-login to docker using

  .. code-block:: console

    docker login ghcr.io

Github preparations
^^^^^^^^^^^^^^^^^^^

Before we can start to build, we need to make sure that Github allows us to connect via ssh.

See this video on how to do it

.. youtube:: s6KTbytdNgs

Please also keep in mind that most of the repositories are only available for users being
part of `avnet-embedded GitHub organization <https://github.com/avnet-embedded>`_.

Please reach out to support to request access.

Running scotty on a different docker image
------------------------------------------

By default scotty will use the corresponding version of the `scotty docker image <https://github.com/orgs/avnet-embedded/packages/container/package/scotty>`_.
To use a different docker image run::

  $ SCOTTY_DOCKER_IMAGE=<image> scotty ...

e.g. to use the latest development version::

  $ SCOTTY_DOCKER_IMAGE="ghcr.io/avnet-embedded/simplecore-tools:kirkstone" scotty ...

to use a different release::

  $ SCOTTY_DOCKER_IMAGE="ghcr.io/avnet-embedded/scotty:<release tag>" scotty ...

Scotty subcommands
------------------

Several commands are supported by Scotty, with different goals:
  - ``update``: download or update the Yocto sources. Will be triggered
    implicitly with default parameters if no sources are found.
  - ``setup``: Setup the build directory. Will be triggered implicitly with
    default parameters if the build directory has not been setup.
  - ``bitbake``: Build a Yocto target.
  - ``shell``: Run a shell in the Yocto build environment.
  - ``command``: Run a command in the Yocto build environment.
  - ``docker-update``: Update Scotty build container.
  - ``info``: Print out information.

Setup your build
----------------

With

.. code-block:: bash

   $ scotty setup

you can configure your build through our interactive UI.

.. note::

  .. code-block:: bash

    $ scotty setup --force

  Will allow you to redo the configuration at any point.


Building a full image
---------------------

A single command is enough to download the sources and build an image:

.. code-block:: bash

   $ scotty bitbake core-image-minimal

Built images can then be found in ``build/build/tmp/deploy/images/``.

The build target can be customized:

.. code-block:: bash

   $ scotty bitbake core-image-minimal
   $ scotty bitbake -- core-image-minimal -c populate_sdk

.. note::

  The available images/SDKs can be displayed by running

  .. code-block:: bash

    $ scotty info images

Recommended hardware setup
^^^^^^^^^^^^^^^^^^^^^^^^^^

For building software pacakges with ``Scotty`` we recommend the following minimal hardware setup:

For base images

- 4 Cores / 8 threads CPU
- 16GB RAM
- 200GB HDD

For SDKs

- 16 Cores / 32 threads CPU
- 64Gb RAM
- 500GB HDD

.. note::

  Other combinations do work as well, but keep in mind that we at least require 2GB of RAM per available CPU thread.

Using Scotty as a helper
------------------------

``Scotty`` can be used to open a shell with a sourced Yocto environment:

.. code-block:: bash

   $ scotty shell

It can also be used to run a single command without opening a shell:

.. code-block:: bash

   # This is equivalent to scotty bitbake core-image-minimal
   $ scotty command bitbake core-image-minimal

   $ scotty command bitbake-layers show-appends

Updating sources
----------------

Scotty will not modify downloaded sources by itself after the initial setup.
Building an image with up-to-date sources can be done using following commands:

.. code-block:: bash

   $ scotty update
   $ scotty bitbake core-image-minimal

Advanced configuration
----------------------

Scotty can be used to download extra sources, add additional layers or tweak the
configuration.

Supported update arguments
^^^^^^^^^^^^^^^^^^^^^^^^^^
- ``--manifest-branch``: Set repo branch used for repo init.
- ``--manifest-url``: Set repo url used for repo init.
- ``--manifest-name``: Set repo manifest used for repo init.
- ``--extra-download``: Add an extra git to download. If this is a layer, it can
  then be used in setup with ``--extra-layer``.

Supported setup arguments
^^^^^^^^^^^^^^^^^^^^^^^^^
- ``--build-dir``: Set build subdirectory, subdirectory of ``build``. Can be
  used to have different builds in the same ``build`` folder.
- ``--machine-dir``: specify the directories where scotty should look for
  supported machines.
- ``--extra-layer``: Add an extra local layer.
- ``--extra-conf``: Add an extra configuration entry in local.conf.
- ``--extra-env``: Pass on additional environment variables.
- ``--sstate-mirrors``: Do use any sstate mirror (default = false).
- ``--features-layers-set``: The set of Avnet Embedded extra layers to use.
- ``--machine-dir``: specify the directories where scotty should look for
  supported machines.

.. note::

  The currently available ``--features-layers-set`` can be displayed by running

  .. code-block:: bash

    $ scotty info feature-sets

Supported bitbake, shell and command arguments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``--build-dir``: Set build subdirectory, subdirectory of ``build``. Can be
  used to have different builds in the same ``build`` folder.

Scripting configuration
-----------------------

It might be useful to skip the configuration menu, so Scotty can be used in a
scripted way. To help with this, most configuration can be set either through
arguments or environment variables.

Supported arguments
^^^^^^^^^^^^^^^^^^^

The ``--features-layers-set`` of the ``setup`` subcommand can be used to bypass
layer sets selection.


Supported environment variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``DISTRO``: Can be used to select the Yocto distro and skip selection menu.
- ``MACHINE``: Can be used to select the Yocto machine and skip selection menu.
- ``ACCEPT_FSL_EULA``: Can be used to set the Freescale/NXP EULA status and skip
  selection menu if applicable).
- ``LICENSE_FLAGS_ACCEPTED``: Can be use to allow e.g. commercial licenses in the resulting images.
- ``UBOOT_ENV_VARS``: Can be use to prepopulate the used u-boot environment (expects a key value list, separated by new lines). To disable pass " ".
- ``SCOTTY_FEATURE_LAYERS``: A space separated list of feature layers (alternative to ``scotty setup --features-layers-set`` - CLI flags have always precedence).

Example
^^^^^^^

.. code-block:: bash

   $ export ACCEPT_FSL_EULA=1
   $ export LICENSE_FLAGS_ACCEPTED=commercial
   $ DISTRO=simplecore-distro MACHINE=sm2s-imx8plus scotty setup --features-layers-set distro
   $ scotty bitbake core-image-minimal

In addition, it is possible to tweak Scotty behaviour using the environment:

- ``SCOTTY_WHITELIST``: The list of host environment variables exposed in Yocto
  environment.
- ``DOCKER_EXTRA_ARGS``: Additional parameters for docker.

Example

.. code-block:: bash

   $ export DOCKER_EXTRA_ARGS="-v /home/downloads:/home/scotty/build/downloads -v /home/sstate-cache:/home/scotty/build/sstate-cache"
   $ scotty bitbake core-image-minimal


Using Scotty on Windows
-----------------------

Scotty has been tested on Windows with WSL2.

Installation
^^^^^^^^^^^^

.. admonition:: The following will need Administator permission
  :class: ATTENTION

  - enable and install ``Windows subsystem for Linux 2`` like decribed `here <https://learn.microsoft.com/en-us/windows/wsl/install>`_.

    We recommend to use the ``Ubuntu`` virtual machine for WSL2.

    **NOTE** only version 2 of WSL is supported.

- install `docker on WSL2 <https://dev.to/bowmanjd/install-docker-on-windows-wsl-without-docker-desktop-34m9>`_
- install ``openssh``

.. code-block:: console

  $ sudo apt update
  $ sudo apt install openssh-server

- install ``pip``

.. code-block:: console

  $ sudo apt update
  $ sudo apt install -y python3-pip

and finally install ``scotty``

.. code-block:: console

  $ pip3 install avnet-scotty

Configure WSL2
^^^^^^^^^^^^^^

It is recommended to disable the `/etc/resolv.conf updating`.
For that run from within the WSL2 VM

.. code-block:: console

  $ echo "[network]" >> /etc/wsl.conf
  $ echo "generateResolvConf = false" >> /etc/wsl.conf

now close the WSL2 VM window.

Dependending on the CPU count and the available RAM of your Windows machine you'll need to configure the following:

From a ``cmd.exe`` on Windows

.. code-block:: console

  $ cd %userprofile%
  $ notepad .wslconfig

Now add the following to the file

.. code-block:: ini

  [wsl2]
  processors=<Amount of RAM in GB / 4>
  swap=<Free disk space in GB - 150>GB

so for a Windows PC with 16 cores, 16GB of RAM and 300GB of free disk space that would be

.. code-block:: ini

  [wsl2]
  processors=4
  swap=150GB

save the file, close the window and run

.. code-block:: console

  $ wsl --shutdown

after that you can launch your WSL VM and start using ``scotty``.

SSH keys
^^^^^^^^

For ``scotty`` to work properly you'll need to create and reference SSH keys for Github, like
described `on this page <https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent>`_.

Reusing your SSH keys from Windows
##################################

In case you want to reuse your SSH keys from windows just run

.. code-block:: console

  $ mkdir -p ~/.ssh
  $ cp /mnt/c/Users/<your Windows username>/.ssh/* ~/.ssh/
  $ chmod 0400 ~/.ssh/id_*

Using WSL2 with VSCode
^^^^^^^^^^^^^^^^^^^^^^^

You'll need to install `this extension <https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl>`_ in your VSCode
and configure it like shown on the website.

Using Scotty without Docker
---------------------------

If needed, Scotty can be used without docker. In this case, you are in charge of
providing a fully configured environment. This can be done by setting the
``SCOTTY_USE_DOCKER`` environment variable::

    $ SCOTTY_USE_DOCKER=0 scotty bitbake core-image-minimal

Scotty Runqemu
==============

``Scotty Runqemu`` is an additional tool allowing to start QEMU to run a QEMU targeted build.

Runqemu Example
---------------

.. code-block:: bash

   $ export DISTRO=simplecore-distro MACHINE=qemux86-64
   $ scotty setup --features-layers-set examples
   $ scotty bitbake simplecore-weston-demo-image
   $ scotty-runqemu simplecore-weston-demo-image

.. note::

  In case your machine does not offer KVM support run

  .. code-block:: bash
    
    $ SCOTTY_QEMUNOKVM=1 scotty-runqemu simplecore-weston-demo-image

.. note::

  In you like to start an image in headless mode (no graphics) run

  .. code-block:: bash
    
    $ SCOTTY_QEMUNOGPAHIC=1 scotty-runqemu simplecore-weston-demo-image

scotty-test
===========

``scotty-test`` is a helper tool to run tests on real hardware.
It will guide the user through the needed steps and create a test report.

To run you will need

- an Azure access token ``SAS_TOKEN``
- access to `simplecore-tools <https://github.com/avnet-embedded/simplecore-tools>`_ repository
- a Github account
- a computer running Linux
  - ``sudo``, ``dd``, ``git`` installed
  - your git client propely setup
- a SDCard
- Internet access
- the hardware you want to test

.. code-block:: bash
  
  $ SAS_TOKEN=abcdef scotty-test

The tool will download the necessary images and SDKs, run the tests and create a Markdown report that will
be pushed to the `simplecore-tools repository <https://github.com/avnet-embedded/simplecore-tools>`_.

scotty-layers.yaml
==================

All the information ``scotty`` uses is defined in ``scotty-layers.yaml`` in the ``manifest`` repository.
This file is a ``yaml`` file containing the following sections:

base section
------------

Allowed number of sections in the ``yaml``: 1

This section defines the layers that are **always** used in any setup.

+-------------+--------+----------------------------+--------------------------------------+
| Key         | Type   | Description                | Example                              |
+=============+========+============================+======================================+
| description | string | Human readable description | description: "My base layers"        |
+-------------+--------+----------------------------+--------------------------------------+
| layers      | list   | Paths to layers to be used | layers:                              |
|             |        |                            |    ? "meta-openembedded/meta-oe"     |
+-------------+--------+----------------------------+--------------------------------------+
| licenses    | list   | additional EULA/licenses   | licenses:                            |
|             |        | to be accepted by the user |    - path: "meta-layer/EULA.txt"     |
|             |        |                            |      env: "META_VAR"                 |
|             |        |                            |      description: "Some explantion"  |
+-------------+--------+----------------------------+--------------------------------------+

**NOTE**: ``licenses`` is optional

distro_* section
----------------

Allowed number of sections in the ``yaml``: 1..n

These sections define the possible selections for Yocto’s ``DISTRO`` setting.

+-------------------+--------+------------------------------------------------+-------------------------------------------------+
| Key               | Type   | Description                                    | Example                                         |
+===================+========+================================================+=================================================+
| description       | string | Human readable description                     | description: "Super Distro"                     |
+-------------------+--------+------------------------------------------------+-------------------------------------------------+
| menu_priority     | int    | Defines the order in the menu                  | menu_priority: 100                              |
+-------------------+--------+------------------------------------------------+-------------------------------------------------+
| layers            | list   | Paths to layers to be used                     | layers:                                         |
|                   |        |                                                |    ? "poky/meta"                                | 
+-------------------+--------+------------------------------------------------+-------------------------------------------------+
| supported_distros | dict   | key/value table of DISTRO name and description | supported_distros: &distros_poky                |
|                   |        |                                                |    poky: "poky: Yocto Project Reference Distro" |
+-------------------+--------+------------------------------------------------+-------------------------------------------------+

machines_* section
------------------

Allowed number of sections in the ``yaml``: 1..n

These sections define the needed layer set for the selected ``MACHINE`` entry.

+-------------------+--------+-----------------------------------------+----------------------------------+
| Key               | Type   | Description                             | Example                          |
+===================+========+=========================================+==================================+
| description       | string | Human readable description              | description: "My machine layers" |
+-------------------+--------+-----------------------------------------+----------------------------------+
| layers            | list   | Paths to layers to be used              | layers:                          |
|                   |        |                                         |    ? "meta-intel"                | 
+-------------------+--------+-----------------------------------------+----------------------------------+
| machine_pattern   | string | Regular expression matching ``MACHINE`` | machine_pattern: "sm2s-.l"       |
+-------------------+--------+-----------------------------------------+----------------------------------+

overlays_* section
------------------

Allowed number of sections in the ``yaml``: 0..n

These sections define the available device tree overlays to be selectable by ``scotty``

+-------------------+--------+-----------------------------------------+----------------------------------+
| Key               | Type   | Description                             | Example                          |
+===================+========+=========================================+==================================+
| description       | string | Human readable description              | description: "My overlays"       |
+-------------------+--------+-----------------------------------------+----------------------------------+
| overlays          | dict   | key/value table                         | overlays:                        |
|                   |        |       overlay-filename/description      |   test.dtb: "my DTB"             | 
+-------------------+--------+-----------------------------------------+----------------------------------+
| machine_pattern   | string | Regular expression matching ``MACHINE`` | machine_pattern: "sm2s-.l"       |
+-------------------+--------+-----------------------------------------+----------------------------------+

feature_* section
-----------------

Allowed number of sections in the ``yaml``: 0..n

These sections define the possible selections for additional features.
Features can reference each other by using yaml anchors.

The following example

.. code:: yaml

  feature_myfeature:
    menu_priority: 200
    description: "My feature layer"
    layers: &layers_myfeature
      <<: [*layers_poky]
      ? "meta-myfeature"
    supported_distros: &distros_myfeature
      <<: [*distros_poky]

defines a feature that is called ``My feature layer``. It will add ``meta-myfeature`` to the layer set, and is only applicable
if ``poky`` is selected as a DISTRO. By selecting this feature all layers defined by the ``poky`` DISTRO will be setup as well.

+-------------------+--------+------------------------------------------------+-------------------------------------------------+
| Key               | Type   | Description                                    | Example                                         |
+===================+========+================================================+=================================================+
| description       | string | Human readable description                     | description: "My feature"                       |
+-------------------+--------+------------------------------------------------+-------------------------------------------------+
| menu_priority     | int    | Defines the order in the menu                  | menu_priority: 100                              |
+-------------------+--------+------------------------------------------------+-------------------------------------------------+
| layers            | list   | Paths to layers to be used                     | layers:                                         |
|                   |        |                                                |    ? "meta-myfeature"                           |
+-------------------+--------+------------------------------------------------+-------------------------------------------------+
| extraconf         | list   | Extra configuration variables for local.conf   | extraconf:                                      |
|                   |        |                                                |    ? "INHERIT += 'myclass'"                     |
+-------------------+--------+------------------------------------------------+-------------------------------------------------+
| supported_distros | dict   | key/value table of DISTRO name and description | supported_distros: &distros_myfeature           |
|                   |        |                                                |    <<: [\*distros_poky]                         |
+-------------------+--------+------------------------------------------------+-------------------------------------------------+
| add-overlays      | object | Additional selectable overlays of the feature  | add-overlays:                                   |
|                   |        |   see `overlays section` for details           |    overlays:                                    |
+-------------------+--------+------------------------------------------------+-------------------------------------------------+

scotty-layers.ext.yaml
======================

``scotty`` will additionally scan for ``scotty-layers.ext.yaml`` in the checked out repositories.
These files are written in the same syntax as ``scotty-layers.yaml`` and allow the standard ``scotty-layers.yaml`` to be extended.

The files have to be placed in the root of the bitbake layer.
