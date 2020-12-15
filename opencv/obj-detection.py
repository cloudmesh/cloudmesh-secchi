import cv2
# print(sys.version)
cap = cv2.VideoCapture('Yi-Site2-(1).mp4')

# tracker = cv2.TrackerMOSSE_create()
tracker = cv2.TrackerCSRT_create()
success, img = cap.read()
bbox = cv2.selectROI("Tracking", img, False)
tracker.init(img, bbox)


def drawBox(img, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x, y), ((x + w), (y + h)), (255, 0, 255), 3, 1)
    # pass


while True:

    timer = cv2.getTickCount()

    # print(timer)

    success, img = cap.read()
    success, bbox = tracker.update(img)

    if success:
        drawBox(img, bbox)
    else:
        cv2.putText(img, "LOST", (75, 50),
                    cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255))

    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    cv2.putText(img, str(int(fps)), (75, 50),
                cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255))

    cv2.imshow("Tracking", img)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break


def drawBox(img, bbox):
    x, y, w, h = bbox
    cv2.rectangle(img, (x, y), ((x + w), (y + h)), (255, 0, 255), 3, 1)
    # pass
