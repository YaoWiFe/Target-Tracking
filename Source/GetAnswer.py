import json
import os

json_path = "E:/CVtask/data_test.json"
result_path = "E:/CVtask/cv-lab-main/result"
save_path = "E:/CVtask/cv-lab-main/result/answer.json"

# 类别值转为索引
type_path = "E:/CVtask/cv-lab-main/testclipsdata/testtype.txt"
with open(type_path, "r") as file:
    type_value = file.read().splitlines()

# 创建一个字典，将类别映射到索引号
type_index = {type_value: index for index, type_value in enumerate(type_value)}

# 读取 JSON 文件
with open(json_path, 'r') as file:
    data = json.load(file)

# 遍历所有 clips
for clip in data['clips']:
    clip_uid = clip["clip_uid"]
    for annotation in clip['annotations']:
        # 获取对象类别的索引
        object_title = annotation['object_title']
        class_value = type_index.get(object_title, None)

        # 检查类别是否存在于索引字典中
        if class_value is None:
            print(f"没有此类别")
            continue
        
        class_value = str(class_value)

        # 同类的文件目录
        sameclass_dir = os.path.join(result_path, clip_uid, class_value)

        # 检查文件夹是否存在
        if not os.path.exists(sameclass_dir):
            continue

        # 遍历该目录下的所有 JSON 文件
        for filename in os.listdir(sameclass_dir):
            if filename.endswith('.json'):
                each_path = os.path.join(sameclass_dir, filename)
                with open(each_path, 'r') as file:
                    each_data = json.load(file)
                
                # 检查是否有 it_track 键
                if 'it_track' not in annotation:
                    annotation['it_track'] = []
                
                # 将JSON文件中的信息添加到 it_track 列表中
                annotation['it_track'].append(each_data)

# 保存修改后的 JSON 文件
with open(save_path, 'w') as file:
    json.dump(data, file, indent=4)

print("JSON 文件已成功修改并保存。")
