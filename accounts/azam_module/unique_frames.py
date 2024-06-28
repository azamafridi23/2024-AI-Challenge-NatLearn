import cv2
import os
import numpy as np

def extract_unique_frames(video_path, tmp_dir, interval=4, threshold=30, min_contour_area=500):
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    vidcap = cv2.VideoCapture(video_path)
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))
    success, prev_frame = vidcap.read()
    count = 0
    frames = []
    frame_number = 0
    
    if not success:
        print("Error: Could not read the first frame.")
        return frames

    while success:
        if frame_number % (interval * fps) == 0:
            if count == 0:
                frame_path = os.path.join(tmp_dir, f"frame{count}.jpg")
                cv2.imwrite(frame_path, prev_frame)     # save the first frame as JPEG file
                frames.append(frame_path)
                count += 1
            else:
                # Compute absolute difference between current frame and previous frame
                diff = cv2.absdiff(image, prev_frame)
                gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, thresh = cv2.threshold(gray_diff, threshold, 255, cv2.THRESH_BINARY)

                # Find contours to determine the extent of differences
                contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                significant_diff = sum(cv2.contourArea(contour) for contour in contours) > min_contour_area

                if significant_diff:
                    frame_path = os.path.join(tmp_dir, f"frame{count}.jpg")
                    cv2.imwrite(frame_path, image)     # save unique frame as JPEG file
                    frames.append(frame_path)
                    count += 1
                    prev_frame = image
        
        success, image = vidcap.read()
        frame_number += 1
    
    vidcap.release()
    print(f"Extracted {count} unique frames at intervals of {interval} seconds.")
    return frames

