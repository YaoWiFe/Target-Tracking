# 随机划分 训练集，验证集，测试集
import os
import random
import shutil

# 设置随机数种子
random.seed(123)

# 定义文件夹路径
root_dir = "D:/mydata/data"
image_dir = os.path.join(root_dir, "images")
label_dir = os.path.join(root_dir, "labels")
output_dir = "c:/Users/ASUS/Desktop/CVtask/mydata/data/dataSet/"

# 定义训练集、验证集和测试集比例
train_ratio = 0.7
val_ratio = 0.15
test_ratio = 0.15

# 获取所有图像文件和标签文件的文件名（不包括文件扩展名）(去掉隐藏文件)
image_filenames = [
    os.path.splitext(f)[0]
    for f in os.listdir(image_dir)
    if os.path.isfile(os.path.join(image_dir, f)) and not f.startswith(".")
]
label_filenames = [
    os.path.splitext(f)[0]
    for f in os.listdir(label_dir)
    if os.path.isfile(os.path.join(image_dir, f)) and not f.startswith(".")
]

# 随机打乱文件名列表
random.shuffle(image_filenames)

# 计算训练集、验证集和测试集的数量
total_count = len(image_filenames)
train_count = int(total_count * train_ratio)
val_count = int(total_count * val_ratio)
test_count = total_count - train_count - val_count

# 定义输出文件夹路径
train_image_dir = os.path.join(output_dir, "train", "images")
train_label_dir = os.path.join(output_dir, "train", "labels")
val_image_dir = os.path.join(output_dir, "val", "images")
val_label_dir = os.path.join(output_dir, "val", "labels")
test_image_dir = os.path.join(output_dir, "test", "images")
test_label_dir = os.path.join(output_dir, "test", "labels")

# 创建输出文件夹
os.makedirs(train_image_dir, exist_ok=True)
os.makedirs(train_label_dir, exist_ok=True)
os.makedirs(val_image_dir, exist_ok=True)
os.makedirs(val_label_dir, exist_ok=True)
os.makedirs(test_image_dir, exist_ok=True)
os.makedirs(test_label_dir, exist_ok=True)

# 将图像和标签文件划分到不同的数据集中
for i, filename in enumerate(image_filenames):
    if i < train_count:
        output_image_dir = train_image_dir
        output_label_dir = train_label_dir
    elif i < train_count + val_count:
        output_image_dir = val_image_dir
        output_label_dir = val_label_dir
    else:
        output_image_dir = test_image_dir
        output_label_dir = test_label_dir

    # 复制图像文件
    src_image_path = os.path.join(image_dir, filename + ".jpg")
    dst_image_path = os.path.join(output_image_dir, filename + ".jpg")
    shutil.copy(src_image_path, dst_image_path)

    # 复制标签文件
    src_label_path = os.path.join(label_dir, filename + ".txt")
    dst_label_path = os.path.join(output_label_dir, filename + ".txt")
    shutil.copy(src_label_path, dst_label_path)
