import ipaddress
import json
import os


CONFIG_SECRETS_TO_OBFUSCATE = []


class Config(object):
    # Dictionary for conversion of bucket names to base URIs
    BUCKET_TO_BASE_URI = json.loads(
        os.environ.get('DSERVER_NOTIFY_BUCKET_TO_BASE_URI',
                       '{"bucket": "s3://bucket"}'))

    # Limit notification access to IPs starting with this string
    ALLOW_ACCESS_FROM = ipaddress.ip_network(
        os.environ.get('DSERVER_NOTIFY_ALLOW_ACCESS_FROM',
                       '0.0.0.0/0'))  # Default is access from any IP
