from app.face.detected_face import DetectedFace
from app.face.face_image import FaceImage


class MostCommonFace(object):
    @staticmethod
    def __detect_faces(face_client, face_images):
        total_detected_faces = {}

        for face_image in face_images:
            with face_image.image_stream() as image_stream:
                # TODO - wrap with try-catch (API error)
                detected_faces_metadata = face_client.face.detect_with_stream(image_stream, return_face_id=True,
                                                                              return_face_landmarks=True)
                for face_metadata in detected_faces_metadata:
                    total_detected_faces[face_metadata.face_id] = DetectedFace(face_metadata, face_image)

        return total_detected_faces

    @staticmethod
    def __calculate_face_image_ratio(face_metadata, face_image):
        image_area = face_image.width*face_image.height
        face_area = face_metadata.face_rectangle.width*face_metadata.face_rectangle.height
        return face_area/image_area

    @staticmethod
    def __find_best_face_in_group(group, detected_faces):
        group_detected_faces = [detected_faces[face_id] for face_id in group]

        return max(group_detected_faces, key=lambda detected_face: MostCommonFace.__calculate_face_image_ratio(
            detected_face.metadata, detected_face.face_image))

    @staticmethod
    def __format_result(detected_face):
        result = {"face_id": detected_face.metadata.face_id, "image_filepath": detected_face.face_image.filepath}
        return result  # FIXME

    @staticmethod
    def most_common_face_from_image_filepaths(face_client, image_filepaths):
        face_images = [FaceImage(filepath) for filepath in image_filepaths]
        if not face_images:
            raise Exception("Empty request image list")     # FIXME

        detected_faces = MostCommonFace.__detect_faces(face_client, face_images)
        if not detected_faces:
            raise Exception("No detected faces")             # FIXME

        # TODO - handle case where number of faces is not supported by API (<2 | >1000)
        group_result = face_client.face.group(detected_faces.keys())

        if not group_result.groups:
            # All faces are equally common. Choose best one from messy group
            common_group = group_result.messy_group
        else:
            common_group = max(group_result.groups, key=len)

        best_detected_face = MostCommonFace.__find_best_face_in_group(common_group, detected_faces)

        return MostCommonFace.__format_result(best_detected_face)
