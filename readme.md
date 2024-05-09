

# 🤝 Hand Sign Data Collection and Keypoint Extraction

This Python application facilitates the collection of hand sign language data using two different camera perspectives (front and back) and extracts hand keypoints using the MediaPipe Hands model for further analysis or machine learning tasks.

## 🚀 Features

- **Simultaneous Video Recording**: Captures hand sign videos from two different camera perspectives (front and back) simultaneously.
- **Graphical User Interface (GUI)**: Provides a user-friendly interface with buttons representing alphanumeric characters for initiating video recordings.
- **Automatic Data Organization**: Organizes recorded videos into directories based on camera perspectives ( `front` for web and `back` for smart glasses ) and button presses.
- **Hand Keypoint Extraction**: Utilizes the MediaPipe Hands model to detect and extract hand keypoints (x, y, z coordinates) from recorded videos.
- **Data Processing**: Converts extracted hand keypoints into numpy files (.npy) for each video frame, allowing for further analysis or model training.

## 🛠️ Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/hand-sign-data-collection.git
   ```

2. **Navigate to the Project Directory:**
   ```bash
   cd hand-sign-data-collection
   ```

3. **Install Dependencies:**
   - Ensure Python 3.x is installed.
   - Install required packages via pip:
     ```bash
     pip install -r requirements.txt
     ```

## 🎬 Usage

1. **Run the Application:**
   ```bash
   python hand_sign_data_collection.py
   ```

2. **Graphical User Interface (GUI):**
   - Click on the buttons (letters/digits) in the GUI to start recording hand sign videos.
   - Videos are saved in the `hand_sign_data` directory, categorized by camera perspective `front` or `back` and button pressed.

3. **Extract Hand Keypoints:**
   - After collecting videos, use `generate_npy.py` to process and extract hand keypoints from recorded videos.
     ```bash
     python generate_npy.py
     ```

## 📋 Directory Structure

```
hand-sign-data-collection/
│
├── hand_sign_data/
│   ├── front/
│   │   ├── A/
│   │   │   ├── video1.mov
│   │   │   └── ...
│   │   ├── B/
│   │   └── ...
│   └── back/
│       ├── A/
│       └── ...
│
├── create_dataframe.py
├── generate_npy.py
├── hand_sign_data_collection.py
├── data_camera1.csv
└── data_camera2.csv
```

- `hand_sign_data/`: Main directory for storing recorded videos and extracted data.
  - `front/`: Videos captured from the front camera perspective.
  - `back/`: Videos captured from the back camera perspective.
- `create_dataframe.py`: Script to create a DataFrame `data_front.csv` and `data_back.csv` from collected video paths.
- `generate_npy.py`: Script to process videos and extract hand keypoints as numpy files (.npy).
- `hand_sign_data_collection.py`: Main script to run the hand sign data collection application.
- `data_front.csv`, `data_back.csv`: CSV files containing video paths for each camera perspective.

## 📹 Demo Video

Watch a demo video showcasing how to use this project to collect hand sign language data and extract hand keypoints:

[![Demo Video](https://youtube.com/shorts/F_BdaFYt7YE?si=0v-ONrf4nGR5brnO)](https://www.youtube.com/watch?v=VIDEO_ID_HERE)

## 🤝 Contributing

Contributions are welcome! If you encounter any issues or have suggestions for enhancements, please feel free to open an issue or submit a pull request. Here are a few ways you can contribute:
- Enhance the user interface (GUI) for better usability.
- Implement additional features such as real-time hand keypoints visualization.
- Optimize video processing and keypoint extraction algorithms.

## 📄 License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).
