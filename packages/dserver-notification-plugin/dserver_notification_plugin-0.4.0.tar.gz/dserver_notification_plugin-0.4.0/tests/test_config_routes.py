"""Test the server's config blueprint route for plugin parameters."""

import json

from . import compare_marked_nested, comparison_marker_from_obj


def test_config_info_route(tmp_app_with_users, snowwhite_token):  # NOQA

    headers = dict(Authorization="Bearer " + snowwhite_token)
    r = tmp_app_with_users.get(
        "/config/info",
        headers=headers,
    )
    assert r.status_code == 200

    expected_response = {
        "allow_access_from": "0.0.0.0/0",
        "bucket_to_base_uri": {"bucket": "s3://bucket"},
    }

    response = json.loads(r.data.decode("utf-8"))

    assert "config" in response

    marker = comparison_marker_from_obj(expected_response)
    assert compare_marked_nested(response['config'], expected_response, marker)