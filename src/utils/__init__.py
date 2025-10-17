"""
Image processing utilities for face recognition.

This module provides helper functions for image manipulation.
Used by face recognition and tracking modules.

Features:
- Image resizing and normalization.
- Face alignment using landmarks.
- Privacy masking for faces.
- Geometric transformations.

Dependencies:
- cv2 (OpenCV) for image processing.
- numpy for array operations.

Notes:
- Functions handle common image formats (JPEG, PNG).
- Alignment uses eye landmarks for rotation.
- Masking blacks out face regions for privacy.
"""
import cv2
import numpy as np

def resize_image(image, width, height):
    """
    Resize the image to the specified width and height.

    Args:
        image: Input image array (numpy).
        width: Target width in pixels.
        height: Target height in pixels.

    Returns:
        Resized image array.
    """
    return cv2.resize(image, (width, height))

def normalize_image(image):
    """
    Normalize the image to have pixel values between 0 and 1.

    Args:
        image: Input image array (uint8).

    Returns:
        Normalized image array (float32).
    """
    return image / 255.0

def align_face(image, landmarks):
    """
    Align the face in the image based on the provided landmarks.

    Uses eye landmarks to calculate rotation angle and center.
    Rotates image to level the eyes horizontally.

    Args:
        image: Input image array.
        landmarks: Dict with 'left_eye' and 'right_eye' coordinates.

    Returns:
        Aligned image array.
    """
    # Example implementation using eye landmarks
    left_eye = landmarks['left_eye']
    right_eye = landmarks['right_eye']

    # Calculate the angle between the eyes
    dY = right_eye[1] - left_eye[1]
    dX = right_eye[0] - left_eye[0]
    angle = np.degrees(np.arctan2(dY, dX)) - 180

    # Calculate the center of the eyes
    eyes_center = ((left_eye[0] + right_eye[0]) // 2, (left_eye[1] + right_eye[1]) // 2)

    # Get the rotation matrix
    M = cv2.getRotationMatrix2D(eyes_center, angle, 1)

    # Apply the affine transformation
    (h, w) = image.shape[:2]
    aligned_image = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC)

    return aligned_image

def apply_privacy_mask(image, face_regions):
    """
    Apply a privacy mask to the specified face regions in the image.

    Draws black rectangles over face areas to obscure identities.

    Args:
        image: Input image array.
        face_regions: List of tuples (x, y, w, h) for face bounding boxes.

    Returns:
        Masked image array with faces blacked out.
    """
    masked_image = image.copy()
    for (x, y, w, h) in face_regions:
        cv2.rectangle(masked_image, (x, y), (x+w, y+h), (0, 0, 0), -1)
    return masked_image