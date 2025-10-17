"""
Face tracking utilities using OpenCV Haar cascades.

This module provides basic face and eye detection for video streams.
It uses pre-trained Haar cascade classifiers for real-time detection.

Features:
- Face detection in frames.
- Eye detection within faces.
- Drawing rectangles and labels on frames.

Dependencies:
- OpenCV (cv2) for image processing and cascades.

Usage:
- Call track_faces() in video processing loops.
- Returns list of face rectangles for further processing.
"""
import cv2


def track_faces(frame, source):
    """
    Detect faces and eyes in a video frame using Haar cascades.

    Draws rectangles around detected faces and eyes, adds labels.

    Args:
        frame: Video frame as numpy array (BGR format).
        source: Source identifier (string) for logging.

    Returns:
        List of face rectangles as (x, y, w, h) tuples.

    Notes:
        - Uses frontal face and eye cascade classifiers.
        - Modifies frame in-place for visualization.
        - Returns empty list if no faces detected.
    """
    # Load Haar cascade classifiers for face and eye detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    
    # Convert frame to grayscale for detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    # Process each detected face
    for (x, y, w, h) in faces:
        # Draw blue rectangle around face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        # Add "Face" label above rectangle
        cv2.putText(frame, "Face", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        
        # Define region of interest (ROI) for eye detection within face
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        
        # Detect eyes in the face ROI
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            # Draw green rectangle around each eye
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
            # Add "Eye" label above eye rectangle
            cv2.putText(roi_color, "Eye", (ex, ey - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    
    # Return list of face rectangles
    return faces