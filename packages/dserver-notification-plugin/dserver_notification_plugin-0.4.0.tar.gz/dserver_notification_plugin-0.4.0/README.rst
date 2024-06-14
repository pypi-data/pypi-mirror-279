dserver Notification Plugin
===========================

.. |dtool| image:: https://github.com/livMatS/dserver-notification-plugin/blob/main/icons/22x22/dtool_logo.png?raw=True
    :height: 20px
    :target: https://github.com/livMatS/dserver-notification-plugin
.. |pypi| image:: https://img.shields.io/pypi/v/dserver-notification-plugin
    :target: https://pypi.org/project/dserver-notification-plugin/
.. |tag| image:: https://img.shields.io/github/v/tag/livMatS/dserver-notification-plugin
    :target: https://github.com/livMatS/dserver-notification-plugin/tags
.. |test| image:: https://img.shields.io/github/actions/workflow/status/livMatS/dserver-notification-plugin/test.yml?branch=main&label=tests
    :target: https://github.com/livMatS/dserver-notification-plugin/actions/workflows/test.yml

|dtool| |pypi| |tag| |test|

- GitHub: https://github.com/livMatS/dserver-notification-plugin
- PyPI: https://pypi.python.org/pypi/dserver-notification-plugin
- Free software: MIT License


Features
--------

- Listen to `S3 event notifications <https://docs.aws.amazon.com/AmazonS3/latest/userguide/notification-content-structure.html>`_
  from an S3-compatible storage backend


Introduction
------------

`dtool <https://dtool.readthedocs.io>`_ is a command line tool for packaging
data and metadata into a dataset. A dtool dataset manages data and metadata
without the need for a central database.

However, if one has to manage more than a hundred datasets it can be helpful
to have the datasets' metadata stored in a central server to enable one to
quickly find datasets of interest.

`dservercore <https://github.com/jic-dtool/dservercore>`_
provides a web API for registering datasets' metadata
and provides functionality to lookup, list and search for datasets.

This plugin enables the dserver to listen to
notifications for the registration and deregistration of datasets.


Installation
------------

Install the dtool lookup server dependency graph plugin

.. code-block:: bash

    $ pip install dserver-notification-plugin

Setup and configuration
-----------------------

Configure plugin behavior
^^^^^^^^^^^^^^^^^^^^^^^^^

The plugin needs to know how to convert a bucket name into a base URI. The
environment variable ``DSERVER_NOTIFY_BUCKET_TO_BASE_URI`` is used
to specify that conversion, e.g.::

    DSERVER_NOTIFY_BUCKET_TO_BASE_URI={"bucket": "ecs://bucket"}

It is also advisable to limit access to the notification listener to a certain
IP range. Use::

    DSERVER_NOTIFY_ALLOW_ACCESS_FROM=192.168.0.0/16

to specify the allowed remote network. To specify a single IP, use::

    DSERVER_NOTIFY_ALLOW_ACCESS_FROM=192.168.1.1/32

Configure elastic search integration in NetApp StorageGRID
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a new endpoint with URI ``https://myserver:myport/elastic-search``
and URN ``arn:<mysite>:es:::<domain-name>/notify/all``

Note that `<mysite>` and `<domain-name>` can be chose arbitrarily.
`notify/all` is appended to the URI and must point to the route of
the notify function.

The bucket needs to be configured to support search integration. Use the
following XML template

.. code-block:: xml

    <MetadataNotificationConfiguration>
        <Rule>
            <ID>dtool</ID>
            <Status>Enabled</Status>
            <Prefix></Prefix>
            <Destination>
               <Urn>urn:mysite:es:::domain-name/notify/all</Urn>
            </Destination>
        </Rule>
    </MetadataNotificationConfiguration>


Configure webhook in minio
^^^^^^^^^^^^^^^^^^^^^^^^^^

The `Publish Events to Webhook minio docs
<https://docs.min.io/minio/baremetal/monitoring/bucket-notifications/publish-events-to-webhook.html>`_
walks through the configuration for sending S3 event notifications to a webhook.
Assuming a *dserver* with this plugin activated running at
``http://dserver:5000``, and your minio instance with a
bucket ``test-bucket`` at ``https://s3server:9000``, use

.. code-block:: bash

    # mc: minio client
    mc config host add s3server http://s3server:9000 {admin_user} {admin_password}

    # Note that the endpoint must be reachable when configuring, otherwise minio will reject
    mc admin config set s3server/ notify_webhook:dtool  endpoint="http://dserver:5000/webhook/notify"
    mc admin service restart s3server  # restart is necessary

    # Activate the actual notifications
    mc event add s3server/test-bucket arn:minio:sqs::testbucket:dtool --event "put,delete"

to configure a webhook endpoint identified by ``dtool`` and activate ``put`` and
``delete`` event notification.
Choose the parameters for ``--event "put,delete"`` from minio's
`Supported Bucket Evenets <https://docs.min.io/minio/baremetal/reference/minio-mc/mc-event-add.html#mc-event-supported-events>`_.

Note that minio is very strict on whom they talk to. If your `dserver`
communicates via `https`, make sure that the server certificate uses `SANs
<https://en.wikipedia.org/wiki/Subject_Alternative_Name>`_ and that the
signing authority's root certificate is available to minio. See
`Install Certificates from Third-party CAs
<https://docs.min.io/docs/how-to-secure-access-to-minio-server-with-tls.html>`_
in the minio docs. Also assure all services are reachable by valid hostnames.
Within a containerized environment such as launched with `docker-compose` ,
host names containing underscores ``_`` may occur, but minio refuses to speak with
such.

Configure webhook in NetApp StorageGRID
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

NetAPP StorageGRID is able to submit S3 event notifications when configured to
communicate with an SNS endpoint, refer to the according sections of the 
`NetApp StorageGRID docs <https://docs.netapp.com/sgws-115/index.jsp>`_ for 
`creating service endpoints <https://docs.netapp.com/sgws-115/topic/com.netapp.doc.sg-tenant-admin/GUID-D98D1AB1-A82A-46AC-88C5-FC53353A29AE.html>`_
and
`configuring event notifications <https://docs.netapp.com/sgws-115/topic/com.netapp.doc.sg-tenant-admin/GUID-F2555EFF-C99B-4F83-9009-C8D59F9EA545.html>`_.

In short, create an endpoint ```http://dserver:5000/webhook/notify```
with a suitable URN, i.e. `urn:dserver:sns:region:notify:all`,
where you may pick all fields freely except ``urn`` and ``sns``. 

Next, enable event notifications for the desired bucket, i.e. for object creation events with a policy snippet like this:

.. code-block:: xml

    <NotificationConfiguration>
      <TopicConfiguration>
        <Id>Object created</Id>
        <Topic>urn:dserver:sns:region:notify:all</Topic>
        <Event>s3:ObjectCreated:*</Event>
      </TopicConfiguration>
    </NotificationConfiguration>


Testing
-------

Launch a minimal mongodb instance with

.. code-block:: bash

    $ cd tests/container && docker-compose up -d

and run tests from within repository root using

.. code-block:: bash

    pytest --log-cli-level=DEBUG

Refer to ``.github/workflows/test.yml`` for the recommended testing environment.

Related repositories
--------------------

- `dtool-s3 <https://github.com/jic-dtool/dtool-s3>`_ - storage broker interface to S3 object storage
- `dtool-ecs <https://github.com/jic-dtool/dtool-ecs>`_ - storage broker interface to ECS S3 object storage
