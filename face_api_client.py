from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials


class FaceApiClient(object):
    class __FaceApiClient:
        KEY = "a2671802fb6f40abaac8430b46a021e7"
        ENDPOINT_STRING = "westeurope"
        ENDPOINT = 'https://{}.api.cognitive.microsoft.com/'.format(ENDPOINT_STRING)

        # TODO - read values from config?
        def __init__(self, key=KEY, endpoint=ENDPOINT):
            self.__face_client = FaceClient(endpoint, CognitiveServicesCredentials(key))

        def most_common_face(self, images):
            pass  # TODO - implementation

    __instance = None

    @staticmethod
    def get_instance():
        if FaceApiClient.__instance is None:
            FaceApiClient.__instance = FaceApiClient.__FaceApiClient()
        return FaceApiClient.__instance

    def __init__(self):
        raise Exception("FaceApiClient class is a singleton. Instance should be accessed with "
                        "FaceApiClient.get_instance()")
