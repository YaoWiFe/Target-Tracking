from ultralytics import YOLO

# Load a model
model = YOLO("yolov8n.yaml")  # build a new model from YAML
model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)
model = YOLO("yolov8n.yaml").load("yolov8n.pt")  # build from YAML and transfer weights

# Train the model
if __name__ == "__main__":
    model.train(
        cfg="ultralytics/cfg/default.yaml",
        data="c:/Users/ASUS/Desktop/CVtask/mydata/data/dataSet/data.yaml",
        optimizer="SGD",
        epochs=1,
        imgsz=640,
    )
