import tkinter as tk
from tkinter import ttk
import cv2
import os
import time
import glob
import string

# Define a list of all alphanumeric characters (letters and digits)
FULL_ALPHANUMERIC_LIST = list(string.ascii_lowercase) + list(string.ascii_uppercase) + list(string.digits)

class VideoRecorderApp:
    """A GUI application for recording videos from two cameras simultaneously."""

    def __init__(self, root):
        """Initialize the VideoRecorderApp."""
        self.root = root
        self.root.title("Video Recorder App")
        self.root.configure(bg="black")  # Set background color to black

        self.record_duration = 30  # Duration to record in seconds
        self.fps = 30  # Frames per second for video recording
        self.camera1 = None  # First camera (e.g., built-in camera)
        self.camera2 = None  # Second camera (e.g., USB webcam)

        self.create_gui()

    def create_gui(self):
        """Create the graphical user interface (GUI) for the application."""
        # Create a frame to hold the buttons
        button_frame = ttk.Frame(self.root, padding="20")
        button_frame.pack(expand=True, fill="both")

        # Configure grid layout for button frame
        button_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)

        # Create buttons dynamically for each alphanumeric character
        for idx, name in enumerate(FULL_ALPHANUMERIC_LIST):
            row = idx // 10
            col = idx % 10

            button = tk.Button(button_frame, text=name, width=5, height=2, bg="green", fg="black")
            button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            button.config(command=lambda n=name: self.start_recording_with_delay(n, button))

        # Center the button frame within the root window
        button_frame.update_idletasks()
        frame_width = button_frame.winfo_width()
        frame_height = button_frame.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_offset = (screen_width - frame_width) // 2
        y_offset = (screen_height - frame_height) // 2
        self.root.geometry(f"+{x_offset}+{y_offset}")

    def select_cameras(self):
        """Initialize the camera objects for both Camera 1 front (built-in) and Camera 2 back (USB webcam)."""
        self.camera1 = cv2.VideoCapture(0)  # Open first camera (index 0 for built-in camera)
        self.camera2 = cv2.VideoCapture(2)  # Open second camera (index 2 for USB webcam)

    def start_recording_with_delay(self, button_name, button):
        """Start the recording process after a delay when a button is pressed."""
        # Disable the button during the delay
        button.config(state=tk.DISABLED)
        
        # Schedule the start_recording function after a delay of 3 seconds
        self.root.after(3000, lambda: self.start_recording(button_name, button))

    def start_recording(self, button_name, button):
        """Record videos from both cameras for the specified button."""
        # Initialize cameras if not already opened
        if self.camera1 is None or self.camera2 is None:
            self.select_cameras()

        # Define parent directories for camera recordings
        camera1_parent_directory = os.path.join("hand_sign_data", "front")
        camera2_parent_directory = os.path.join("hand_sign_data", "back")
        os.makedirs(camera1_parent_directory, exist_ok=True)
        os.makedirs(camera2_parent_directory, exist_ok=True)

        # Define directories for the specific button within each camera parent directory
        camera1_directory = os.path.join(camera1_parent_directory, button_name)
        camera2_directory = os.path.join(camera2_parent_directory, button_name)
        os.makedirs(camera1_directory, exist_ok=True)
        os.makedirs(camera2_directory, exist_ok=True)

        # Check if the maximum number of videos (50) per button per camera is reached
        if len(glob.glob(os.path.join(camera1_directory, '*.mov'))) >= 50 or len(glob.glob(os.path.join(camera2_directory, '*.mov'))) >= 50:
            print(f"Reached maximum videos (50) for button '{button_name}'")
            # Re-enable the button if needed
            button.config(state=tk.NORMAL)
            return

        # Start recording videos from both cameras
        filename1 = f"{button_name}_{time.strftime('%Y%m%d_%H%M%S')}.mov"
        filepath1 = os.path.join(camera1_directory, filename1)

        filename2 = f"{button_name}_{time.strftime('%Y%m%d_%H%M%S')}.mov"
        filepath2 = os.path.join(camera2_directory, filename2)

        codec = cv2.VideoWriter_fourcc(*'avc1')  # H.264 codec

        out1 = cv2.VideoWriter(filepath1, codec, self.fps, (640, 480))  # Adjust resolution and fps for camera 1
        out2 = cv2.VideoWriter(filepath2, codec, self.fps, (640, 480))  # Adjust resolution and fps for camera 2

        start_time = time.time()

        while (time.time() - start_time) <= self.record_duration + 1:
            ret1, frame1 = self.camera1.read()
            ret2, frame2 = self.camera2.read()

            if not ret1 or not ret2:
                break

            out1.write(frame1)
            out2.write(frame2)

            # Display frames from both cameras (optional)
            # cv2.imshow('front', frame1)
            # cv2.imshow('back (USB Webcam)', frame2)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release video writer and camera resources
        out1.release()
        out2.release()
        cv2.destroyAllWindows()

        # Re-enable the button after recording completes
        button.config(state=tk.NORMAL)

if __name__ == "__main__":
    # Create the Tkinter root window and initialize the VideoRecorderApp
    root = tk.Tk()
    app = VideoRecorderApp(root)
    root.mainloop()
