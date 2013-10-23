First check if django is yet installed:

.. code-block:: console
    $ python -c "import django; print(django.get_version())"

If you get the following error:

.. code-block:: console
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
    ImportError: No module named django

Then django isn't installed so go ahead and install it:

.. code-block:: console

    $ conda install django
    Package plan for installation in environment /Applications/anaconda:

    The following packages will be linked:

        package                    |            build
        ---------------------------|-----------------
        django-1.5.4               |           py27_0   hard

    Proceed ([y]/n)? y

    Linking packages ...
    [      COMPLETE      ] |##############################################| 100%

