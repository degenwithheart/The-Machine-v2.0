# Facial Recognition Project

This project implements facial tracking and recognition using the DeepFace library. It captures video input, recognizes known faces, and stores unknown faces for further analysis. The system supports multiple cameras, face tracking, privacy masking, detailed logging, watchlist management, and system health monitoring.

## Project Structure

```
facial-recognition-project
├── src
│   ├── main.py               # Entry point of the application
│   ├── face_recognition.py   # Contains FaceRecognizer class
│   ├── face_tracking.py      # Contains FaceTracker class
│   ├── admin.py              # Admin functionalities and menu
│   └── utils
│       └── __init__.py       # Utility functions for image processing
├── facebase
│   ├── known_faces           # Directory for known face images
│   ├── unknown_faces         # Directory for unknown face images
│   └── watchlist             # Directory for watchlist face images
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd facial-recognition-project
   ```

2. **Install dependencies:**
   Make sure you have Python installed, then run:
   ```
   pip install -r requirements.txt
   ```

3. **Add known faces:**
   Place images of known faces in the `facebase/known_faces` directory. The images should be clear and well-lit for better recognition accuracy.

4. **Add watchlist faces:**
   Place images of faces to be watched in the `facebase/watchlist` directory. These faces will trigger alerts when detected.

5. **Run the application:**
   Execute the main script to start the facial recognition and tracking process:
   ```
   python src/main.py
   ```

## Usage Guidelines

- The application will open video feeds from your webcams.
- It will attempt to recognize faces in real-time.
- If an unknown face is detected, it will be saved in the `facebase/unknown_faces` directory for further analysis.
- The system supports multiple cameras for comprehensive monitoring.
- Privacy masking is implemented to blur or hide faces that are not of interest.
- Detailed logs of all face recognition events are maintained for auditing and analysis.
- Watchlist management allows administrators to manage faces of interest.
- System health monitoring ensures the system is running optimally.

## Admin Menu Options

1. **Add Known Face**: Add a new known face to the system.
2. **Delete Known Face**: Delete a known face from the system by ID.
3. **View Unknown Faces**: Display a list of all unknown faces stored in the system.
4. **View Logs**: Display the log of all detected faces.
5. **Clear Logs**: Clear the log of detected faces.
6. **View Face Data**: Display detailed information about all faces in the system.
7. **Delete Unknown Faces**: Delete all unknown faces from the system.
8. **Update Admin Face**: Update the admin face image used for authentication.
9. **Change Admin Password**: Change the admin password.
10. **System Status**: Display the current status of the system, including active cameras and system health.
11. **Manage Watchlist**: Manage the watchlist of faces of interest.
12. **Exit**: Exit the admin menu.

## Additional Information

- Ensure your webcams are functioning properly before running the application.
- You may need to adjust the image quality and lighting conditions for optimal performance.
- For any issues or contributions, please refer to the project's issue tracker.