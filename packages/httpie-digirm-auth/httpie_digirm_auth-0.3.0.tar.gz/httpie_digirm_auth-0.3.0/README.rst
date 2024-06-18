httpie-digirm-auth
==================

Authorization plugin (`DigiRMAuth <https://github.com/kulack/httpie-digirm-auth>`_) to specify API keys in `HTTPie <https://github.com/jkbr/httpie>`_.


Installation
------------

.. code-block:: bash

    $ httpie plugins install httpie-digirm-auth

    # OR

    $ pip install httpie-digirm-auth


You should now see:

* ``httpie-digirm-auth`` plugin in the ``httpie plugins list`` command
* ``drm`` under ``--auth-type`` in ``http --help`` output.


Usage
-----

.. code-block:: bash

    $ https --auth-type=drm --auth='api-key-id:api-key-secret' \
        remotemanager.digi.com/ws/v1/devices/inventory


You can omit the ``--auth`` parameter and specify the API key ID and secret in the ``~/.netrc`` file (or prompt for them) as if they were user names and passwords.

.. code-block:: bash

    $ https --auth-type=drm remotemanager.digi.com/ws/v1/devices/inventory


Compatibility
-------------

Attempts to recognize Digi Remote Manager API key authentication and falls back to basic auth if the key is not a Digi Remote Manager API key.

In the API key authentication scheme the API key ID and API key secret are used in the ``X-API-KEY-ID`` and ``X-API-KEY-SECRET`` headers respectively.
