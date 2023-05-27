# AI_Volumn_Hand_Control
This project is called AI Hand Volume Control. It is an application that uses computer vision and hand tracking to control the volume of the audio output using hand gestures. The project utilizes the following technologies and concepts:

1. OpenCV: The OpenCV library is used for image and video processing. It provides functions for webcam access, image manipulation, and drawing on images.

2. Hand Tracking: The project includes a custom module called "ch1_HandTracking," which uses the OpenCV library to detect and track the user's hand in real-time.

3. Audio Control: The project utilizes the "pycaw" library to interact with the Windows Core Audio API. It retrieves the system's audio output device and allows control over the volume levels.

4. Gesture-Based Volume Control: The application tracks the position of specific landmarks on the hand (such as fingertips) and calculates the distance between them. The distance is then mapped to a volume range, and the volume level is adjusted accordingly.

5. Visual Feedback: The application displays a live video feed from the webcam, with the hand landmarks and a line connecting them. Additionally, it shows a vertical bar representing the volume level and a numerical value indicating the percentage of the volume.

Users can control the volume by moving their hand closer or farther apart. The distance between the landmarks determines the volume level, with closer distances resulting in higher volumes and vice versa.

Overall, this project demonstrates the integration of computer vision, hand tracking, and audio control to create a gesture-based volume control system. It offers a hands-free and intuitive way to adjust the audio output using hand gestures.
