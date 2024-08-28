# 获取目标的类别数目和具体类别列表
import json

path = "c:/Users/ASUS/Desktop/CVtask/data_train_new.json"
save_path = "c:/Users/ASUS/Desktop/CVtask/mydata/"
# 创建一个空集合存储物品
mytitle = set()
with open(path, "r") as f:
    data = json.load(f)

file = open(save_path + "Alltype.txt", "w")
clips = data["clips"]
for clip in clips:
    annotations = clip["annotations"]
    for annotation in annotations:
        object_title = str(annotation["object_title"])
        if object_title not in mytitle:
            mytitle.add(object_title)
            file.write(object_title + "/n")
        else:
            pass
