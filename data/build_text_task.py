# coding=utf-8
# 生成训练及测试数据集
import os
import os.path as path
import json
import shutil
import re
import random
from typing import Literal
import numpy as np
from legent.utils.math import is_point_on_box
from sklearn.model_selection import train_test_split

#todo
#exist_no:1450
#所有=20000
#比例
robot_possable_pos = [
    [-1.1976431608200073, 0.1319998800754547, -4.5299391746521],
    [-4.9139251708984375, 0.14200010895729065, 2.9029886722564697],
    [2.641841173171997, 0.13199952244758606, 4.531292915344238],
    [5.847576141357422, 0.1319998800754547, -4.481896877288818],
    [2.2042901515960693, 0.13199952244758606, 2.1048526763916016],
    [4.261860370635986, 0.13199976086616516, 3.703007698059082],
    [-2.5636794567108154, 3.131999969482422, 0.13945524394512177],
    [0.5606305003166199, 3.1319994926452637, 4.489130020141602],
    [5.850497722625732, 3.1319994926452637, -1.0864429473876953],
    [3.361269474029541, 3.131999969482422, -2.1504874229431152],
    [-5.835768222808838, 3.490466594696045, -4.6003031730651855]
]
human_possable_pos = [
    [-5.0159010887146, 0.13199976086616516, -4.016477108001709],
    [-5.061328411102295, 0.13199973106384277, 4.476864337921143],
    [1.667828917503357, 0.13199973106384277, 3.2717766761779785],
    [1.6528249979019165, 0.13199985027313232, -1.1526516675949097],
    [3.8993852138519287, 0.13199996948242188, 0.49500057101249695],
    [5.607304573059082, 0.13199961185455322, 4.50911283493042],
    [-2.5674407482147217, 3.131999969482422, 2.9703996181488037],
    [3.180063486099243, 3.131999969482422, 0.6425180435180664],
    [4.204190254211426, 3.131999969482422, -3.2232816219329834],
    [-3.3540027141571045, 3.131999969482422, -4.601791858673096],
    [-5.123232364654541, 3.1319994926452637, -3.11215877532959]
]
robot = [
    "First Floor Living Room and Kitchen",
    "First Floor Bathroom1",
    "First Floor Cloakroom1",
    "First Floor Bedroom1",
    "First Floor Cloakroom2",
    "First Floor Bathroom2",
    "Second Floor Corridor",
    "Second Floor Bedroom1",
    "Second Floor Bathroom1",
    "Second Floor Bedroom2",
    "Second Floor Bathroom2"
]
human = [
    "First Floor Living Room and Kitchen",
    "First Floor Bathroom1",
    "First Floor Cloakroom1",
    "First Floor Bedroom1",
    "First Floor Cloakroom2",
    "First Floor Bathroom2",
    "Second Floor Corridor",
    "Second Floor Bedroom1",
    "Second Floor Bathroom1",
    "Second Floor Cloakroom2",
    "Second Floor Bathroom2"
]

with open("json/interactable.json", 'r') as file:
    save_dict = json.load(file)
# with open("json/scene.json", 'r') as file:
#     scene = json.load(file)
interactable_id = save_dict["interactable"]
upstair = save_dict["upstair"]
downstair = save_dict["downstair"]
docker = save_dict["docker"]
target = save_dict["target"]
box = save_dict["box"]
exist = save_dict["exist"]
unable_grab = [21, 95, 96, 136, 141, 143, 144, 145, 213, 214, 215, 266, 283, 295, 297, 315, 341, 389, 409]
interactable_id = list(set(interactable_id) - set(unable_grab))
floor = [7, 8, 9, 15, 16, 39, 40, 41, 42, 43,
         48, 50, 51, 66, 67, 68, 71, 82, 83, 84, 85, 112, 113, 114, 176, 183, 184, 196, 201, 205, 217, 218, 220, 228,
         229, 233, 234, 243, 241, 244, 268, 271, 274, 275, 312, 318, 328, 335, 336, 337, 343, 348, 353, 381, 382, 388,
         389, 390, 391, 405, 414, 415]
with open("json/addressables.json", 'r') as file:
    prefabs = json.load(file)["prefabs"]
prefabs = {prefab["name"]: prefab for prefab in prefabs}
color = {}
with open("json/properties.txt", "r", encoding='gbk') as f:
    for line in f.readlines():
        line = line.strip('\n')
        if "color" in line:
            text_list = line.split("...")
            object_color_name = text_list[0].split("LowPolyInterior2_")[1]
            object_color = text_list[2]
            color[object_color_name] = object_color

with open("json/scene_test.json", 'r') as file:
    scene_test_id = json.load(file)
with open("json/scene_train.json", 'r') as file:
    scene_train_id = json.load(file)
with open("json/scene.json", 'r') as file:
    scene = json.load(file)
scene_train = {"instances": [sce for i, sce in enumerate(scene["instances"]) if i in scene_train_id]}
scene_test = {"instances": [sce for i, sce in enumerate(scene["instances"]) if i in scene_test_id]}
scene_dict = {
    "train": scene_train,
    "test": scene_test
}
interactable_id_train = [i for i in interactable_id if i in scene_train_id]
interactable_id_test = [i for i in interactable_id if i in scene_test_id]
interactable_id_dict = {
    "train": interactable_id_train,
    "test": interactable_id_test
}
exist_train = [i for i in exist if i in scene_train_id]
exist_test = [i for i in exist if i in scene_test_id]
exist_dict = {
    "train": exist_train,
    "test": exist_test
}
target_train = [i for i in target if i in scene_train_id]
target_test = [i for i in target if i in scene_test_id]
target_dict = {
    "train": target_train,
    "test": target_test
}
# print(len(scene_train["instances"]), len(interactable_id_train), len(exist_train))
def get_on_which_object(scene, object_id):
    on_candidates = []
    object_pos = scene["instances"][object_id]["position"]
    on_id, on_name = None, None
    # get all candidates Floor->Table->Plate->Apple, [Floor, Table, Plate]
    for i, instance in enumerate(scene["instances"]):
        # TODO: get size from observation.game_states
        pos, size, rot = np.array(instance["position"]), np.array(prefabs[instance["prefab"]]["size"]), np.array(
            instance["rotation"])
        if i != object_id and is_point_on_box(object_pos, pos, size, box_rotation=rot):  # TODO: consider more
            on_candidates.append(i)
    if 0 in on_candidates:
        on_candidates.remove(0)
    max_y = -100
    on_id = None
    for i in on_candidates:
        if scene["instances"][i]["position"][1] > max_y:
            max_y = scene["instances"][i]["position"][1]
            on_id = i

    if on_id is not None:
        on_name = scene["instances"][on_id]["prefab"].split("LowPolyInterior2_")[1]
    # if on_id is None and on_name is None:
    #     on_id = 0
    #     on_name = "House4"
    if on_id is not None and "Sushi_roll" in on_name :
        on_id = 399
        on_name = "LowPolyInterior2_CuttingBoard_01"
    if str(on_id) in docker.keys():
        on_name = docker[str(on_id)]["name"]
    return on_id, on_name
#################################################################################################
#划分训练集和测试集
# def split_scene(scene):
#
#     objects = []
#     object_name = set()
#     for i, i_instance in enumerate(scene["instances"]):
#         if get_on_which_object(scene, i)[0] is None or get_on_which_object(scene, i)[0] == 0:
#             objects.append(i)
#             object_name.add(i_instance["prefab"])
#     print(len(scene["instances"]))
#     print(len(objects))
#     object_plate = [i for i in object_name if "Plate" in i]
#     object_name = object_name - set(object_plate)
#     scene_train_word, scene_test_word = train_test_split(list(object_name), test_size=0.3, random_state=42)
#     scene_train_word.extend(object_plate)
#     scene_train = [i for i in objects if scene["instances"][i]["prefab"] in scene_train_word]
#     scene_test = [i for i in objects if scene["instances"][i]["prefab"] in scene_test_word]
#     # for i in list(set(range(0, 417)) - set(scene_train) - set(scene_test)):
#     #     print(i,":",get_on_which_object(scene, i)[0])
#     while len(set(range(0, 417)) - set(scene_train) - set(scene_test)) != 0:
#         flag = 0
#         for i in list(set(range(0, 417)) - set(scene_train) - set(scene_test)):
#             # print(i)
#             if get_on_which_object(scene, i)[0] in scene_train:
#                 scene_train.append(i)
#                 flag = 1
#             elif get_on_which_object(scene, i)[0] in scene_test:
#                 scene_test.append(i)
#                 flag = 1
#         if flag == 0:
#             random_id = random.choice(list(set(range(0, 417)) - set(scene_train) - set(scene_test)))
#             scene_train.append(random_id)
#         print(len(set(range(0, 417)) - set(scene_train) - set(scene_test)))
#     return scene_train, scene_test
# #
# #
# scene_train, scene_test = split_scene(scene)
# print(set(scene_test) & set(scene_train))
# print(len(scene_train), len(scene_test))
# #347 70
# with open("json/scene_train.json", 'w') as file:
#     json.dump(scene_train, file)
# with open("json/scene_test.json", 'w') as file:
#     json.dump(scene_test, file)
# raise()
#################################################################################################
with open("json/history_task.json", 'r') as file:
    history_task = json.load(file)

#eg.pos = [1.0, 1.0, 1.0]
def get_room(pos):
    if -6.18 <= pos[0] <= 1.3 and pos[1] <= 2.5 and -5.01 <= pos[2] <= 2.60:
        room = "First Floor Living Room and Kitchen"  #
    elif -6.18 <= pos[0] <= -1.25 and pos[1] <= 2.5 and 2.60 <= pos[2] <= 5.01:
        room = "First Floor Bathroom1"  #
    elif -1.25 <= pos[0] <= 3.65 and pos[1] <= 2.5 and 2.60 <= pos[2] <= 5.01:
        room = "First Floor Cloakroom1"
    elif 1.3 <= pos[0] <= 6.18 and pos[1] <= 2.5 and -5.01 <= pos[2] <= 0:
        room = "First Floor Bedroom1"  #
    elif 1.3 <= pos[0] <= 6.18 and pos[1] <= 2.5 and 0 <= pos[2] <= 2.6:
        room = "First Floor Cloakroom2"  #
    elif 3.65 <= pos[0] <= 6.18 and pos[1] <= 2.5 and 2.6 <= pos[2] <= 5.01:
        room = "First Floor Bathroom2"  #
    elif -1.2 <= pos[0] <= 6.18 and pos[1] >= 2.5 and 0 <= pos[2] <= 5.01:
        room = "Second Floor Bedroom1"  #
    elif 3.67 <= pos[0] <= 6.18 and pos[1] >= 2.5 and -5.01 <= pos[2] <= 0:
        room = "Second Floor Bathroom1"
    elif -6.18 <= pos[0] <= -3.75 and pos[1] >= 2.5 and 2.6 <= pos[2] <= 5.01:
        room = "Second Floor Cloakroom1"
    elif (-3.75 <= pos[0] <= -1.2 and pos[1] >= 2.5 and -2.45 <= pos[2] <= 5.01) or \
            (-6.18 <= pos[0] <= -1.2 and pos[1] >= 2.5 and -2.45 <= pos[2] <= -0.15):
        room = "Second Floor Corridor"
    elif -1.2 <= pos[0] <= 3.67 and pos[1] >= 2.5 and -5.01 <= pos[2] <= 0:
        room = "Second Floor Bedroom2"  #
    elif -3.75 <= pos[0] <= -1.2 and pos[1] >= 2.5 and -5.01 <= pos[2] <= -2.45:
        room = "Second Floor Cloakroom2"  #
    elif -6.18 <= pos[0] <= -3.75 and pos[1] >= 2.5 and -5.01 <= pos[2] <= -2.45:
        room = "Second Floor Bathroom2"  #
    return room


# result = {}
# for jjj, i_instance in enumerate(scene["instances"]):
#     result[str(jjj)] = {
#         "on":[-1,None],
#         "in":None,
#         "inroom":None
#     }
#     i1, _ = get_on_which_object(scene, jjj)
#     if i1 is not None and get_room(scene["instances"][jjj]["position"]) != get_room(scene["instances"][i1]["position"]):
#         i1 = None
#     if i1 is not None:
#         lym = scene["instances"][i1]["prefab"]
#         if "Sushi_roll" in lym:
#             lym = "LowPolyInterior2_CuttingBoard_01"
#         result[str(jjj)]["on"] = [i1,lym]
#     lym = get_room(scene["instances"][jjj]["position"])
#     result[str(jjj)]["inroom"] = lym
#     if str(jjj) in docker.keys():
#         result[str(jjj)]["in"] = docker[str(jjj)]["name"]
#     print(f"{jjj}:{lym}")
# with open("lym.json", 'w') as file:
#     json.dump(result, file)
# raise()


def create_text_task(task_type, part_interactable, part_target, part_exist, scene=None, num=1):
    # TODO: verified the correctness of all cases
    global exist

    def get_random_object(scene):
        # object_candidates = []
        # for i, instance in enumerate(scene["instances"]):
        #     if instance["type"] == "interactable":
        #         object_candidates.append(i)
        object_id = random.choice(part_interactable)
        object_name = scene["instances"][object_id]["prefab"].split("LowPolyInterior2_")[1]
        # print(object_id, object_name)
        return object_id, object_name

    def get_random_target(scene, object_id):
        target_candidates = []
        # for i, instance in enumerate(scene["instances"]):
        #     if i != object_id and\
        #             "Floor" not in instance["prefab"] and\
        #             "Wall" not in instance["prefab"] and\
        #             i not in docker.keys():
        #         target_candidates.append(i)
        # target_id = random.choice(target_candidates)
        target_id = random.choice(part_target)
        target_name = scene["instances"][target_id]["prefab"].split("LowPolyInterior2_")[1]
        return target_id, target_name

    def get_random_place(scene):
        object_id = random.choice(interactable_id + target)
        object_name = scene["instances"][object_id]["prefab"].split("LowPolyInterior2_")[1]
        return object_id, object_name

    samples = []
    where_full = []
    for i in range(num):
        # generate (task, plan, solution) triplets
        robot_pos = random.choice(robot_possable_pos)
        human_pos = random.choice(human_possable_pos)
        robot_room = get_room(robot_pos)
        human_room = get_room(human_pos)
        if task_type == "come":
            task = "Come here."
            solution = ["goto_user()"]
            plan = ["Go to the user."]
        elif task_type == "put":
            while_i = 0
            while True:
                object_id, object_name = get_random_object(scene)
                target_id, target_name = get_random_target(scene, object_id)
                if [object_id, target_name] not in history_task["put"]:
                    history_task["put"].append([object_id, target_name])
                    break
                while_i+=1
                if while_i >150:
                    break
            if while_i >140:
                break
            # object_id = 355
            # object_name = scene["instances"][object_id]["prefab"].split("LowPolyInterior2_")[1]
            # target_id = 42
            # target_name = scene["instances"][target_id]["prefab"].split("LowPolyInterior2_")[1]
            for robot_pos in robot_possable_pos:
                robot_room = get_room(robot_pos)
                if str(target_id) in docker.keys():
                    task = f"Put the {object_name} in the {target_name}."
                else:
                    task = f"Put the {object_name} on the {target_name}."
                solution = []
                plan = []
                image = []
                on_id, on_name = get_on_which_object(scene, object_id)
                pos = scene["instances"][object_id]["position"]
                room = get_room(pos)
                target_pos = scene["instances"][target_id]["position"]
                target_room = get_room(target_pos)

                if object_id in upstair and robot_pos[1] <= 2.5:
                    solution.extend([f"goto(268)"])
                    plan.extend([f"Go upstair."])
                    image.extend(["268.jpg"])
                if object_id in downstair and robot_pos[1] > 2.5:
                    solution.extend([f"goto(268)"])
                    plan.extend([f"Go downstair."])
                    image.extend(["51.jpg"])
                if room != robot_room:
                    plan.extend([f"Go to the {room}."])
                    image.extend([f"{room}.jpg"])
                    robot_room = room
                if str(object_id) in docker.keys():
                    docker_id = docker[str(object_id)]["id"]
                    docker_name = docker[str(object_id)]["name"]
                    solution.extend([f"goto({docker_id})", "interact()", "grab()"])
                    plan.extend(
                        [f"Go to the {docker_name}.", f"Open the {docker_name}.", f"Grab the {object_name}."])
                    image.extend([f"{docker_id}.jpg", f"open_{docker_id}.jpg", f"grab_{object_id}.jpg"])
                else:
                    if on_id is not None and on_id != 0 and on_name != "House4":
                        plan.extend([f"Go to the {on_name}."])
                        image.extend([f"{on_id}.jpg"])
                    solution.extend([f"goto({object_id})", "grab()"])
                    plan.extend([f"Go to the {object_name}.", f"Grab the {object_name}."])
                    image.extend([f"{object_id}.jpg", f"grab_{object_id}.jpg"])
                object_pos_y = scene["instances"][object_id]["position"][1]
                target_pos_y = scene["instances"][target_id]["position"][1]
                if object_pos_y < 2.5 <= target_pos_y:
                    solution.extend([f"goto(268)"])
                    plan.extend([f"Go upstair."])
                    image.extend(["268.jpg"])
                if object_pos_y >= 2.5 > target_pos_y:
                    solution.extend([f"goto(268)"])
                    plan.extend([f"Go downstair."])
                    image.extend(["51.jpg"])
                if robot_room != target_room:
                    plan.extend([f"Go to the {target_room}."])
                    image.extend([f"{room}.jpg"])
                if target_id in box:
                    solution.extend([f"lookDown()", "release()"])
                    plan.extend([f"Put the {object_name} on the ground."])
                    image.extend([f"{object_id}.jpg"])
                    solution.extend([f"goto({target_id})", "interact()"])
                    plan.extend([f"Go to the {target_name}.", f"Open the {target_name}."])
                    image.extend([f"{target_id}.jpg", f"open_{target_id}.jpg"])
                    solution.extend([f"goto({object_id})", "grab()"])
                    plan.extend([f"Go to the {object_name}.", f"Pick up the {object_name}."])
                    image.extend([f"{object_id}.jpg", f"grab_{object_id}.jpg"])
                    solution.extend([f"goto({target_id})", f"release()"])
                    plan.extend([f"Go to the {target_name}.", f"Release the {object_name}."])
                    image.extend([f"{target_id}.jpg"])
                else:
                    solution.extend([f"goto({target_id})"])
                    plan.extend([f"Go to the {target_name}."])
                    image.extend([f"{target_id}.jpg"])
                    solution.extend([f"release()"])
                    plan.extend([f"Release the {object_name}."])
                index = random.choice([1, 2])
                sample = {
                    "task": task,
                    "scene": get_room(robot_pos) + "_" + str(index) + ".png",
                    "plan": plan,
                    "robot_room": get_room(robot_pos),
                    "start_image": str(object_id) + ".png",
                    "image": image,
                    "id": object_id,
                    "color": color[object_name]
                }
                samples.append(sample)
                if len(sample["plan"]) - len(sample["image"]) != 1:
                    print(i)
                    raise ()
                print(task, i)
                # print(sample)
        # elif task_type == "where":
        #     # TODO: use ChatGPT
        #     while True:
        #         object_id, object_name = get_random_object(scene)
        #         on_id, on_name = get_on_which_object(scene, object_id)
        #         if on_id != 0 and object_id not in where_full:
        #             wrong_times = random.choice([1, 2, 3, 4])
        #             random_objects = []
        #             for count in range(150):
        #                 history = [object_id]
        #                 for _ in range(0, wrong_times):
        #                     random_object_id, random_object_name = get_random_place(scene)
        #                     random_objects.append([random_object_id, random_object_name])
        #                     history.append(random_object_name)
        #                 if history not in history_task["where"]:
        #                     history_task["where"].append(history)
        #                     break
        #             if count < 149:
        #                 break
        #             else:
        #                 where_full.append(object_id)
        #     for robot_pos in robot_possable_pos:
        #         robot_room = get_room(robot_pos)
        #         task = f"Where is the {object_name}?"
        #         reply = f"It's on the {on_name}."
        #         solution = []
        #         plan = []
        #
        #         on_id, on_name = get_on_which_object(scene, object_id)
        #         pos = scene["instances"][object_id]["position"]
        #         room = get_room(pos)
        #
        #         if robot_pos[1] <= 2.5:
        #             random_object_id_old = 4
        #         else:
        #             random_object_id_old = 264
        #         target_room_old = robot_room
        #         for random_object in random_objects:
        #             random_object_id, random_object_name = random_object[0],random_object[1]
        #             target_pos = scene["instances"][random_object_id]["position"]
        #             target_room = get_room(target_pos)
        #             random_on_id, random_on_name = get_on_which_object(scene, random_object_id)
        #             if random_object_id in upstair and random_object_id_old in downstair:
        #                 solution.extend([f"goto(268)"])
        #                 plan.extend([f"Go upstair."])
        #             elif random_object_id in downstair and random_object_id_old in upstair:
        #                 solution.extend([f"goto(51)"])
        #                 plan.extend([f"Go downstair."])
        #             if target_room != target_room_old:
        #                 plan.extend([f"Go to the {target_room}."])
        #             if random_on_id != 0 and random_on_name != "House4":
        #                 plan.extend([f"Go to the {random_on_name}."])
        #             solution.extend([f"goto({random_object_id})", f'speak("It\'s not on the {random_object_name}.")'])
        #             plan.extend(
        #                 [f"Go to the {random_object_name}.",
        #                  f"Reply to the user:It\'s not on the {random_object_name}."])
        #             random_object_id_old = random_object_id
        #             target_room_old = target_room
        #         if on_id in upstair and random_object_id_old in downstair:
        #             solution.extend([f"goto(268)"])
        #             plan.extend([f"Go upstair."])
        #         elif on_id in downstair and random_object_id_old in upstair:
        #             solution.extend([f"goto(51)"])
        #             plan.extend([f"Go downstair."])
        #
        #         on_pos = scene["instances"][on_id]["position"]
        #         on_room = get_room(on_pos)
        #         if on_room != target_room_old:
        #             plan.extend([f"Go to the {on_room}."])
        #         if on_id != 0 and on_name != "House4":
        #             plan.extend([f"Go to the {on_name}."])
        #         solution.extend([f"goto({on_id})", f'speak("{reply}")'])
        #         plan.extend([f"Reply to the user：It's on the {on_name}."])
        #         index = random.choice([1, 2])
        #         sample = {
        #             "task": task,
        #             "scene": get_room(robot_pos) + "_" + str(index) + ".png",
        #             "plan": plan,
        #             "robot_room": get_room(robot_pos),
        #             "image": str(object_id) + ".png",
        #             "id": object_id,
        #             "color":color[object_name]
        #         }
        #         samples.append(sample)
        #         print(task, i)
        elif task_type == "exist":
            while True:
                object_id = random.choice(part_exist)
                object_name = scene["instances"][object_id]["prefab"].split("LowPolyInterior2_")[1]
                on_id_no, on_name_no = get_on_which_object(scene, object_id)
                flag = 0
                for _ in range(150):
                    on_id = random.choice(part_target)
                    on_name = scene["instances"][on_id]["prefab"].split("LowPolyInterior2_")[1]
                    if on_id != on_id_no and [object_name, on_name] not in history_task[
                        "exist"]:  # 如果新随机出来的物品与之前的物品在同一个桌子上
                        history_task["exist"].append([object_name, on_name])
                        flag = 1
                        break
                if flag == 0:
                    exist = list(set(exist) - {object_id})
                else:
                    break
            for robot_pos in robot_possable_pos:
                robot_room = get_room(robot_pos)
                if object_name in color.keys():
                    object_color = color[object_name] + " "
                else:
                    object_color = ""
                if on_name == "Bathroom" or on_name == "Kitchen1" or str(on_id) in docker.keys():
                    task = f"Is there a {object_name} in the {on_name}?"
                else:
                    task = f"Is there a {object_name} on the {on_name}?"
                reply = "No"
                solution = []
                plan = []
                image = []
                on_pos_y = scene["instances"][on_id]["position"][1]
                if on_pos_y > 2.5 and robot_pos[1] <= 2.5:
                    solution.extend([f"goto(268)"])
                    plan.extend([f"Go upstair."])
                    image.extend(["268.jpg"])
                if on_pos_y <= 2.5 and robot_pos[1] > 2.5:
                    solution.extend([f"goto(268)"])
                    plan.extend([f"Go downstair."])
                    image.extend(["51.jpg"])
                pos = scene["instances"][on_id]["position"]
                room = get_room(pos)
                if room != robot_room:
                    plan.extend([f"Go to the {room}."])
                    image.extend([f"{room}.jpg"])
                    robot_room = room
                if str(on_id) in docker.keys():
                    docker_id = docker[str(on_id)]["id"]
                    docker_name = docker[str(docker_id)]["name"]
                    solution.extend([f"goto({on_id})", "interact()"])
                    plan.extend([f"Go to the {on_name}.", f"Open the {docker_name}."])
                    image.extend([f"{on_id}.jpg", f"open_{docker_id}.jpg"])
                else:
                    plan.extend([f"Go to the {on_name}."])
                    image.extend([f"{on_id}.jpg"])
                solution.extend([f'speak("{reply}")'])
                plan.extend([f"Check the {on_name}.", "Reply to the user:No."])
                image.extend([f"{on_id}.jpg"])
                index = random.choice([1, 2])
                sample = {
                    "task": task,
                    "scene": get_room(robot_pos) + "_" + str(index) + ".png",
                    "plan": plan,
                    "robot_room": get_room(robot_pos),
                    "start_image": str(object_id) + ".png",
                    "image": image,
                    "id": object_id,
                    "color": object_color
                }
                samples.append(sample)
                if len(sample["plan"]) - len(sample["image"]) != 1:
                    print(i)
                    raise ()
                print(task, i)
    return samples


def test_object(scene, object_list, type="goto"):

    if type == "bring":
        all_samples = []
        for object_id in object_list:
            object_name = scene["instances"][object_id]["prefab"].split("LowPolyInterior2_")[1]
            object_color = color[object_name]
            task = f"Bring the {object_name} to me."
            on_id, on_name = get_on_which_object(scene, object_id)
            pos = scene["instances"][object_id]["position"]
            room = get_room(pos)
            for robot_pos in robot_possable_pos:
                for human_pos in human_possable_pos:
                    robot_room = get_room(robot_pos)
                    human_room = get_room(human_pos)
                    solution = []
                    plan = []
                    image = []
                    object_pos_y = scene["instances"][object_id]["position"][1]
                    if object_pos_y > 2.5 and robot_pos[1] <= 2.5:
                        solution.extend([f"goto(268)"])
                        plan.extend([f"Go upstair."])
                        image.extend(["268.jpg"])
                    if object_pos_y <= 2.5 and robot_pos[1] > 2.5:
                        solution.extend([f"goto(268)"])
                        plan.extend([f"Go downstair."])
                        image.extend(["51.jpg"])
                    if room != robot_room:
                        plan.extend([f"Go to the {room}."])
                        image.extend([f"{room}.jpg"])
                        robot_room = room
                    if str(object_id) in docker.keys():
                        docker_id = docker[str(object_id)]["id"]
                        docker_name = docker[str(object_id)]["name"]
                        solution.extend([f"goto({docker_id})", "interact()", "grab()"])
                        plan.extend(
                            [f"Go to the {docker_name}.", f"Open the {docker_name}.", f"Pick up the {object_name}."])
                        image.extend([f"{docker_id}.jpg", f"open_{docker_id}.jpg", f"grab_{object_id}.jpg"])
                    else:
                        if on_id is not None and on_id != 0 and on_name != "House4":
                            plan.extend([f"Go to the {on_name}."])
                            image.extend([f"{on_id}.jpg"])
                        solution.extend([f"goto({object_id})", "grab()"])
                        plan.extend([f"Go to the {object_name}.", f"Grab the {object_name}."])
                        image.extend([f"{object_id}.jpg", f"grab_{object_id}.jpg"])
                    if object_pos_y > 2.5 and human_pos[1] <= 2.5:
                        solution.extend([f"goto(51)"])
                        plan.extend([f"Go downstair."])
                        image.extend(["51.jpg"])
                    if object_pos_y <= 2.5 and human_pos[1] > 2.5:
                        solution.extend([f"goto(51)"])
                        plan.extend([f"Go upstair."])
                        image.extend(["268.jpg"])
                    if robot_room != human_room:
                        plan.extend([f"Go to the {human_room}."])
                        image.extend([f"{human_room}.jpg"])
                        robot_room = human_room
                    solution.extend(["goto_user()"])
                    plan.extend(["Go to the user.", f"Give the {object_name} to the user."])
                    image.extend([f"user.jpg"])
                    index = random.choice([1, 2])
                    sample = {
                        "task": task,
                        "scene": get_room(robot_pos) + "_" + str(index) + ".png",
                        "plan": plan,
                        "image": image,
                        "start_image": str(object_id) + ".png",
                        "robot_room": get_room(robot_pos),
                        "human_room": get_room(human_pos),
                        "id": object_id,
                        "color": object_color
                    }
                    all_samples.append(sample)
            # print(task, object_id)
    elif type == "take":
        all_samples = []
        for object_id in object_list:
            on_id, on_name = get_on_which_object(scene, object_id)
            pos = scene["instances"][object_id]["position"]
            room = get_room(pos)
            for robot_pos in robot_possable_pos:
                robot_room = get_room(robot_pos)
                object_name = scene["instances"][object_id]["prefab"].split("LowPolyInterior2_")[1]
                object_color = color[object_name]
                task = f"Take the {object_name}."
                solution = []
                plan = []
                image = []
                object_pos_y = scene["instances"][object_id]["position"][1]
                if object_pos_y > 2.5 and robot_pos[1] <= 2.5:
                    solution.extend([f"goto(268)"])
                    plan.extend([f"Go upstair."])
                    image.extend(["268.jpg"])
                if object_pos_y <= 2.5 and robot_pos[1] > 2.5:
                    solution.extend([f"goto(268)"])
                    plan.extend([f"Go downstair."])
                    image.extend(["51.jpg"])
                if room != robot_room:
                    plan.extend([f"Go to the {room}."])
                    image.extend([f"{room}.jpg"])
                    robot_room = room
                if str(object_id) in docker.keys():
                    docker_id = docker[str(object_id)]["id"]
                    docker_name = docker[str(object_id)]["name"]
                    solution.extend([f"goto({docker_id})", "interact()", "grab()"])
                    plan.extend(
                        [f"Go to the {docker_name}.", f"Open the {docker_name}.", f"Pick up the {object_name}."])
                    image.extend([f"{docker_id}.jpg", f"open_{docker_id}.jpg"])
                else:
                    if on_id is not None and on_id != 0 and on_name != "House4":
                        plan.extend([f"Go to the {on_name}."])
                        image.extend([f"{on_id}.jpg"])
                    solution.extend([f"goto({object_id})", "grab()"])
                    plan.extend([f"Go to the {object_name}.", f"Grab the {object_name}."])
                    image.extend([f"{object_id}.jpg"])
                index = random.choice([1, 2])
                sample = {
                    "task": task,
                    "scene": get_room(robot_pos) + "_" + str(index) + ".png",
                    "plan": plan,
                    "robot_room": get_room(robot_pos),
                    "start_image": str(object_id) + ".png",
                    "image": image,
                    "id": object_id,
                    "color": object_color
                }
                all_samples.append(sample)
            # print(task, object_id)
    elif type == "goto":
        all_samples = []
        for object_id in object_list:
            on_id, on_name = get_on_which_object(scene, object_id)
            pos = scene["instances"][object_id]["position"]
            room = get_room(pos)
            for robot_pos in robot_possable_pos:
                robot_room = get_room(robot_pos)
                object_name = scene["instances"][object_id]["prefab"].split("LowPolyInterior2_")[1]
                object_color = color[object_name]
                task = f"Go to the {object_name}."
                solution = []
                plan = []
                image = []
                object_pos_y = scene["instances"][object_id]["position"][1]
                if object_pos_y > 2.5 and robot_pos[1] <= 2.5:
                    solution.extend([f"goto(268)"])
                    plan.extend([f"Go upstair."])
                    image.extend(["268.jpg"])
                if object_pos_y <= 2.5 and robot_pos[1] > 2.5:
                    solution.extend([f"goto(268)"])
                    plan.extend([f"Go downstair."])
                    image.extend(["51.jpg"])
                if room != robot_room:
                    plan.extend([f"Go to the {room}."])
                    image.extend([f"{room}.jpg"])
                    robot_room = room
                if str(object_id) in docker.keys():
                    docker_id = docker[str(object_id)]["id"]
                    docker_name = docker[str(object_id)]["name"]
                    solution.extend([f"goto({docker_id})", "interact()"])
                    plan.extend([f"Go to the {docker_name}.", f"Open the {docker_name}."])
                    image.extend([f"{docker_id}.jpg"])
                else:
                    if on_id is not None and on_id != 0 and on_name != "House4":
                        plan.extend([f"Go to the {on_name}."])
                        image.extend([f"{on_id}.jpg"])
                    solution.extend([f"goto({object_id})"])
                    plan.extend([f"Go to the {object_name}."])
                index = random.choice([1, 2])
                sample = {
                    "task": task,
                    "scene": get_room(robot_pos) + "_" + str(index) + ".png",
                    "plan": plan,
                    "robot_room": get_room(robot_pos),
                    "start_image": str(object_id) + ".png",
                    "image": image,
                    "id": object_id,
                    "color": object_color
                }
                all_samples.append(sample)
            # print(task, object_id)
    elif type == "new_where":
        all_samples = []
        for object_id in object_list:
            on_id, on_name = get_on_which_object(scene, object_id)
            if on_id is None:
                continue
            pos = scene["instances"][object_id]["position"]
            room = get_room(pos)
            for robot_pos in robot_possable_pos:
                robot_room = get_room(robot_pos)
                object_name = scene["instances"][object_id]["prefab"].split("LowPolyInterior2_")[1]
                if object_name in color.keys():
                    object_color = color[object_name] + " "
                else:
                    object_color = ""
                task = f"Where is the {object_name}?"
                solution = []
                plan = []
                image = []
                if object_id in upstair and robot_pos[1] <= 2.5:
                    solution.extend([f"goto(268)"])
                    plan.extend([f"Go upstair."])
                    image.extend(["268.jpg"])
                if object_id in downstair and robot_pos[1] > 2.5:
                    solution.extend([f"goto(268)"])
                    plan.extend([f"Go downstair."])
                    image.extend(["51.jpg"])
                if room != robot_room:
                    plan.extend([f"Go to the {room}."])
                    image.extend([f"{room}.jpg"])
                    robot_room = room
                if str(object_id) in docker.keys():
                    docker_id = docker[str(object_id)]["id"]
                    docker_name = docker[str(object_id)]["name"]
                    solution.extend([f"goto({docker_id})", "interact()"])
                    plan.extend([f"Go to the {docker_name}.", f"Open the {docker_name}."])
                    image.extend([f"{docker_id}.jpg", f"open_{docker_id}.jpg"])
                    plan.extend([f"Check the {docker_name}."])
                else:
                    if on_id is not None and on_id != 0 and on_name != "House4":
                        plan.extend([f"Go to the {on_name}."])
                        image.extend([f"{on_id}.jpg"])
                        plan.extend([f"Check the {on_name}."])
                plan.extend([f"Reply to the user：It's on the {on_name}."])
                index = random.choice([1, 2])
                sample = {
                    "task": task,
                    "scene": get_room(robot_pos) + "_" + str(index) + ".png",
                    "plan": plan,
                    "robot_room": get_room(robot_pos),
                    "start_image": str(object_id) + ".png",
                    "image": image,
                    "id": object_id,
                    "color": object_color
                }
                all_samples.append(sample)
            # print(task, object_id)
    elif type == "exist":
        all_samples = []
        for object_id in object_list:
            object_name = scene["instances"][object_id]["prefab"].split("LowPolyInterior2_")[1]
            on_id, on_name = get_on_which_object(scene, object_id)
            pos = scene["instances"][object_id]["position"]
            # print(object_id, pos)
            room = get_room(pos)
            if on_id is None or on_id == 0 and object_id not in floor or "House4" in on_name:
                continue
            history_task["exist"].append([object_id, on_id])
            if object_name in color.keys():
                object_color = color[object_name] + " "
            else:
                object_color = ""
            if on_name == "Bathroom" or on_name == "Kitchen1" or (on_id is not None and str(on_id)) in docker.keys():
                task = f"Is there a {object_name} in the {on_name}?"
            else:
                task = f"Is there a {object_name} on the {on_name}?"
            for robot_pos in robot_possable_pos:
                robot_room = get_room(robot_pos)
                reply = "Yes."
                solution = []
                plan = []
                image = []
                if pos[1] > 2.5 and robot_pos[1] <= 2.5:
                    solution.extend([f"goto(268)"])
                    plan.extend([f"Go upstair."])
                    image.extend(["268.jpg"])
                if pos[1] <= 2.5 and robot_pos[1] > 2.5:
                    solution.extend([f"goto(268)"])
                    plan.extend([f"Go downstair."])
                    image.extend(["51.jpg"])
                if room != robot_room:
                    plan.extend([f"Go to the {room}."])
                    image.extend([f"{room}.jpg"])
                    robot_room = room
                if str(object_id) in docker.keys():
                    docker_id = docker[str(object_id)]["id"]
                    docker_name = docker[str(object_id)]["name"]
                    solution.extend([f"goto({docker_id})", "interact()"])
                    plan.extend([f"Go to the {docker_name}.", f"Open the {docker_name}."])
                    image.extend([f"{docker_id}.jpg", f"open_{docker_id}.jpg"])
                else:
                    plan.extend([f"Go to the {on_name}."])
                    image.extend([f"{on_id}.jpg"])
                solution.extend([f'speak("{reply}")'])
                plan.extend([f"Check the {on_name}.", f"Reply to the user:YES."])
                image.extend([f"{on_id}.jpg"])
                index = random.choice([1, 2])
                sample = {
                    "task": task,
                    "scene": get_room(robot_pos) + "_" + str(index) + ".png",
                    "plan": plan,
                    "robot_room": get_room(robot_pos),
                    "start_image": str(object_id) + ".png",
                    "image": image,
                    "id": object_id,
                    "color": object_color
                }
                all_samples.append(sample)
    # for i in all_samples:
    #     if len(i["plan"]) - len(i["image"]) != 1:
    #         print(i)
    #         raise()
    return all_samples


def write_in_file(root):
    global scene
    type = root.split("/")[-1]

    samples = create_text_task("put",
                               interactable_id_dict[type],
                               target_dict[type],
                               exist_dict[type],
                               scene=scene,
                               num=480 if type =="train" else 120)
    print(f"put_{type}:", len(samples))
    with open(os.path.join(root,"put.json"), 'w') as file:
        json.dump(samples, file)

    samples = create_text_task("exist",
                               interactable_id_dict[type],
                               target_dict[type],
                               exist_dict[type],
                               scene=scene,
                               num=480 if type =="train" else 120)
    print(f"exist_{type}:", len(samples))
    with open(os.path.join(root, "exist.json"), 'w') as file:
        json.dump(samples, file)

    samples = test_object(scene, exist_dict[type], "new_where")
    print(f"where_{type}:", len(samples))
    with open(os.path.join(root, "where.json"), 'w') as file:
        json.dump(samples, file)

    samples = test_object(scene, interactable_id_dict[type], "bring")
    print(f"bring_{type}:", len(samples))
    with open(os.path.join(root, "bring.json"), 'w') as file:
        json.dump(samples, file)

    samples = test_object(scene, interactable_id_dict[type], "take")
    print(f"take_{type}:", len(samples))
    with open(os.path.join(root, "take.json"), 'w') as file:
        json.dump(samples, file)

    samples = test_object(scene, interactable_id_dict[type], "goto")
    print(f"goto_{type}:", len(samples))
    with open(os.path.join(root, "goto.json"), 'w') as file:
        json.dump(samples, file)

    samples = test_object(scene, exist_dict[type], "exist")
    print(f"exist_yes_{type}:", len(samples))
    with open(os.path.join(root, "exist_yes.json"), 'w') as file:
        json.dump(samples, file)


if __name__ == "__main__":
    # name_id = {}
    # for i,instance in enumerate(scene["instances"]):
    #     pos = instance["position"]
    #     room = get_room(pos)
    #     name = instance["prefab"].split("LowPolyInterior2_")[1]
    #     if str(i) in docker.keys():
    #         docker_id = docker[str(i)]["id"]
    #         docker_name = docker[str(i)]["name"]
    #         docker_key = room + docker_name
    #         if docker_key not in name_id.keys():
    #             name_id[docker_key] = [i]
    #             name_id[docker_key.lower()] = [i]
    #         else:
    #             name_id[docker_key].append(i)
    #             name_id[docker_key.lower()].append(i)
    #     key = room + name
    #     if key not in name_id.keys():
    #         name_id[key] = [i]
    #         name_id[key.lower()] = [i]
    #     else:
    #         name_id[key].append(i)
    #         name_id[key.lower()].append(i)
    # with open("json/name_id.json", 'w') as file:
    #     json.dump(name_id, file)
    #################################################################################################
    # ids = []
    # for json_name in ["bring","exist","exist_yes","goto","put","take","where"]:
    #     with open(f"data/{json_name}.json", 'r') as file:
    #         json_data = json.load(file)
    #     for data in json_data:
    #         if data["id"] not in ids:
    #             ids.append(data["id"])
    # pic_ids = os.listdir("data/image")
    # pic_list = []
    # for pic in pic_ids:
    #     pic_list.append(pic[:-4])
    # for i in ids:
    #     if str(i) not in pic_list:
    #         print(i)
    #################################################################################################
    # write_in_file("result/train")
    # samples = create_text_task("put", scene=scene, num=1)
    #################################################################################################
    # with open("result/where.json", 'r') as file:
    #     json_data = json.load(file)
    # for i,data in enumerate(json_data):
    #     task = data["task"]
    #     start = 3
    #     for index,split_text in enumerate(task.split(" ")):
    #         if "_" in split_text:
    #             end = index
    #             break
    #     color = ""
    #     for index in range(start,end):
    #         color = color+task.split(" ")[index]+" "
    #     color = color[:-1]
    #     print(color)
    #     json_data[i]["task"] = task.split(color)[0]+task.split(color)[1][1:]
    #     json_data[i]["color"] = color
    # print(len(json_data))
    #################################################################################################
    # with open("result/where.json", 'w') as file:
    #     json.dump(json_data, file)
    # room = []
    # room1 = []
    # for json_name in ["put"]:
    #     with open(f"data/{json_name}.json", 'r') as file:
    #         json_data = json.load(file)
    #     for data in json_data:
    #         robot_room = data["scene"][:-6]
    #         if robot_room not in room:
    #             room.append(robot_room)
    #     for pos in robot_possable_pos:
    #         robot_room = get_room(pos)
    #         if robot_room not in room1:
    #             room1.append(robot_room)
    # print(sorted(room))
    # print(sorted(room1))
    #################################################################################################
    ###生成图片名称
    # pic_open = set()
    # pic_grab = set()
    # pic_rest = set()
    # pic_name = set()
    # for json_name in ["bring","exist","exist_yes","goto","put","take","where"]:
    #     with open(f"result/original/{json_name}.json", 'r') as file:
    #         json_data = json.load(file)
    #     for i in json_data:
    #         for j in i["image"]:
    #             if j not in pic_name:
    #                 pic_name.add(j)
    #                 if "grab" in j:
    #                     pic_grab.add(j)
    #                 elif "open" in j:
    #                     pic_open.add(j)
    #                 else:
    #                     pic_rest.add(j)
    # jsons = os.listdir("result/image")
    # print(pic_name - set(jsons))

    # 'user.jpg','First Floor Cloakroom1.jpg', 'First Floor Cloakroom2.jpg',
    #          'First Floor Living Room and Kitchen.jpg', 'Second Floor Bathroom1.jpg',
    #          'Second Floor Bathroom2.jpg', 'Second Floor Bedroom1.jpg', 'Second Floor Bedroom2.jpg',
    #          'Second Floor Cloakroom1.jpg', 'Second Floor Cloakroom2.jpg', 'Second Floor Corridor.jpg
    # list1 = ['100.jpg', '101.jpg', '11.jpg', '110.jpg', '114.jpg', '13.jpg', '14.jpg',
    #          '140.jpg', '141.jpg', '143.jpg', '144.jpg', '145.jpg', '16.jpg', '171.jpg',
    #          '172.jpg', '175.jpg', '180.jpg', '182.jpg', '183.jpg', '184.jpg', '185.jpg',
    #          '186.jpg', '188.jpg', '191.jpg', '192.jpg', '193.jpg', '194.jpg', '201.jpg',
    #          '205.jpg', '206.jpg', '207.jpg', '208.jpg', '217.jpg', '218.jpg', '220.jpg',
    #          '228.jpg', '229.jpg', '230.jpg', '241.jpg', '268.jpg', '272.jpg', '273.jpg',
    #          '274.jpg', '279.jpg', '283.jpg', '284.jpg', '309.jpg', '310.jpg', '311.jpg',
    #          '317.jpg', '319.jpg', '324.jpg', '328.jpg', '329.jpg', '333.jpg', '334.jpg',
    #          '335.jpg', '337.jpg', '343.jpg', '344.jpg', '365.jpg', '373.jpg', '381.jpg',
    #          '382.jpg', '388.jpg', '39.jpg', '405.jpg', '406.jpg', '410.jpg', '43.jpg',
    #          '44.jpg', '48.jpg', '51.jpg', '6.jpg', '66.jpg', '67.jpg', '7.jpg', '71.jpg',
    #          '78.jpg', '79.jpg', '8.jpg', '80.jpg', '81.jpg', '9.jpg', '93.jpg', '95.jpg',
    #          '96.jpg', '99.jpg']
    # open_list = ['open_95.jpg', 'open_134.jpg', 'open_309.jpg', 'open_26.jpg', 'open_144.jpg',
    #              'open_59.jpg', 'open_129.jpg', 'open_154.jpg', 'open_238.jpg', 'open_226.jpg',
    #              'open_156.jpg', 'open_413.jpg', 'open_416.jpg', 'open_143.jpg', 'open_132.jpg',
    #              'open_53.jpg', 'open_354.jpg', 'open_355.jpg', 'open_141.jpg', 'open_97.jpg',
    #              'open_135.jpg', 'open_412.jpg', 'open_235.jpg', 'open_222.jpg', 'open_58.jpg',
    #              'open_54.jpg', 'open_221.jpg', 'open_411.jpg', 'open_96.jpg', 'open_24.jpg',
    #              'open_310.jpg', 'open_225.jpg', 'open_45.jpg', 'open_25.jpg', 'open_155.jpg']
    # grab_list = ['grab_396.jpg', 'grab_358.jpg', 'grab_138.jpg', 'grab_24.jpg', 'grab_118.jpg', 'grab_221.jpg',
    #              'grab_267.jpg', 'grab_25.jpg', 'grab_394.jpg', 'grab_369.jpg', 'grab_356.jpg', 'grab_97.jpg',
    #              'grab_122.jpg', 'grab_236.jpg', 'grab_353.jpg', 'grab_411.jpg', 'grab_200.jpg', 'grab_412.jpg',
    #              'grab_167.jpg', 'grab_54.jpg', 'grab_119.jpg', 'grab_92.jpg', 'grab_108.jpg', 'grab_243.jpg',
    #              'grab_26.jpg', 'grab_154.jpg', 'grab_107.jpg', 'grab_234.jpg', 'grab_312.jpg', 'grab_397.jpg',
    #              'grab_120.jpg', 'grab_395.jpg', 'grab_380.jpg', 'grab_156.jpg', 'grab_168.jpg', 'grab_173.jpg',
    #              'grab_131.jpg', 'grab_242.jpg', 'grab_370.jpg', 'grab_111.jpg', 'grab_150.jpg', 'grab_58.jpg',
    #              'grab_276.jpg', 'grab_316.jpg', 'grab_153.jpg', 'grab_371.jpg', 'grab_398.jpg', 'grab_235.jpg',
    #              'grab_209.jpg', 'grab_155.jpg', 'grab_233.jpg', 'grab_104.jpg', 'grab_137.jpg', 'grab_103.jpg',
    #              'grab_134.jpg', 'grab_355.jpg', 'grab_151.jpg', 'grab_49.jpg', 'grab_222.jpg', 'grab_416.jpg',
    #              'grab_90.jpg', 'grab_210.jpg', 'grab_264.jpg', 'grab_59.jpg', 'grab_149.jpg', 'grab_413.jpg',
    #              'grab_22.jpg', 'grab_219.jpg', 'grab_53.jpg', 'grab_225.jpg', 'grab_387.jpg', 'grab_226.jpg',
    #              'grab_128.jpg', 'grab_132.jpg', 'grab_336.jpg', 'grab_129.jpg', 'grab_146.jpg', 'grab_238.jpg',
    #              'grab_354.jpg', 'grab_379.jpg', 'grab_130.jpg', 'grab_211.jpg', 'grab_392.jpg', 'grab_148.jpg',
    #              'grab_105.jpg', 'grab_152.jpg', 'grab_64.jpg', 'grab_135.jpg', 'grab_212.jpg', 'grab_237.jpg',
    #              'grab_91.jpg', 'grab_357.jpg', 'grab_106.jpg', 'grab_109.jpg', 'grab_372.jpg', 'grab_401.jpg',
    #              'grab_393.jpg', 'grab_174.jpg', 'grab_332.jpg', 'grab_265.jpg', 'grab_368.jpg', 'grab_147.jpg',
    #              'grab_384.jpg', 'grab_244.jpg', 'grab_414.jpg', 'grab_94.jpg', 'grab_199.jpg', 'grab_415.jpg',
    #              'grab_142.jpg', 'grab_348.jpg', 'grab_127.jpg', 'grab_63.jpg', 'grab_139.jpg', 'grab_45.jpg',
    #              'grab_126.jpg']
    #################################################################################################
    # write_in_file("result/train")
    # write_in_file("result/test")
    #################################################################################################
    #############检查数据重复
    # room_set = set()
    # for i in robot:
    #     for j in i.split(" "):
    #         room_set.add(j)
    # for i in human:
    #     for j in i.split(" "):
    #         room_set.add(j)
    # a = room_set
    # for i in list(a):
    #     room_set.add(i + ".")
    # docker_set = set()
    # for i in docker.values():
    #     docker_set.add(i["name"])
    #     docker_set.add(i["name"] + ".")
    #     docker_set.add(i["name"] + "?")
    #
    # for f in ["bring", "exist_yes", "goto", "take", "where", "put", "exist"]:
    #     with open(f"result/train/{f}.json", 'r') as file:
    #         train = json.load(file)
    #     with open(f"result/test/{f}.json", 'r') as file:
    #         test = json.load(file)
    #     train_word = set()
    #     test_word = set()
    #     train_task = []
    #     test_task = []
    #     for i in train:
    #         if i in train_task:
    #             raise ()
    #         else:
    #             train_task.append(i)
    #         for j in i["task"].split(" "):
    #             train_word.add(j)
    #         for j in i["plan"]:
    #             for k in j.split(" "):
    #                 train_word.add(k)
    #     for i in test:
    #         if i in test_task:
    #             raise ()
    #         else:
    #             test_task.append(i)
    #         for j in i["task"].split(" "):
    #             test_word.add(j)
    #         for j in i["plan"]:
    #             for k in j.split(" "):
    #                 test_word.add(k)
    #     print(f, len(train), len(test), "\n", train_word & test_word - room_set - docker_set)
    ################################################################################################
    # ###删除数据
    # repeat = ['BathroomProps_09', 'Clothes9_C2','Dumbbell_01', 'Clothes2_C4'
    #           'Book_05', 'TV_05','BathroomProps_10','Plant_17','Clothes4_C3'
    #           'Car_01',"Bin_01","Kitchen1_C1_01L",'Plate']
    # for f in ["bring", "exist_yes", "goto", "take", "where", "put", "exist"]:
    #     with open(f"result/test/{f}.json", 'r') as file:
    #         test = json.load(file)
    #     del_index = []
    #     for index,i in enumerate(test):
    #         flag = 0
    #         for j in i["task"].split(" "):
    #             for r in repeat:
    #                 print(r,j)
    #                 if r in j:
    #                     flag = 1
    #         for j in i["plan"]:
    #             for k in j.split(" "):
    #                 for r in repeat:
    #                     print(r, k)
    #                     if r in k:
    #                         flag = 1
    #         if flag == 1:
    #             del_index.append(index)
    #     for i in reversed(del_index):
    #         del test[i]
    #     with open(f"result/test/{f}.json", 'w') as file:
    #         json.dump(test, file)
    # #################################################################################################
    with open(f"result/train/bring.json", 'r') as file:
        train = json.load(file)
    with open(f"result/test/bring.json", 'r') as file:
        test = json.load(file)
    train = random.sample(train, 5280)
    test = random.sample(test, 286)
    print("bring", len(train), len(test))
    with open(f"result/train/bring.json", 'w') as file:
        json.dump(train, file)
    with open(f"result/test/bring.json", 'w') as file:
        json.dump(test, file)

    with open(f"result/train/exist_yes.json", 'r') as file:
        train = json.load(file)
    with open(f"result/test/exist_yes.json", 'r') as file:
        test = json.load(file)
    train = train
    test = test
    print("exist_yes", len(train), len(test))
    with open(f"result/train/exist_yes.json", 'w') as file:
        json.dump(train, file)
    with open(f"result/test/exist_yes.json", 'w') as file:
        json.dump(test, file)

    with open(f"result/train/take.json", 'r') as file:
        train = json.load(file)
    with open(f"result/test/take.json", 'r') as file:
        test = json.load(file)
    train = train
    test = random.sample(test, 286)
    print("take", len(train), len(test))
    with open(f"result/train/take.json", 'w') as file:
        json.dump(train, file)
    with open(f"result/test/take.json", 'w') as file:
        json.dump(test, file)

    with open(f"result/train/goto.json", 'r') as file:
        train = json.load(file)
    with open(f"result/test/goto.json", 'r') as file:
        test = json.load(file)
    train = train
    test = random.sample(test, 286)
    print("goto", len(train), len(test))
    with open(f"result/train/goto.json", 'w') as file:
        json.dump(train, file)
    with open(f"result/test/goto.json", 'w') as file:
        json.dump(test, file)

    with open(f"result/train/where.json", 'r') as file:
        train = json.load(file)
    with open(f"result/test/where.json", 'r') as file:
        test = json.load(file)
    train = train
    test = test
    print("where", len(train), len(test))
    with open(f"result/train/where.json", 'w') as file:
        json.dump(train, file)
    with open(f"result/test/where.json", 'w') as file:
        json.dump(test, file)

    with open(f"result/train/put.json", 'r') as file:
        train = json.load(file)
    with open(f"result/test/put.json", 'r') as file:
        test = json.load(file)
    train = train
    test = random.sample(test, 286)
    print("put", len(train), len(test))
    with open(f"result/train/put.json", 'w') as file:
        json.dump(train, file)
    with open(f"result/test/put.json", 'w') as file:
        json.dump(test, file)

    with open(f"result/train/exist.json", 'r') as file:
        train = json.load(file)
    with open(f"result/test/exist.json", 'r') as file:
        test = json.load(file)
    train = train
    test = random.sample(test, 286)
    print("exist", len(train), len(test))
    with open(f"result/train/exist.json", 'w') as file:
        json.dump(train, file)
    with open(f"result/test/exist.json", 'w') as file:
        json.dump(test, file)
