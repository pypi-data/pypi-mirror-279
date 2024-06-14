CHANGELOG
=========

This project uses `semantic versioning <http://semver.org/>`_.
This change log uses principles from `keep a changelog <http://keepachangelog.com/>`_.

[0.4.0]
-------

Changed
^^^^^^^

- Swicthed from ``dtool-lookup-server`` to ``dservercore``

[0.3.0]
-------

Changed
^^^^^^^

- Transitioned from ``setup.py`` to ``pyproject.toml``.
- Rebranded from ``dtool-lookup-server-`` prefix to ``dserver-`` prefix.

[0.2.0]
-------

Added
^^^^^

- ``QueryDatasetSchema`` schema with
  ``creator_usernames``, ``base_uris``, ``uuids``,  ``tags``, ``aggregation``, and ``query`` query fields.
- ``/mongo/query`` route,
- ``/mongo/aggregate`` route.
- ``MONGO_URI``. ``MONGO_DB``, ``MONGO_COLLECTION``, ``ALLOW_DIRECT_QUERY``, and ``ALLOW_DIRECT_AGGREGATION`` configuration parameters.

Changed
^^^^^^^


Deprecated
^^^^^^^^^^


Removed
^^^^^^^


Fixed
^^^^^


Security
^^^^^^^^


