# coding=utf-8
# 处理环境数据集图片
import os
import os.path as path
import json
import shutil
import re
import random

root = "D:\legent\LEGENT\.legent\data"
train_path = "D:\legent\LEGENT\.legent\data\\train"
test_path = "D:\legent\LEGENT\.legent\data\\test"
valid_path = "D:\legent\LEGENT\.legent\data\\valid"
graph_path = "graph"
train_jsons_path = "train_jsons"
train_jsons_path_cn = "train_jsons_cn"

if not path.exists(train_path):
    os.makedirs(train_path)
    os.makedirs(test_path)
    os.makedirs(valid_path)
    os.makedirs(path.join(train_path, graph_path))
    os.makedirs(path.join(test_path, graph_path))
    os.makedirs(path.join(valid_path, graph_path))

graphs = os.listdir("D:\legent\LEGENT\.legent\\train")
jsons = os.listdir("D:\legent\LEGENT\.legent\\train_jsons")
jsons_cn = os.listdir("D:\legent\LEGENT\.legent\\train_jsons_cn")
for train_json in jsons_cn:
    train_list = []
    test_list = []
    valid_list = []
    with open(path.join("D:\legent\LEGENT\.legent\\train_jsons_cn", train_json), 'r') as file:
        xx_train_json = json.load(file)
    for image_action in xx_train_json:
        image_name = image_action["image"]
        if "goto" in image_name:
            task_num = image_name.split("_")[0]
            index = task_num.split("goto")[1]
            if int(index) <= 82:
                train_list.append(image_action)
            elif 82 < int(index) <= 105:
                test_list.append(image_action)
            elif 105 < int(index) <= 117:
                valid_list.append(image_action)
        elif "take" in image_name:
            task_num = image_name.split("_")[0]
            index = task_num.split("take")[1]
            if int(index) <= 76:
                train_list.append(image_action)
            elif 76 < int(index) <= 98:
                test_list.append(image_action)
            elif 98 < int(index) <= 108:
                valid_list.append(image_action)
        elif "bring" in image_name:
            task_num = image_name.split("_")[0]
            index = task_num.split("bring")[1]
            if int(index) <= 76:
                train_list.append(image_action)
            elif 76 < int(index) <= 98:
                test_list.append(image_action)
            elif 98 < int(index) <= 108:
                valid_list.append(image_action)
        elif "put" in image_name:
            task_num = image_name.split("_")[0]
            index = task_num.split("put")[1]
            if int(index) <= 4638:
                train_list.append(image_action)
            elif 4638 < int(index) <= 5963:
                test_list.append(image_action)
            elif 5963 < int(index) <= 6626:
                valid_list.append(image_action)
        elif "where" in image_name:
            task_num = image_name.split("_")[0]
            index = task_num.split("where")[1]
            if int(index) <= 6914:
                train_list.append(image_action)
            elif 6914 < int(index) <= 8890:
                test_list.append(image_action)
            elif 8890 < int(index) <= 9877:
                valid_list.append(image_action)
        elif "exist" in image_name and "exist_yes" not in image_name:
            task_num = image_name.split("_")[0]
            index = task_num.split("exist")[1]
            if int(index) <= 2875:
                train_list.append(image_action)
            elif 2875 < int(index) <= 3696:
                test_list.append(image_action)
            elif 3696 < int(index) <= 4107:
                valid_list.append(image_action)
        elif "exist_yes" in image_name:
            task_num = image_name.split("_")[1]
            index = task_num.split("yes")[1]
            if int(index) <= 118:
                train_list.append(image_action)
            elif 118 < int(index) <= 152:
                test_list.append(image_action)
            elif 152 < int(index) <= 168:
                valid_list.append(image_action)
    task = train_json.split("_")
    if "exist_yes" in train_json:
        task_type = "exist_yes"
    else:
        task_type = task[0]
    train_file = task_type+"_train.json"
    test_file = task_type+"_test.json"
    valid_file = task_type+"_valid.json"
    with open(path.join("D:\legent\LEGENT\.legent\data\\train\json_cn", train_file), 'w') as file:
        json.dump(train_list, file)
    with open(path.join("D:\legent\LEGENT\.legent\data\\test\json_cn", test_file), 'w') as file:
        json.dump(test_list, file)
    with open(path.join("D:\legent\LEGENT\.legent\data\\valid\json_cn", valid_file), 'w') as file:
        json.dump(valid_list, file)
# for i,graph_name in enumerate(graphs):
#     print(i)
#     if "goto" in graph_name:
#         task_num = graph_name.split("_")[0]
#         index = task_num.split("goto")[1]
#         if int(index) <= 82:
#             shutil.copyfile(path.join("D:\legent\LEGENT\.legent\\train", graph_name),
#                             path.join(train_path, graph_path, graph_name))
#         elif 82 < int(index) <= 105:
#             shutil.copyfile(path.join("D:\legent\LEGENT\.legent\\train", graph_name),
#                             path.join(test_path, graph_path, graph_name))
#         elif 105 < int(index) <= 117:
#             shutil.copyfile(path.join("D:\legent\LEGENT\.legent\\train", graph_name),
#                             path.join(valid_path, graph_path, graph_name))
#     elif "take" in graph_name:
#         task_num = graph_name.split("_")[0]
#         index = task_num.split("take")[1]
#         if int(index) <= 76:
#             shutil.copyfile(path.join("D:\legent\LEGENT\.legent\\train", graph_name),
#                             path.join(train_path, graph_path, graph_name))
#         elif 76 < int(index) <= 98:
#             shutil.copyfile(path.join("D:\legent\LEGENT\.legent\\train", graph_name),
#                             path.join(test_path, graph_path, graph_name))
#         elif 98 < int(index) <= 108:
#             shutil.copyfile(path.join("D:\legent\LEGENT\.legent\\train", graph_name),
#                             path.join(valid_path, graph_path, graph_name))
#     elif "bring" in graph_name:
#         task_num = graph_name.split("_")[0]
#         index = task_num.split("bring")[1]
#         if int(index) <= 76:
#             shutil.copyfile(path.join("D:\legent\LEGENT\.legent\\train", graph_name),
#                             path.join(train_path, graph_path, graph_name))
#         elif 76 < int(index) <= 98:
#             shutil.copyfile(path.join("D:\legent\LEGENT\.legent\\train", graph_name),
#                             path.join(test_path, graph_path, graph_name))
#         elif 98 < int(index) <= 108:
#             shutil.copyfile(path.join("D:\legent\LEGENT\.legent\\train", graph_name),
#                             path.join(valid_path, graph_path, graph_name))
#     elif "put" in graph_name:
#         task_num = graph_name.split("_")[0]
#         index = task_num.split("put")[1]
#         if int(index) <= 4638:
#             shutil.copyfile(path.join("D:\legent\LEGENT\.legent\\train", graph_name),
#                             path.join(train_path, graph_path, graph_name))
#         elif 4638 < int(index) <= 5963:
#             shutil.copyfile(path.join("D:\legent\LEGENT\.legent\\train", graph_name),
#                             path.join(test_path, graph_path, graph_name))
#         elif 5963 < int(index) <= 6626:
#             shutil.copyfile(path.join("D:\legent\LEGENT\.legent\\train", graph_name),
#                             path.join(valid_path, graph_path, graph_name))
#     elif "where" in graph_name:
#         task_num = graph_name.split("_")[0]
#         index = task_num.split("where")[1]
#         if int(index) <= 6914:
#             shutil.copyfile(path.join("D:\legent\LEGENT\.legent\\train", graph_name),
#                             path.join(train_path, graph_path, graph_name))
#         elif 6914 < int(index) <= 8890:
#             shutil.copyfile(path.join("D:\legent\LEGENT\.legent\\train", graph_name),
#                             path.join(test_path, graph_path, graph_name))
#         elif 8890 < int(index) <= 9877:
#             shutil.copyfile(path.join("D:\legent\LEGENT\.legent\\train", graph_name),
#                             path.join(valid_path, graph_path, graph_name))
#     elif "exist" in graph_name and "exist_yes" not in graph_name:
#         task_num = graph_name.split("_")[0]
#         index = task_num.split("exist")[1]
#         if int(index) <= 2875:
#             shutil.copyfile(path.join("D:\legent\LEGENT\.legent\\train", graph_name),
#                             path.join(train_path, graph_path, graph_name))
#         elif 2875 < int(index) <= 3696:
#             shutil.copyfile(path.join("D:\legent\LEGENT\.legent\\train", graph_name),
#                             path.join(test_path, graph_path, graph_name))
#         elif 3696 < int(index) <= 4107:
#             shutil.copyfile(path.join("D:\legent\LEGENT\.legent\\train", graph_name),
#                             path.join(valid_path, graph_path, graph_name))
#     elif "exist_yes" in graph_name:
#         task_num = graph_name.split("_")[1]
#         index = task_num.split("yes")[1]
#         if int(index) <= 118:
#             shutil.copyfile(path.join("D:\legent\LEGENT\.legent\\train", graph_name),
#                             path.join(train_path, graph_path, graph_name))
#         elif 118 < int(index) <= 152:
#             shutil.copyfile(path.join("D:\legent\LEGENT\.legent\\train", graph_name),
#                             path.join(test_path, graph_path, graph_name))
#         elif 152 < int(index) <= 168:
#             shutil.copyfile(path.join("D:\legent\LEGENT\.legent\\train", graph_name),
#                             path.join(valid_path, graph_path, graph_name))
