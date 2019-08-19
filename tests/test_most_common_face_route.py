import pytest
from jsonschema import validate


def validate_response(response_json):
    schema = {
        "type": "object",
        "properties": {
            "image_filepath": {"anyOf": [{"type": "string"}, {"type": "null"}]},
            "face_id": {"anyOf": [{"type": "string"}, {"type": "null"}]},
            "face_rectangle": {
                "anyOf": [
                    {"type": "null"},
                    {"type": "object",
                     "properties": {
                        "top": {"type": "number"},
                        "left": {"type": "number"},
                        "width": {"type": "number"},
                        "height": {"type": "number"}
                     }
                     }
                ]
            }
        }
    }

    validate(instance=response_json, schema=schema)


def validate_error_response(response_json):
    schema = {
        "type": "object",
        "properties": {
            "error": {"type": "string"},
            "details": {"anyOf": [{"type": "string"}, {"type": "null"}]},
        }
    }

    validate(instance=response_json, schema=schema)


@pytest.mark.parametrize("json_data", [{"images": [r"test_images\test-image-person-group.jpg",
                                                   r"test_images\man3-person-group.jpg"]},
                                       {"images": [r"test_images\man3-person-group.jpg"]},
                                       {"images": [r"test_images\test-image-person-group.jpg",
                                                   r"test_images\man1-person-group.jpg",
                                                   r"test_images\man2-person-group.jpg",
                                                   r"test_images\man3-person-group.jpg",
                                                   r"test_images\woman1-person-group.jpg",
                                                   r"test_images\child1-person-group.jpg"]}
                                       ])
def test_most_common_face_valid_requests(test_client, json_data):
    response = test_client.post('/face/most-common-face', json=json_data)
    assert response.status_code == 200
    validate_response(response.json)
    assert response.json['image_filepath'] == r"test_images\man3-person-group.jpg"


@pytest.mark.parametrize("json_data", [None, {}, {"test_key": []}, {"images": "test_value"}, {"images": []}])
def test_most_common_face_invalid_request_parameters(test_client, json_data):
    response = test_client.post('/face/most-common-face', json=json_data)
    assert response.status_code == 400
    validate_error_response(response.json)


def test_image_file_not_exists(test_client):
    response = test_client.post('/face/most-common-face', json={"images": [r"path\to\test\file"]})
    assert response.status_code == 500
    validate_error_response(response.json)


def test_image_without_faces(test_client):
    response = test_client.post('/face/most-common-face', json={"images": [r"test_images\test-image-no-faces.jpg"]})
    assert response.status_code == 200
    validate_response(response.json)
    assert response.json['image_filepath'] is None
    assert response.json['face_id'] is None
    assert response.json['face_rectangle'] is None
