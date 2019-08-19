from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials


class SingletonFaceClient(object):
    ENDPOINT_STRING_FORMAT = 'https://{}.api.cognitive.microsoft.com/'
    __instance = None

    @classmethod
    def get_instance(cls, config):
        if SingletonFaceClient.__instance is None:
            endpoint = cls.ENDPOINT_STRING_FORMAT.format(config['FACE_CLIENT_ENDPOINT_STRING'])
            SingletonFaceClient.__instance = FaceClient(endpoint,
                                                        CognitiveServicesCredentials(config['FACE_CLIENT_KEY']))

        return SingletonFaceClient.__instance

    def __init__(self):
        raise Exception("FaceApiClient class is a singleton. Instance should be accessed with "
                        "FaceApiClient.get_instance()")
