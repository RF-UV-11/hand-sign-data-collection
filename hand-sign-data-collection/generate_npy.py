import cv2
import mediapipe as mp
import pandas as pd
import numpy as np
import os

# Initialize MediaPipe Hands model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

def extract_hand_keypoints(results):
    """
    Extracts hand keypoints (x, y, z coordinates) from MediaPipe Hand landmarks.

    Args:
        results (mediapipe.Hands): Results containing hand landmarks.

    Returns:
        np.array: Array of hand keypoints for detected hands.
                  Each row represents keypoints for a single hand (21 landmarks x 3 coordinates).
    """
    keypoints = []
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            hand_keypoints = np.array([[landmark.x, landmark.y, landmark.z] for landmark in hand_landmarks.landmark]).flatten()
            keypoints.append(hand_keypoints)
    return np.array(keypoints) if keypoints else np.zeros((0, 63))  # 21 landmarks * 3 coordinates = 63 keypoints per hand

def process_video(video_path, save_dir='data'):
    """
    Processes a video, extracts hand keypoints using MediaPipe Hands, and saves keypoints as .npy files.

    Args:
        video_path (str): Path to the input video file.
        save_dir (str): Directory to save extracted keypoints.

    Returns:
        None
    """
    cap = cv2.VideoCapture(video_path)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    target_frame_count = 30  # Extract keypoints from 30 frames
    frame_skip_count = max(frame_count // target_frame_count, 1)

    # Create directory to save keypoints
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    save_path = os.path.join(save_dir, video_name)
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    frame_number = 0
    while cap.isOpened() and frame_number < target_frame_count:
        # Set frame position to skip frames
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number * frame_skip_count)

        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Process frame with MediaPipe Hands
        results = hands.process(frame_rgb)

        # Extract hand keypoints
        hand_keypoints = extract_hand_keypoints(results)
        # Save hand keypoints as .npy file
        npy_filename = f'keypoints_{frame_number+1:02d}.npy'
        npy_filepath = os.path.join(save_path, npy_filename)
        np.save(npy_filepath, hand_keypoints)

        frame_number += 1

    cap.release()
    cv2.destroyAllWindows()

def main():
    """
    Main function to process videos listed in a DataFrame and extract hand keypoints.
    """
    # Prompt user to enter camera choice (1 or 2)
    camera_choice = input("Enter camera choice (front or back): ")

    if camera_choice not in ["front","back"]:
        print("Please choose from front or back")
        return
    # Load DataFrame containing video paths
    csv_file_path = f"data_{camera_choice}.csv"
    df = pd.read_csv(csv_file_path)

    # Process each video in the DataFrame
    for video_path in df['Video_Path']:
        process_video(video_path)

    print("Hand keypoints extraction completed.")

if __name__ == "__main__":
    main()
