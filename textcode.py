# coding=utf-8
import json
import os
import os.path as path
import numpy as np
from legent.utils.math import is_point_on_box
import re

#######################################################################################
#### 服务器远程连接
from legent import Environment, Action

env = Environment(env_path=None)
try:
    # Do anything here.
    # For example, we send a message to the client
    env.reset()
    env.step(Action(text = "I'm on the remote server."))
    while True:
        env.step()
finally:
    env.close()
#######################################################################################
#基本用法
# import json
# from legent import Environment, Action, Observation,ResetInfo
# env = Environment(env_path='auto')
# try:
#     env.reset(ResetInfo())
#     while True:
#         env.step()
# finally:
#     env.close()
#######################################################################################
# from sklearn.model_selection import train_test_split

#
# with open("scene.json", 'r') as file:
#     scene = json.load(file)
# instances = scene['instances']
# index_list = []
# for index in range(len(instances)):
#     if instances[index]["position"][1] > 3 and "House" not in instances[index]['prefab']:
#         index_list.append(index)
# index_list.reverse()
# for i in index_list:
#     print(scene['instances'][i]['prefab'])
#     scene['instances'].pop(i)
# with open("scene.json", 'w') as file:
#     json.dump(scene, file)


# with open("addressables.json", 'r') as file:
#     prefabs = json.load(file)
# for index,i in enumerate(prefabs["prefabs"]):
#     size = prefabs["prefabs"][index]["size"]
#     prefabs["prefabs"][index]["size"] = [size["x"],size["y"],size["z"]]
# with open("addressables.json", 'w') as file:
#     json.dump(prefabs, file)


# with open("json/scene.json", 'r') as file:
#     scene = json.load(file)
# prefabs = [i['name'] for i in prefabs["prefabs"]]
# print(prefabs)
# scene_prefab = [i["prefab"] for i in scene["instances"]]
# for i,name in enumerate(scene_prefab) :
#     if name not in prefabs:
#         print(i,name)


# with open("json/scene.json", 'r') as file:
#     scene = json.load(file)
# instances = scene['instances']
# id_name_dict = {}
# for index in range(len(instances)):
#     full_name = instances[index]["prefab"]
#     name = instances[index]["prefab"].split("_")[1]
#     id_name_dict[index] = [name, full_name]
# with open("json/id_name_dict.json", 'w') as file:
#     json.dump(id_name_dict, file)
# with open("json/scene.json", 'r') as file:
#     scene = json.load(file)
# with open("json/interactable.json", 'r') as file:
#     save_dict = json.load(file)
# target = save_dict["target"]
# delete = []
# for i,id in enumerate(target):
#     if "Plant" in scene["instances"][id]["prefab"].split("_")[1] or\
#             "Sofa" in scene["instances"][id]["prefab"].split("_")[1]:
#         delete.append(i)
#         print(id)
#     if "Bed" in scene["instances"][id]["prefab"].split("_")[1] and \
#             "BedTab" not in scene["instances"][id]["prefab"].split("_")[1]:
#         # print(id)
#         pass
# for i in list(reversed(delete)):
#     target.pop(i)
# save_dict["target"] = target
# with open("json/interactable.json", 'w') as file:
#     json.dump(save_dict, file)

# "goto": ['goto'],
# "take": ["take"],
# "bring":["bring"],
# "exist":["exist_yes"],
# "where": ["where"],

# name = "put3520_2.png"
# task_num = name.split("_")[0]
# index = task_num.split("put")[1]
# print(index)
# raise()
# import os
#
# files = os.listdir("D:\legent\LEGENT\.legent\\train")
# goto = 0
# take = 0
# bring = 0
# exist = 0
# where = 0
# exist_yes = 0
# put = 0
#
# take_list = []
# bring_list = []
# goto_list = []
# exist_yes_list = []
# exist_list = []
# where_list = []
# put_list = []
# for file in files:
#     if "goto" in file:
#         goto += 1
#         if file.split("_")[0] not in goto_list:
#             goto_list.append(file.split("_")[0])
#     elif "take" in file:
#         take += 1
#         if file.split("_")[0] not in take_list:
#             take_list.append(file.split("_")[0])
#     elif "bring" in file:
#         bring += 1
#         if file.split("_")[0] not in bring_list:
#             bring_list.append(file.split("_")[0])
#     elif "where" in file:
#         where += 1
#         if file.split("_")[0] not in where_list:
#             where_list.append(file.split("_")[0])
#     elif "put" in file:
#         put += 1
#         if file.split("_")[0] not in put_list:
#             put_list.append(file.split("_")[0])
#     elif "exist" in file and "exist_yes" not in file:
#         exist += 1
#         if file.split("_")[0] not in exist_list:
#             exist_list.append(file.split("_")[0])
#     elif "exist_yes" in file:
#         exist_yes += 1
#         if file.split("_")[1] not in exist_yes_list:
#             exist_yes_list.append(file.split("_")[1])
# print("goto task number:",len(goto_list),"data number:",goto)
# print("take task number:",len(take_list),"data number:",take)
# print("bring task number:",len(bring_list),"data number:",bring)
# print("where task number:",len(where_list),"data number:",where)
# print("put task number:",len(put_list),"data number:",put)
# print("exist task number:",len(exist_list),"data number:",exist)
# print("exist_yes task number:",len(exist_yes_list),"data number:",exist_yes)

# with open("json/color.json", 'w') as file:
#     json.dump(lym, file)
# lym = "Is there a {object_name} in the {on_name}?"
# split_task = lym.split(" the ")
# object_id = split_task[0][11:-3]
# target_id = split_task[1][:-1]
# print(object_id,"***",target_id,"***")
# raise()
# ######################################################################################
# with open("result/data/put.json", 'r') as file:
#     put = json.load(file)
# with open("json/history_task.json", 'r') as file:
#     history_task = json.load(file)
# history_put = []
# for data in put:
#     task = data["task"]
#     split_task = task.split(" on the ")
#     object_id = data["id"]
#     target_id = split_task[1][:-1]
#     if [object_id, target_id] not in history_put:
#         history_put.append([object_id, target_id])
# history_task["put"] = history_put
# with open("json/history_task.json", 'w') as file:
#     json.dump(history_task, file)
#
# with open("result/data/exist.json", 'r') as file:
#     exist = json.load(file)
# with open("json/history_task.json", 'r') as file:
#     history_task = json.load(file)
# history_put = []
# for data in exist:
#     task = data["task"]
#     split_task = task.split(" the ")
#     object_id = split_task[0][11:-3]
#     target_id = split_task[1][:-1]
#     if [object_id, target_id] not in history_put:
#         history_put.append([object_id, target_id])
# history_task["exist"] = history_put
# with open("json/history_task.json", 'w') as file:
#     json.dump(history_task, file)

# with open("result/data/where.json", 'r') as file:
#     where = json.load(file)
# with open("json/history_task.json", 'r') as file:
#     history_task = json.load(file)
# history_put = []
# for i, data in enumerate(where):
#     if i % 11 == 0:
#         task = data["task"]
#         split_task = task.split(" the ")
#         object_id = data["id"]
#         history = [object_id]
#         for plan in data["plan"]:
#             if "Reply to the user:" in plan:
#                 history.append(plan.split(" on the ")[1][:-1])
#         if history not in history_put:
#             history_put.append(history)
#         print(i)
# history_task["where"] = history_put
# with open("json/history_task.json", 'w') as file:
#     json.dump(history_task, file)
###################################################################################
# import re
#
# ret = re.match("Is there a (.*) [i,o]n the (.*)\?", "Is there a {object_name} on the {on_name}?")
# print(ret.group(1))
# print(ret.group(2))
# jsons = os.listdir("/home/liyanming/work/legent/legent_python/result/")
# sum_num = 0
# for json_f in jsons:
#     if "json" in json_f:
#         with open(path.join("/home/liyanming/work/legent/legent_python/result/", json_f), 'r') as file:
#             data = json.load(file)
#         data_train, data_test = train_test_split(data, test_size=0.2, random_state=5)
#         print("task:", json_f[:-5], len(data))
#         # print("train:",len(data_train))
#         # print("test:",len(data_test))
#         sum_num += len(data)
#         with open(path.join("/home/liyanming/work/legent/legent_python/result/train",json_f[:-5]+"_train.json"), 'w') as file:
#             json.dump(data_train, file)
#         with open(path.join("/home/liyanming/work/legent/legent_python/result/test",json_f[:-5]+"_test.json"), 'w') as file:
#             json.dump(data_test, file)
# print("all:", sum_num)
###################################################################################
# with open("json/scene.json", 'r') as file:
#     scene = json.load(file)
# with open("addressables.json", 'r') as file:
#     prefabs = json.load(file)["prefabs"]
# prefabs = {prefab["name"]: prefab for prefab in prefabs}
#
#
# def get_on_which_object(scene, object_id):
#     on_candidates = []
#     object_pos = scene["instances"][object_id]["position"]
#     on_id, on_name = None, None
#     # get all candidates Floor->Table->Plate->Apple, [Floor, Table, Plate]
#     for i, instance in enumerate(scene["instances"]):
#         # TODO: get size from observation.game_states
#         pos, size, rot = np.array(instance["position"]), np.array(prefabs[instance["prefab"]]["size"]), np.array(
#             instance["rotation"])
#         if i != object_id and is_point_on_box(object_pos, pos, size, box_rotation=rot):  # TODO: consider more
#             on_candidates.append(i)
#     max_y = -100
#     on_id = None
#     for i in on_candidates:
#         if scene["instances"][i]["position"][1] > max_y:
#             max_y = scene["instances"][i]["position"][1]
#             on_id = i
#
#     if on_id is not None:
#         on_name = scene["instances"][on_id]["prefab"].split("LowPolyInterior2_")[1]
#     if on_id is None and on_name is None:
#         on_id = 0
#         on_name = "House4"
#     # if str(on_id) in docker.keys():
#     #     on_name = docker[str(on_id)]["name"]
#     return on_id, on_name
#
#
# on_dict = {}
# num = 0
# for i in range(len(scene["instances"])):
#     on_dict[str(i)] = []
# for i in range(len(scene["instances"])):
#     on_id, on_name = get_on_which_object(scene, i)
#     if i not in on_dict[str(on_id)]:
#         on_dict[str(on_id)].append(i)
#     if on_id != 0:
#         num += 1
# print(num)
# with open("json/interactable.json", 'r') as file:
#     interactable = json.load(file)
# interactable["on"] = on_dict
# with open("json/interactable.json", 'w') as file:
#     json.dump(interactable, file)
######################################################################################################、
# # 拆分数据集
# jsons = os.listdir("result/original")
# for json_name in jsons:
#     if "json" not in json_name:
#         continue
#     print(json_name)
#     with open(path.join("result/original", json_name), 'r') as file:
#         data = json.load(file)
#     data_num = len(data)
#     train_num = data_num * 0.8
#     data_dict = {}
#     for sample in data:
#         if sample["task"] not in data_dict.keys():
#             data_dict[sample["task"]] = [sample]
#         else:
#             data_dict[sample["task"]].append(sample)
#     print("data_dict done")
#     num = 0
#     flag = "train"
#     train_data = []
#     test_data = []
#     for key in data_dict.keys():
#         if flag == "train":
#             train_data.extend(data_dict[key])
#             num+=len(data_dict[key])
#             if num >=train_num:
#                 flag ="test"
#         elif flag == "test":
#             test_data.extend(data_dict[key])
#         else:
#             raise Exception('error')
#         # print(num)
#     with open(path.join("result/train",json_name[:-5]+"_train.json"), 'w') as file:
#         json.dump(train_data, file)
#     with open(path.join("result/test",json_name[:-5]+"_test.json"), 'w') as file:
#         json.dump(test_data, file)

#计数
# jsons = os.listdir("result/original")
# for json_name in jsons:
#     with open(path.join("result/original", json_name), 'r') as file:
#         data = json.load(file)
#     print(json_name,":",len(data))
# print("\n\n")
# jsons = os.listdir("result/train")
# for json_name in jsons:
#     with open(path.join("result/train", json_name), 'r') as file:
#         data = json.load(file)
#     print(json_name,":",len(data))
# print("\n\n")
# jsons = os.listdir("result/test")
# for json_name in jsons:
#     with open(path.join("result/test", json_name), 'r') as file:
#         data = json.load(file)
#     print(json_name,":",len(data))

##检查重复
# train=[]
# test=[]
# jsons = os.listdir("result/train")
# for json_name in jsons:
#     if "json" not in json_name:
#         continue
#     with open(path.join("result/train", json_name), 'r') as file:
#         data = json.load(file)
#     for num1,i in enumerate(data):
#         if i["task"] not in train:
#             train.append(i["task"])
#         print(num1)
# # jsons = os.listdir("result/test")
# # for json_name in jsons:
# #     if "json" not in json_name:
# #         continue
# #     with open(path.join("result/test", json_name), 'r') as file:
# #         data = json.load(file)
# #     for num2,i in enumerate(data):
# #         if i["task"] not in test:
# #             test.append(i["task"])
# #         print(num2)
# with open("test/put.json", 'r') as file:
#     data = json.load(file)
# for num2,i in enumerate(data):
#     if i["task"] not in test:
#         test.append(i["task"])
#     print(num2)
# print("aaaa:",list(set(train) & set(test)))

##检查数据内部重复
# jsons = os.listdir("result/original")
# for json_name in jsons:
#     print(json_name)
#     if "bring" in json_name:
#         continue
#     with open(path.join("result/original", json_name), 'r') as file:
#         data = json.load(file)
#     content = []
#     for i,dat in enumerate(data):
#         if i%100==0:
#             print(i)
#         if {"task": dat["task"],"robot_room":dat["robot_room"],"plan": dat["plan"],"id":dat["id"]} not in content:
#             content.append({"task": dat["task"],"robot_room":dat["robot_room"],"plan": dat["plan"],"id":dat["id"]})
#         else:
#             print(dat)

# def result_correct(truth, answer):
#     truth = truth.lower()
#     answer = answer.lower()
#     if truth == answer:
#         return True
#     else:
#         return False
#
#
# with open("oldtest/test_epochbest_rank0.json", 'r') as f:
#     data = json.load(f)
# with open("oldtest/test.json", 'r') as f:
#     groundtruth = json.load(f)
# result = {}
# test = []
# for i in ["goto", "put", "take", "where", "bring", "exist"]:
#     result[i] = 0  #correct = 0  wrong = 0
# for i, llm_answer in enumerate(data):
#     task = ""
#     for t in result.keys():
#         if t in llm_answer["task_id"][0]:
#             task = t
#     truth = groundtruth[i]
#     if truth["task_id"] == llm_answer["task_id"][0]:
#         if result_correct(truth["text_output"], llm_answer["caption"]):
#             llm_answer["task_id"] = llm_answer["task_id"][0]
#             llm_answer["task"] = truth["task_name"]
#             llm_answer["robot_room"] = truth["scene"][:-6]
#             llm_answer["plan"] = llm_answer["caption"].split("\n")
#             result[task] += 1
#             test.append(llm_answer)
# with open("演示任务.json", 'w') as file:
#     json.dump(test, file)
# from multiprocessing import  Process
#
# def fun1(i):
#     print(f'测试{i}多进程')
#
# if __name__ == '__main__':
#     print(sorted(os.listdir("KG/KG_image")))
    # process_list = []
    # for i in range(5):  #开启5个子进程执行fun1函数
    #     p = Process(target=fun1,args=(i,)) #实例化进程对象
    #     p.start()
    #     process_list.append(p)
    #
    # # for i in process_list:
    # #     i.join()
    #
    # print('结束测试')