# 将AllTpye.txt文本转换成所需要的yaml文本
import yaml

source = "c:/Users/ASUS/Desktop/CVtask/mydata/Alltype.txt"
train = "c:/Users/ASUS/Desktop/CVtask/mydata/data/dataSet/train"
val = "c:/Users/ASUS/Desktop/CVtask/mydata/data/dataSet/val"
test = "c:/Users/ASUS/Desktop/CVtask/mydata/data/dataSet/test"
save_path = "c:/Users/ASUS/Desktop/CVtask/mydata/data/dataSet/"

names = {}
myset = {}

index = 0
with open(source, "r") as file:
    # 逐行存入列表
    lines = file.readlines()
    for line in lines:
        names[index] = line.strip()
        index += 1

myset["train"] = train
myset["val"] = val
myset["test"] = test
myset["names"] = names
myset["nc"] = index

with open(save_path + "data.yaml", "w") as file:
    yaml.dump(myset, file)
