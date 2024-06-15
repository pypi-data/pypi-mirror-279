httpie-digirm-auth
==================

`DigiRMAuth <https://github.com/kulack/httpie_digirm_auth>`_ auth plugin for `HTTPie <https://github.com/jkbr/httpie>`_.


Installation
------------

* Clone this repository

.. code-block:: bash

    $ httpie plugins install httpie-digirm-auth

You should now see ``digirm`` under ``--auth-type`` in ``$ http --help`` output.


Usage
-----

.. code-block:: bash

    $ https --auth-type=digirm --auth='api_key_id:api_key_secret' remotemanager.digi.com/ws/v1/devices/inventory


You can omit the ``--auth`` parameter and specify the api_key and api_key_secret in the ``~/.netrc`` file as if they were user names and passwords.

.. code-block:: bash

    $ https --auth-type=digirm remotemanager.digi.com/ws/v1/devices/inventory


Compatibility
-------------

As of version 0.1.0 of this library, only Digi Remote Manager API key authentication is supported.

In that authentication schema the API key ID and API key secret are used in the ``X-API-KEY-ID`` and ``X-API-KEY-SECRET`` headers respectively.
