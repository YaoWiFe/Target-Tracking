import cv2
import json

# 此代码用于裁取视频的特定帧并保存为图片，这些图片将被用于yolov8模型训练

# 此文件用于翻译json文件，以适用于yolov8格式
# 文件，文件每一行为一个目标的信息，包括class, x_center, y_center, width, height格式
# 每个图像对应一个txt文件

path = "c:/Users/ASUS/Desktop/CVtask/data_train_new.json"
save_path = "D:/mydata/data/images/"
video_path = "c:/Users/ASUS/Desktop/CVtask/train_clips/"
label_path = "D:/mydata/data/labels/"
type_path = "c:/Users/ASUS/Desktop/CVtask/mydata/Alltype.txt"

mytitle = {}
types = {}

index = 0

# 打开alltype文档读取所有类别
with open(type_path, "r") as file:

    lines = file.readlines()
    for line in lines:
        types[line.strip()] = index
        index += 1

# 打开json文件读取到data中
with open(path, "r") as f:
    data = json.load(f)
# 对每一个clips进行初步提取
clips = data["clips"]
# 要对"visual_crop" 和 "lt_track"中的帧图片 同时提取
for clip in clips:
    clip_uid = clip["clip_uid"]
    annotations = clip["annotations"]
    cap = cv2.VideoCapture(video_path + clip_uid + ".mp4")
    for annotation in annotations:
        object_title = annotation["object_title"]
        visual_crop = annotation["visual_crop"]
        # 计算归一化的坐标值，yolov8要求
        yolo_x, yolo_y, yolo_w, yolo_h = (
            float(
                (visual_crop["x"] + visual_crop["width"] / 2)
                / visual_crop["original_width"]
            ),
            float(
                (visual_crop["y"] + visual_crop["height"] / 2)
                / visual_crop["original_height"]
            ),
            float(visual_crop["width"] / visual_crop["original_width"]),
            float(visual_crop["height"] / visual_crop["original_height"]),
        )
        if yolo_x > 1:
            yolo_x = 1
        if yolo_w > 1:
            yolo_w = 1
        if yolo_y > 1:
            yolo_y = 1
        if yolo_h > 1:
            yolo_h = 1
        # 设置读取帧的位置
        cap.set(cv2.CAP_PROP_POS_FRAMES, visual_crop["frame_number"] * 6)
        # 读取帧
        ret, img = cap.read()
        if not ret:
            print("没有此视频文件——" + clip_uid)
            break

        # 对图片命名，名称为object_title+出现的次数
        if mytitle.get(object_title) is None:
            mytitle[object_title] = 1
            cv2.imwrite(
                save_path + object_title + "_" + str(mytitle[object_title]) + ".jpg",
                img,
            )
            # 按照名称写入对应label文件
            with open(
                label_path + object_title + "_" + str(mytitle[object_title]) + ".txt",
                "w",
            ) as file:
                file.write(
                    str(types[object_title])
                    + " "
                    + str(yolo_x)
                    + " "
                    + str(yolo_y)
                    + " "
                    + str(yolo_w)
                    + " "
                    + str(yolo_h)
                )

        else:
            mytitle[object_title] += 1
            cv2.imwrite(
                save_path + object_title + "_" + str(mytitle[object_title]) + ".jpg",
                img,
            )
            with open(
                label_path + object_title + "_" + str(mytitle[object_title]) + ".txt",
                "w",
            ) as file:
                file.write(
                    str(types[object_title])
                    + " "
                    + str(yolo_x)
                    + " "
                    + str(yolo_y)
                    + " "
                    + str(yolo_w)
                    + " "
                    + str(yolo_h)
                )
        # 如果该注释片段中有跟踪轨迹，那么继续抽十帧（数据量过大）
        if "lt_track" in annotation:
            lt_track = annotation["lt_track"][:200]
            for part in lt_track:
                yolo_x, yolo_y, yolo_w, yolo_h = (
                    float((part["x"] + part["width"] / 2) / part["original_width"]),
                    float((part["y"] + part["height"] / 2) / part["original_height"]),
                    float(part["width"] / part["original_width"]),
                    float(part["height"] / part["original_height"]),
                )
                if yolo_x > 1:
                    yolo_x = 1
                if yolo_w > 1:
                    yolo_w = 1
                if yolo_y > 1:
                    yolo_y = 1
                if yolo_h > 1:
                    yolo_h = 1
                cap.set(cv2.CAP_PROP_POS_FRAMES, part["frame_number"] * 6)
                ret, img = cap.read()
                if not ret:
                    print("没有此视频文件——" + clip_uid)
                    break

                mytitle[object_title] += 1
                cv2.imwrite(
                    save_path
                    + object_title
                    + "_"
                    + str(mytitle[object_title])
                    + ".jpg",
                    img,
                )
                with open(
                    label_path
                    + object_title
                    + "_"
                    + str(mytitle[object_title])
                    + ".txt",
                    "a",
                ) as file:
                    file.write(
                        str(types[object_title])
                        + " "
                        + str(yolo_x)
                        + " "
                        + str(yolo_y)
                        + " "
                        + str(yolo_w)
                        + " "
                        + str(yolo_h)
                    )

    cap.release()
