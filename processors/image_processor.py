import cv2
import dlib


def show_image(img, num_faces):
    # resize the image if it exceeds a certain width or height
    if img.shape[0] > 1024 or img.shape[1] > 1024:
        img = resize_image(img, 1024)

    cv2.imshow(winname=f'Faces detected: {num_faces}.', mat=img)
    cv2.waitKey(delay=0)
    cv2.destroyAllWindows()


def resize_image(image, target_size):
    portrait = False
    if image.shape[0] >= image.shape[1]:
        portrait = True

    if portrait:
        size_divisor = image.shape[0] / target_size
    else:
        size_divisor = image.shape[1] / target_size

    size = (int(image.shape[1] / size_divisor), int(image.shape[0] / size_divisor))
    return cv2.resize(image, size, interpolation=cv2.INTER_AREA)


class ImageProcessor:
    def __init__(self, file):
        self.file = file
        self.img = cv2.imread(self.file)
        self.detector = dlib.get_frontal_face_detector()

        # convert the img to grayscale for facial recognition
        self.img_grayscale = cv2.cvtColor(src=self.img, code=cv2.COLOR_BGR2GRAY)

    def rectangle_face(self):
        faces = self.detector(self.img_grayscale)
        for face in faces:
            x1 = face.left()
            x2 = face.right()
            y1 = face.top()
            y2 = face.bottom()
            cv2.rectangle(img=self.img, pt1=(x1, y1), pt2=(x2, y2), color=(0, 255, 0), thickness=4)

        show_image(self.img, len(faces))

    def landmark_face(self):
        """
        Landmark ranges:
        Jaw Points = 0–16
        Right Brow Points = 17–21
        Left Brow Points = 22–26
        Nose Points = 27–35
        Right Eye Points = 36–41
        Left Eye Points = 42–47
        Mouth Points = 48–60
        Lips Points = 61–67
        """

        predictor = dlib.shape_predictor('processors/shape_predictor_68_face_landmarks.dat')
        faces = self.detector(self.img_grayscale)
        for face in faces:
            landmarks = predictor(image=self.img_grayscale, box=face)
            for landmark in range(0, 68):
                x = landmarks.part(landmark).x
                y = landmarks.part(landmark).y
                cv2.circle(img=self.img, radius=3, center=(x, y), color=(0, 255, 0), thickness=-1)

        show_image(self.img, len(faces))
