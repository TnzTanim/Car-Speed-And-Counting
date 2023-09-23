# Vehicle Speed and Counting System with YOLO and OpenCV

This Python project is designed to detect, track, and estimate the speed of vehicles in a video while counting how many vehicles pass through two designated lines in the video. Here's a detailed explanation of how it works:

## Overview

This project is like having a smart eye that can detect vehicles in a video, follow their movement, calculate their speeds, and count how many vehicles are coming and going.

## How It Works

1. **Vehicle Detection**: The code uses a pre-trained YOLO (You Only Look Once) model (`yolov8n.pt`) to recognize vehicles in the video. YOLO is like a smart camera that can identify different objects, including cars and trucks.

2. **Vehicle Tracking**: To keep tabs on the vehicles as they move, a custom tracking system is implemented. This tracker assigns a unique ID to each vehicle and follows them from one frame to the next.

3. **Speed Calculation**: The program calculates the speed of each vehicle by measuring how long it takes for a vehicle to cross between two lines in the video. These lines represent a certain distance, typically assumed to be 30 meters. By dividing this distance by the time taken, it estimates the vehicle's speed in kilometers per hour (km/h).

4. **Counting Vehicles**: The system keeps track of vehicles that cross the two lines in the video. When a vehicle crosses the first line, it's considered to be leaving, and when it crosses the second line, it's considered to be entering.

5. **Visualization**: You can watch the analysis unfold in real-time through an OpenCV window. Vehicles are marked with dots, and their speeds are displayed. The program also keeps a count of entering and leaving vehicles.

## Why It Might Not Be Perfect

- **Processing Speed**: The accuracy of speed calculations depends on the processing power of your computer. Faster computers can measure speed more accurately. Slower computers may produce less precise results.

- **Constant Speed Assumption**: The program assumes that vehicles move at a constant speed between the two lines. In reality, vehicle speeds may vary, leading to less accurate speed calculations.

- **Distance Assumption**: The distance between the two lines is typically set at 30 meters, but this value is often just an estimation. To increase accuracy, you may need to measure the actual distance between the lines in your video.

- **Adjustments for Specific Scenarios**: Depending on your video and the types of vehicles present, you might need to make adjustments to the program to enhance its performance for your specific situation. This could include fine-tuning detection parameters or handling different vehicle types.

## How to Use the Code

1. **Get the Code**: Download the code from the GitHub repository.

2. **Prepare Your Model**: Ensure you have a YOLO model file (`yolov8n.pt`) that can recognize vehicles. Place this model file in the same directory as the code.

3. **Configure the Video**: Change the video source by modifying the following line in the code: `cap = cv2.VideoCapture('2.mp4')`. Replace `'2.mp4'` with the path to your video file.

4. **Run the Main Script**: Execute the `Main.py` script provided in the repository, and it will open a window displaying the video. As the video plays, the program will start detecting vehicles, tracking them, estimating their speeds, and counting them.

5. **Review the Results**: In the OpenCV window, you'll see dots on vehicles, and the program will keep count of vehicles entering and leaving. Vehicle speeds are also displayed.

6. **Finish**: When you're done analyzing the video, close the window to exit the program.

Feel free to experiment with the code to adapt it to your specific needs and video scenarios.
