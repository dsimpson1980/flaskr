From start to finish (for Mac OSX)
==================================

Mac OSX come with python already installed.  For a number of reasons I prefer to
use Anaconda from continuum which you can download here <link>.  I will assume
that you install it to the /Applications/ folder

You can check which version of python is being used by running the following:

.. code-block:: none

    $ which python

Which should return:

.. code-block:: none

    /Applications/anaconda/bin/python

If you used the standalone anconda installer this should already be the case.  If
not you will need to add the following line to the start of your .bash_profile
in your home directory:

.. code-block::

    export PATH="/Applications/anaconda/bin:$PATH"

this adds the path to your python installation to the start of the PATH
environment variable.

TODO: Include details for install postgres.app and postgresadmin

This uses the conda command to track package installations and dependencies.  I
have compiled a number of packages and uploaded them to binstar that can be
found here.

To make sure conda is aware of this repository you will need to make a .condarc
file in your user directory.  This can be done quite easily by running:

.. code-block:: none

    $ cd
    $ touch .condarc
    $ nano .condarc

The detailed instructions can be found here but in brief the .condarc file
should look something like this:

.. code-block:: python

    # This is the default conda runtime configuration

    # channel locations. These override conda defaults, i.e., conda will
    # search *only* the channels listed here, in the order given here

    channels:
      - http://repo.continuum.io/pkgs/free/
      - http://repo.continuum.io/pkgs/pro/
      - https://conda.binstar.org/dsimpson1980/

you will need to install the following packages:

.. code-block:: none

    $ conda install pandas (this will install numpy)
    $ conda install flask-sqlalchemy (this will install flask and sqlalchemy)
    $ conda install wtforms (from my repo above)

Unfortunately, I haven't yet compiled the celery <link> package so it will need
to be installed using pip:

.. code-block:: none

    $ pip install celery
