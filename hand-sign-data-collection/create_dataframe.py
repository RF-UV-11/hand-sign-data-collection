import os
import pandas as pd

# Function to collect video file paths from a specified root directory
def collect_video_paths(root_dir):
    """
    Traverse directories under the specified root directory and collect video file paths.
    
    Args:
        root_dir (str): Root directory path containing video files.
        
    Returns:
        list of dict: List of dictionaries containing 'Class' (directory name) and 'Video_Path' (file path).
    """
    video_data = []
    
    # Walk through directories and collect video file paths
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.mov'):
                # Extract class name from the immediate parent directory
                class_name = os.path.basename(dirpath)
                video_path = os.path.join(dirpath, filename)
                
                # Append class name and video path to the list
                video_data.append({'Class': class_name, 'Video_Path': video_path})
    
    return video_data

def main():
    # Prompt the user to choose a camera (1 or 2)
    camera_choice = input("Choose a camera (1 or 2): ")

    # Validate the user input and define the root directory based on the chosen camera
    if camera_choice == '1':
        root_dir = os.path.join("hand_sign_data", "front")
    elif camera_choice == '2':
        root_dir = os.path.join("hand_sign_data", "back")
    else:
        print("Invalid camera choice. Please choose either 1 or 2.")
        return

    # Collect video paths and create DataFrame
    video_data = collect_video_paths(root_dir)
    df = pd.DataFrame(video_data)

    # Save DataFrame to CSV file named data.csv
    csv_file_path = f"data_camera-{camera_choice}.csv"
    df.to_csv(csv_file_path, index=False)

    print(f"DataFrame successfully created and saved to '{csv_file_path}'.")

if __name__ == "__main__":
    main()
