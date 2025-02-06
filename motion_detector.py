import cv2
import numpy as np

# Initialize the video capture
cap = cv2.VideoCapture(2)

ret, frame1 = cap.read()
frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
frame1 = cv2.GaussianBlur(frame1, (21, 21), 0)

while True:
    ret, frame2 = cap.read()
    if not ret:
        break
    
    gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    
    diff = cv2.absdiff(frame1, gray)
    
    thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
    
    thresh = cv2.dilate(thresh, None, iterations=2)
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        if cv2.contourArea(contour) < 1000:  # Ignore small movements
            continue
        
        # Get bounding box for the detected motion
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)

        print("Motion Detected")

        # capture 50 images
        # get prdiction for 50 images in an json file 
        # find out highest confidence and assiciated class index
        # show the prediction.
    
    # Display the result
    cv2.imshow("Motion Detection", frame2)
    cv2.imshow("Threshold", thresh)
    
    # Update the previous frame
    frame1 = gray
    
    # Break loop on 'q' key press
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()