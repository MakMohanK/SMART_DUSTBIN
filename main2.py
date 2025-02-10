import cv2
import threading

class VideoStream:
    def __init__(self, source=2):
        self.cap = cv2.VideoCapture(source)
        self.frame = None
        self.stopped = False
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        while not self.stopped:
            ret, frame = self.cap.read()
            if ret:
                self.frame = frame  

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True
        self.cap.release()

def detect_motion(prev_frame, frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    frame_diff = cv2.absdiff(prev_frame, gray)
    thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) < 500:
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return gray, frame

# Usage
vs = VideoStream()
ret, initial_frame = vs.cap.read()
if ret:
    prev_frame = cv2.cvtColor(initial_frame, cv2.COLOR_BGR2GRAY)
    prev_frame = cv2.GaussianBlur(prev_frame, (21, 21), 0)
else:
    prev_frame = None

while True:
    frame = vs.read()
    if frame is not None and prev_frame is not None:
        prev_frame, frame = detect_motion(prev_frame, frame)
        cv2.imshow("Live Stream", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vs.stop()
cv2.destroyAllWindows()
