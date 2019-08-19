import os

import pytest


@pytest.mark.parametrize("json_data", [None, {}, {"test_key": []}, {"images": "test_value"}])
def test_most_common_face_invalid_request_parameters(test_client, json_data):
    response = test_client.post('/face/most-common-face', json=json_data)
    assert response.status_code == 400


def test_most_common_face_valid_request(test_client):
    response = test_client.post('/face/most-common-face', json={"images":
                                [os.path.abspath(r"..\test_images\test-image-person-group.jpg")]})
    assert response.status_code == 200
