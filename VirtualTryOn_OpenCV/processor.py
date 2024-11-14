import os
import cv2
import cvzone
from cvzone.PoseModule import PoseDetector

def process_image(user_image_path, shirt_image_path, result_folder="Results/"):
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)

    # Load user image and shirt image
    user_image = cv2.imread(user_image_path)
    shirt_image = cv2.imread(shirt_image_path, cv2.IMREAD_UNCHANGED)

    if user_image is None or shirt_image is None:
        print("Error: Could not load images.")
        return None

    detector = PoseDetector()
    user_image = detector.findPose(user_image)
    lmList, bboxInfo = detector.findPosition(user_image, bboxWithHands=False, draw=False)

    if lmList:
        lm11 = lmList[11][0:2]  # Left shoulder
        lm12 = lmList[12][0:2]  # Right shoulder
        widthOfShirt = int(abs(lm11[0] - lm12[0]) * (262 / 190))
        if widthOfShirt > 0:
            imgShirt = cv2.resize(shirt_image, (widthOfShirt, int(widthOfShirt * (581 / 440))))
            offset = (int(44 * ((abs(lm11[0] - lm12[0])) / 190)), int(48 * ((abs(lm11[0] - lm12[0])) / 190)))
            user_image = cvzone.overlayPNG(user_image, imgShirt, (lm12[0] - offset[0], lm12[1] - offset[1]))

            # Save result image
            result_path = os.path.join(result_folder, 'modified_image.png')
            cv2.imwrite(result_path, user_image)
            # Show the image
            cv2.imshow("Image", user_image)
            return user_image

    return None


def process_video_or_realtime(source, shirt_image_path, result_folder, is_video=True):
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)

    detector = PoseDetector()
    shirt_image = cv2.imread(shirt_image_path, cv2.IMREAD_UNCHANGED)

    if shirt_image is None:
        print("Error: Could not load shirt image.")
        return

    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print("Error: Could not open video or webcam.")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_size = (frame_width, frame_height)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_filename = 'output_video.mp4' if is_video else 'output_realtime.mp4'
    output_path = os.path.join(result_folder, output_filename)

    out = cv2.VideoWriter(output_path, fourcc, 20.0, frame_size)

    while True:
        success, img = cap.read()
        if not success:
            print("Error: Failed to capture frame.")
            break

        img = detector.findPose(img)
        lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)

        if lmList:
            lm11 = lmList[11][0:2]  # Left shoulder
            lm12 = lmList[12][0:2]  # Right shoulder
            widthOfShirt = int(abs(lm11[0] - lm12[0]) * (262 / 190))
            if widthOfShirt > 0:
                imgShirt = cv2.resize(shirt_image, (widthOfShirt, int(widthOfShirt * (581 / 440))))
                offset = (int(44 * ((abs(lm11[0] - lm12[0])) / 190)), int(48 * ((abs(lm11[0] - lm12[0])) / 190)))
                img = cvzone.overlayPNG(img, imgShirt, (lm12[0] - offset[0], lm12[1] - offset[1]))

        out.write(img)

        cv2.imshow("Virtual Dressing Room", img)

        # Check for 'q' key to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
