from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials


class SingletonFaceClient(object):
    KEY = "a2671802fb6f40abaac8430b46a021e7"
    ENDPOINT_STRING = "westeurope"
    ENDPOINT = 'https://{}.api.cognitive.microsoft.com/'.format(ENDPOINT_STRING)

    __instance = None

    @staticmethod
    def get_instance():
        if SingletonFaceClient.__instance is None:
            # TODO - read values from config?
            SingletonFaceClient.__instance = FaceClient(SingletonFaceClient.ENDPOINT,
                                                        CognitiveServicesCredentials(SingletonFaceClient.KEY))
        return SingletonFaceClient.__instance

    def __init__(self):
        raise Exception("FaceApiClient class is a singleton. Instance should be accessed with "
                        "FaceApiClient.get_instance()")
