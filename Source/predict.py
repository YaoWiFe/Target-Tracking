import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = model = YOLO(
    "C:/Users/ASUS/Desktop/CVtask/lab/runs/detect/train2/weights/best.pt"
)
# model = model = YOLO("yolov8-seg.yaml").load("yolov8n-seg.pt")

# Open the video file
video_path = (
    "c:/Users/ASUS/Desktop/CVtask/train_clips/0a7cef36-8d0d-4d5b-a2fa-020619292021.mp4"
)
cap = cv2.VideoCapture(video_path)
cv2.namedWindow("YOLOv8 Inference", cv2.WINDOW_NORMAL)
# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 inference on the frame
        results = model(frame)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        resized_frame = cv2.resize(
            annotated_frame[0], (800, 600)
        )  # 调整图像大小为800x600
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
