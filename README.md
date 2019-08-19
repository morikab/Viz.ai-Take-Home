# Viz.ai-Take-Home
A simple http service that exposes an endpoint for finding the most common face in a list of images.

The service receives a list of image filepaths and returns metadata about the "best image" of this common face, where  
"best image" is defined as the the image where the bounding box of the face is largest in relation to the size of the 
image.

## Getting Started

### Prerequisites
* Install project dependencies:
```
pip install -r requirements.txt
```

* Valid Azure subscription. You can find a guide for creating one for free [here](https://azure.microsoft.com/en-us/free/). 

### Usage
#### Setting Configuration
Our service requires a local configuration file located at <project-dir>/instance/config.cfg.
This file contains parameters needed for instantiating a local running instance of the service.

*Example config.cfg*:
```
PORT = 8001
HOST = "0.0.0.0"

FACE_CLIENT_KEY = "a2671802fb6f40abaac8430b46a021e7"
FACE_CLIENT_ENDPOINT_STRING = "westeurope"
``` 

In the example above:
*   HOST & PORT - are the host and port used for running our service
*   FACE_CLIENT_KEY & FACE_CLIENT_ENDPOINT_STRING - are authentication parameters for the Azure's Cognitive Services 
    resource our service will use. See [here](https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-apis-create-account) 
    a guide for creating a new Azure's Cognitive Services resource. 

**All configuration values above are needed for running the service**

#### Run Service

```
python main.py
```
All requests and responses are based on json-over-http.

*Example request:*
```
import requests
json_data = {"images": [r"test_images\child1-person-group.jpg", r"test_images\child2-person-group.jpg"]} 
requests.post("http://localhost:8001", json={})
```

*Example response json:*
```
{
    "image_filepath": "test_images\child1-person-group.jpg",
    "face_id": "0da8f12a-c433-4c52-b9ed-98a58093d0ab",
    "faceRectangle": {
      "top": 128,
      "left": 459,
      "width": 224,
      "height": 224
    }
}
```

In case of error a json response similar to this is returned:
```bash
{"error": "Unknown server error", "details": None}
```



## Running tests
* Define <project-dir>/instance/test-config.cfg (follow same instructions as in *Setting Configuration* section above).
* Run pytest under tests/
