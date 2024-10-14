import os
import cvzone
import cv2
from cvzone.PoseModule import PoseDetector

# Initialize video capture and pose detector
cap = cv2.VideoCapture("Resources/Videos/1.mp4")
# cap = cv2.VideoCapture(0)
detector = PoseDetector()

# Set up shirt folder and parameters
shirtFolderPath = "Resources/Shirts"
listShirts = os.listdir(shirtFolderPath)
fixedRatio = 262 / 190  # widthOfShirt / widthOfPoint11to12
shirtRatioHeightWidth = 581 / 440
imageNumber = 0

# Load buttons
imgButtonRight = cv2.imread("Resources/button.png", cv2.IMREAD_UNCHANGED)
imgButtonLeft = cv2.flip(imgButtonRight, 1)

# Selection variables
counterRight = 0
counterLeft = 0
selectionSpeed = 10

# Main loop
while True:
    success, img = cap.read()
    
    if not success:
        print("Failed to read video frame.")
        break

    img = detector.findPose(img)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)
    print(lmList)
    if lmList:
        lm11 = lmList[11][0:2]  # Left shoulder
        lm12 = lmList[12][0:2]  # Right shoulder
        
        # Calculate shirt width (use absolute value to avoid negative widths)
        widthOfShirt = int(abs(lm11[0] - lm12[0]) * fixedRatio)
        print(f"lm11: {lm11}, lm12: {lm12}, widthOfShirt: {widthOfShirt}")
        
        if widthOfShirt > 0:
            # Load shirt image and resize it
            imgShirt = cv2.imread(os.path.join(shirtFolderPath, listShirts[imageNumber]), cv2.IMREAD_UNCHANGED)
            imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(widthOfShirt * shirtRatioHeightWidth)))
            
            # Calculate offset
            currentScale = (abs(lm11[0] - lm12[0])) / 190
            offset = int(44 * currentScale), int(48 * currentScale)

            try:
                # Overlay shirt on the body
                img = cvzone.overlayPNG(img, imgShirt, (lm12[0] - offset[0], lm12[1] - offset[1]))
            except Exception as e:
                print(f"Failed to overlay shirt: {e}")
        else:
            print("Skipping overlay due to invalid widthOfShirt.")

        # Overlay control buttons
        img = cvzone.overlayPNG(img, imgButtonRight, (1074, 293))
        img = cvzone.overlayPNG(img, imgButtonLeft, (72, 293))

        # Right hand gesture for changing shirts
        if lmList[16][0] < 300:
            counterRight += 1
            cv2.ellipse(img, (139, 360), (66, 66), 0, 0,
                        counterRight * selectionSpeed, (0, 255, 0), 20)
            if counterRight * selectionSpeed > 360:
                counterRight = 0
                if imageNumber < len(listShirts) - 1:
                    imageNumber += 1
        # Left hand gesture for changing shirts
        elif lmList[15][0] > 900:
            counterLeft += 1
            cv2.ellipse(img, (1138, 360), (66, 66), 0, 0,
                        counterLeft * selectionSpeed, (0, 255, 0), 20)
            if counterLeft * selectionSpeed > 360:
                counterLeft = 0
                if imageNumber > 0:
                    imageNumber -= 1
        else:
            counterRight = 0
            counterLeft = 0

    # Show the image
    cv2.imshow("Image", img)
    
    # Exit if the user presses the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
