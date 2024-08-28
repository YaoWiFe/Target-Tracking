import cv2
from ultralytics import YOLO
import json
import os

json_path = "E:/CVtask/data_test.json"
video_path = "E:/CVtask/test_clips/"
save_path = "E:/CVtask/cv-lab-main/result/"

# 加载YOLOv8模型
model = YOLO('Yolov8n.pt')

# 打开json文件读取到data中
with open(json_path, "r") as f:
    data = json.load(f)

# 对每一个clips进行处理
clips = data["clips"]
for clip in clips:
    clip_uid = clip["clip_uid"]
    video_file = os.path.join(video_path, clip_uid + ".mp4")
    
    if not os.path.exists(video_file):
        print(f"Video file {video_file} does not exist. Skipping.")
        continue

    cap = cv2.VideoCapture(video_file)
    if not cap.isOpened():
        print(f"Cannot open video file {video_file}. Skipping.")
        continue
    
    # 循环遍历视频帧
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # 获取当前帧号
        frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

        # 在帧上运行YOLOv8追踪，持续追踪帧间的物体
        results = model.track(frame, persist=True)

        # 输出当前帧号和每次追踪推理结果的boxes
        print(f"Frame {frame_number}: {results[0].boxes}")

        # 写结果
        box = results[0].boxes
        cls = box.cls.tolist()  # 类别信息转换为列表
        cls = [int(x) for x in cls]  # 类别转为整型存储
        xyxy = box.xyxy.tolist()  # 坐标信息转换为列表
        xywh = box.xywh.tolist()  # 尺寸信息转换为列表
        
        # 统计每个 cls 的数量
        cls_count = {}
        for index, class_value in enumerate(cls):
            # 统计当前 cls 的数量
            cls_count[class_value] = cls_count.get(class_value, 0) + 1

            if index < len(xyxy) and index < len(xywh):
                # 构建 visual_crop 字典
                visual_crop = {
                    "frame_number": frame_number,
                    "x": xyxy[index][0],
                    "y": xyxy[index][1],
                    "width": xywh[index][2],
                    "height": xywh[index][3],
                    "exported_clip_frame_number": frame_number * 6
                }
                
                # 构建输出文件
                # 输出路径
                clip_dir = os.path.join(save_path, clip_uid)
                if not os.path.exists(clip_dir):
                    os.makedirs(clip_dir)
                class_dir = os.path.join(clip_dir, str(class_value))
                if not os.path.exists(class_dir):
                    os.makedirs(class_dir)
                
                # 构建自定义输出文件名
                output_file_name = f"frame_{frame_number}_cls_{class_value}_count_{cls_count[class_value]}.json"
                output_path = os.path.join(class_dir, output_file_name)
                
                object_data = {
                    "visual_crop": visual_crop
                }
                # 将合并后的值写入一个文本文件
                with open(output_path, 'w') as file:
                    json.dump(object_data, file, indent=4)

        # 在帧上展示结果
        annotated_frame = results[0].plot()

        # 在帧上显示当前帧号
        cv2.putText(annotated_frame, f"Frame: {frame_number}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        
        # 展示带注释的帧
        cv2.imshow("YOLOv8 Tracking", annotated_frame)
 
        # 如果按下'q'则退出循环
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # 释放视频捕获对象
    cap.release()
    # 关闭显示窗口
    cv2.destroyAllWindows()
