# coding=utf-8
# 生成测试数据集
import os
import os.path as path
import json
import shutil
import re
import random
from typing import Literal
import numpy as np
from legent.utils.math import is_point_on_box

with open("json/interactable.json", 'r') as file:
    save_dict = json.load(file)
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
with open("json/history_task.json", 'r') as file:
    history_task = json.load(file)
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


def create_text_task(task_type, scene=None, num=1):
    # TODO: verified the correctness of all cases
    global exist

    def get_random_object(scene):
        # object_candidates = []
        # for i, instance in enumerate(scene["instances"]):
        #     if instance["type"] == "interactable":
        #         object_candidates.append(i)
        object_id = random.choice(interactable_id)
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
        target_id = random.choice(target)
        target_name = scene["instances"][target_id]["prefab"].split("LowPolyInterior2_")[1]
        return target_id, target_name

    def get_random_place(scene):
        object_id = random.choice(interactable_id + target)
        object_name = scene["instances"][object_id]["prefab"].split("LowPolyInterior2_")[1]
        return object_id, object_name

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
        max_y = -100
        on_id = None
        for i in on_candidates:
            if scene["instances"][i]["position"][1] > max_y:
                max_y = scene["instances"][i]["position"][1]
                on_id = i

        if on_id is not None:
            on_name = scene["instances"][on_id]["prefab"].split("LowPolyInterior2_")[1]
        if on_id is None and on_name is None:
            on_id = 0
            on_name = "House4"
        if str(on_id) in docker.keys():
            on_name = docker[str(on_id)]["name"]
        return on_id, on_name

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
            while True:
                object_id, object_name = get_random_object(scene)
                target_id, target_name = get_random_target(scene, object_id)
                if [object_id, target_name] not in history_task["put"]:
                    history_task["put"].append([object_id, target_name])
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
                on_id, on_name = get_on_which_object(scene, object_id)
                pos = scene["instances"][object_id]["position"]
                room = get_room(pos)
                target_pos = scene["instances"][target_id]["position"]
                target_room = get_room(target_pos)

                if object_id in upstair and robot_pos[1] <= 2.5:
                    solution.extend([f"goto(268)"])
                    plan.extend([f"Go upstair."])
                if object_id in downstair and robot_pos[1] > 2.5:
                    solution.extend([f"goto(268)"])
                    plan.extend([f"Go downstair."])
                if room != robot_room:
                    plan.extend([f"Go to the {room}."])
                    robot_room = room
                if str(object_id) in docker.keys():
                    docker_id = docker[str(object_id)]["id"]
                    docker_name = docker[str(object_id)]["name"]
                    solution.extend([f"goto({docker_id})", "interact()", "grab()"])
                    plan.extend(
                        [f"Go to the {docker_name}.", f"Open the {docker_name}.", f"Grab the {object_name}."])
                else:
                    if on_id != 0 and on_name != "House4":
                        plan.extend([f"Go to the {on_name}."])
                    solution.extend([f"goto({object_id})", "grab()"])
                    plan.extend([f"Go to the {object_name}.", f"Grab the {object_name}."])
                object_pos_y = scene["instances"][object_id]["position"][1]
                target_pos_y = scene["instances"][target_id]["position"][1]
                if object_pos_y < 2.5 <= target_pos_y:
                    solution.extend([f"goto(268)"])
                    plan.extend([f"Go upstair."])
                if object_pos_y >= 2.5 > target_pos_y:
                    solution.extend([f"goto(268)"])
                    plan.extend([f"Go downstair."])
                if robot_room != target_room:
                    plan.extend([f"Go to the {target_room}."])
                if target_id in box:
                    solution.extend([f"lookDown()", "release()"])
                    plan.extend([f"Put the {object_name} on the ground."])
                    solution.extend([f"goto({target_id})", "interact()"])
                    plan.extend([f"Go to the {target_name}.", f"Open the {target_name}."])
                    solution.extend([f"goto({object_id})", "grab()"])
                    plan.extend([f"Go to the {object_name}.", f"Pick up the {object_name}."])
                    solution.extend([f"goto({target_id})", f"release()"])
                    plan.extend([f"Go to the {target_name}.", f"Release the {object_name}."])
                else:
                    solution.extend([f"goto({target_id})"])
                    plan.extend([f"Go to the {target_name}."])
                    solution.extend([f"release()"])
                    plan.extend([f"Release the {object_name}."])
                index = random.choice([1, 2])
                sample = {
                    "task": task,
                    "scene": get_room(robot_pos) + "_" + str(index) + ".png",
                    "plan": plan,
                    "robot_room": get_room(robot_pos),
                    "image": str(object_id) + ".png",
                    "id": object_id,
                    "color": color[object_name]
                }
                samples.append(sample)
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
                object_id = random.choice(exist)
                object_name = scene["instances"][object_id]["prefab"].split("LowPolyInterior2_")[1]
                on_id_no, on_name_no = get_on_which_object(scene, object_id)
                flag = 0
                for _ in range(150):
                    on_id = random.choice(target)
                    on_name = scene["instances"][on_id]["prefab"].split("LowPolyInterior2_")[1]
                    if on_id != on_id_no and [object_name, on_name] not in history_task["exist"]:  # 如果新随机出来的物品与之前的物品在同一个桌子上
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
                on_pos_y = scene["instances"][on_id]["position"][1]
                if on_pos_y > 2.5 and robot_pos[1] <= 2.5:
                    solution.extend([f"goto(268)"])
                    plan.extend([f"Go upstair."])
                if on_pos_y <= 2.5 and robot_pos[1] > 2.5:
                    solution.extend([f"goto(268)"])
                    plan.extend([f"Go downstair."])
                pos = scene["instances"][on_id]["position"]
                room = get_room(pos)
                if room != robot_room:
                    plan.extend([f"Go to the {room}."])
                    robot_room = room

                if str(on_id) in docker.keys():
                    docker_id = docker[str(on_id)]["id"]
                    docker_name = docker[str(docker_id)]["name"]
                    solution.extend([f"goto({on_id})", "interact()"])
                    plan.extend([f"Go to the {on_name}.", f"Open the {docker_name}."])
                else:
                    plan.extend([f"Go to the {on_name}."])
                solution.extend([f'speak("{reply}")'])
                plan.extend([f"Check the {on_name}.", "Reply to the user:No."])
                index = random.choice([1, 2])
                sample = {
                    "task": task,
                    "scene": get_room(robot_pos) + "_" + str(index) + ".png",
                    "plan": plan,
                    "robot_room": get_room(robot_pos),
                    "image": str(object_id) + ".png",
                    "id": object_id,
                    "color": object_color
                }
                samples.append(sample)
                print(task, i)
    return samples


def test_object(scene, type="goto"):
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
        max_y = -100
        on_id = None
        for i in on_candidates:
            if scene["instances"][i]["position"][1] > max_y:
                max_y = scene["instances"][i]["position"][1]
                on_id = i

        if on_id is not None:
            on_name = scene["instances"][on_id]["prefab"].split("LowPolyInterior2_")[1]
        if on_id is None and on_name is None:
            on_id = 0
            on_name = "House4"
        if str(on_id) in docker.keys():
            on_name = docker[str(on_id)]["name"]
        return on_id, on_name

    if type == "bring":
        all_samples = []
        for object_id in interactable_id:
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
                    object_pos_y = scene["instances"][object_id]["position"][1]
                    if object_pos_y > 2.5 and robot_pos[1] <= 2.5:
                        solution.extend([f"goto(268)"])
                        plan.extend([f"Go upstair."])
                    if object_pos_y <= 2.5 and robot_pos[1] > 2.5:
                        solution.extend([f"goto(268)"])
                        plan.extend([f"Go downstair."])
                    if room != robot_room:
                        plan.extend([f"Go to the {room}."])
                        robot_room = room
                    if str(object_id) in docker.keys():
                        docker_id = docker[str(object_id)]["id"]
                        docker_name = docker[str(object_id)]["name"]
                        solution.extend([f"goto({docker_id})", "interact()", "grab()"])
                        plan.extend(
                            [f"Go to the {docker_name}.", f"Open the {docker_name}.", f"Pick up the {object_name}."])
                    else:
                        if on_id != 0 and on_name != "House4":
                            plan.extend([f"Go to the {on_name}."])
                        solution.extend([f"goto({object_id})", "grab()"])
                        plan.extend([f"Go to the {object_name}.", f"Grab the {object_name}."])
                    if object_pos_y > 2.5 and human_pos[1] <= 2.5:
                        solution.extend([f"goto(51)"])
                        plan.extend([f"Go downstair."])
                    if object_pos_y <= 2.5 and human_pos[1] > 2.5:
                        solution.extend([f"goto(51)"])
                        plan.extend([f"Go upstair."])
                    if robot_room != human_room:
                        plan.extend([f"Go to the {human_room}."])
                        robot_room = human_room
                    solution.extend(["goto_user()"])
                    plan.extend(["Go to the user.", f"Give the {object_name} to the user."])

                    index = random.choice([1, 2])
                    sample = {
                        "task": task,
                        "scene": get_room(robot_pos) + "_" + str(index) + ".png",
                        "plan": plan,
                        "robot_room": get_room(robot_pos),
                        "human_room": get_room(human_pos),
                        "image": str(object_id) + ".png",
                        "id": object_id,
                        "color": object_color
                    }
                    all_samples.append(sample)
            print(task, object_id)
    elif type == "take":
        all_samples = []
        for object_id in interactable_id:
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
                object_pos_y = scene["instances"][object_id]["position"][1]
                if object_pos_y > 2.5 and robot_pos[1] <= 2.5:
                    solution.extend([f"goto(268)"])
                    plan.extend([f"Go upstair."])
                if object_pos_y <= 2.5 and robot_pos[1] > 2.5:
                    solution.extend([f"goto(268)"])
                    plan.extend([f"Go downstair."])
                if room != robot_room:
                    plan.extend([f"Go to the {room}."])
                    robot_room = room
                if str(object_id) in docker.keys():
                    docker_id = docker[str(object_id)]["id"]
                    docker_name = docker[str(object_id)]["name"]
                    solution.extend([f"goto({docker_id})", "interact()", "grab()"])
                    plan.extend(
                        [f"Go to the {docker_name}.", f"Open the {docker_name}.", f"Pick up the {object_name}."])
                else:
                    if on_id != 0 and on_name != "House4":
                        plan.extend([f"Go to the {on_name}."])
                    solution.extend([f"goto({object_id})", "grab()"])
                    plan.extend([f"Go to the {object_name}.", f"Grab the {object_name}."])
                index = random.choice([1, 2])
                sample = {
                    "task": task,
                    "scene": get_room(robot_pos) + "_" + str(index) + ".png",
                    "plan": plan,
                    "robot_room": get_room(robot_pos),
                    "image": str(object_id) + ".png",
                    "id": object_id,
                    "color": object_color
                }
                all_samples.append(sample)
            print(task, object_id)
    elif type == "goto":
        all_samples = []
        for object_id in interactable_id:
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
                object_pos_y = scene["instances"][object_id]["position"][1]
                if object_pos_y > 2.5 and robot_pos[1] <= 2.5:
                    solution.extend([f"goto(268)"])
                    plan.extend([f"Go upstair."])
                if object_pos_y <= 2.5 and robot_pos[1] > 2.5:
                    solution.extend([f"goto(268)"])
                    plan.extend([f"Go downstair."])
                if room != robot_room:
                    plan.extend([f"Go to the {room}."])
                    robot_room = room
                if str(object_id) in docker.keys():
                    docker_id = docker[str(object_id)]["id"]
                    docker_name = docker[str(object_id)]["name"]
                    solution.extend([f"goto({docker_id})", "interact()"])
                    plan.extend([f"Go to the {docker_name}.", f"Open the {docker_name}."])
                else:
                    if on_id != 0 and on_name != "House4":
                        plan.extend([f"Go to the {on_name}."])
                    solution.extend([f"goto({object_id})"])
                    plan.extend([f"Go to the {object_name}."])
                index = random.choice([1, 2])
                sample = {
                    "task": task,
                    "scene": get_room(robot_pos) + "_" + str(index) + ".png",
                    "plan": plan,
                    "robot_room": get_room(robot_pos),
                    "image": str(object_id) + ".png",
                    "id": object_id,
                    "color": object_color
                }
                all_samples.append(sample)
            print(task, object_id)
    elif type == "new_where":
        all_samples = []
        for object_id in exist:
            on_id, on_name = get_on_which_object(scene, object_id)
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
                if object_id in upstair and robot_pos[1] <= 2.5:
                    solution.extend([f"goto(268)"])
                    plan.extend([f"Go upstair."])
                if object_id in downstair and robot_pos[1] > 2.5:
                    solution.extend([f"goto(268)"])
                    plan.extend([f"Go downstair."])
                if room != robot_room:
                    plan.extend([f"Go to the {room}."])
                    robot_room = room
                if str(object_id) in docker.keys():
                    docker_id = docker[str(object_id)]["id"]
                    docker_name = docker[str(object_id)]["name"]
                    solution.extend([f"goto({docker_id})", "interact()"])
                    plan.extend([f"Go to the {docker_name}.", f"Open the {docker_name}."])
                else:
                    if on_id != 0 and on_name != "House4":
                        plan.extend([f"Go to the {on_name}."])
                plan.extend([f"Reply to the user：It's on the {on_name}."])
                index = random.choice([1, 2])
                sample = {
                    "task": task,
                    "scene": get_room(robot_pos) + "_" + str(index) + ".png",
                    "plan": plan,
                    "robot_room": get_room(robot_pos),
                    "image": str(object_id) + ".png",
                    "id": object_id,
                    "color": object_color
                }
                all_samples.append(sample)
            print(task, object_id)
    elif type == "exist":
        all_samples = []
        for object_id in exist:
            object_name = scene["instances"][object_id]["prefab"].split("LowPolyInterior2_")[1]
            on_id, on_name = get_on_which_object(scene, object_id)
            pos = scene["instances"][object_id]["position"]
            print(object_id, pos)
            room = get_room(pos)
            if on_id == 0 and object_id not in floor or "House4" in on_name:
                continue
            history_task["exist"].append([object_id, on_id])
            if object_name in color.keys():
                object_color = color[object_name] + " "
            else:
                object_color = ""
            if on_name == "Bathroom" or on_name == "Kitchen1" or str(on_id) in docker.keys():
                task = f"Is there a {object_name} in the {on_name}?"
            else:
                task = f"Is there a {object_name} on the {on_name}?"
            for robot_pos in robot_possable_pos:
                robot_room = get_room(robot_pos)
                reply = "Yes."
                solution = []
                plan = []
                if pos[1] > 2.5 and robot_pos[1] <= 2.5:
                    solution.extend([f"goto(268)"])
                    plan.extend([f"Go upstair."])
                if pos[1] <= 2.5 and robot_pos[1] > 2.5:
                    solution.extend([f"goto(268)"])
                    plan.extend([f"Go downstair."])
                if room != robot_room:
                    plan.extend([f"Go to the {room}."])
                    robot_room = room
                if str(object_id) in docker.keys():
                    docker_id = docker[str(object_id)]["id"]
                    docker_name = docker[str(object_id)]["name"]
                    solution.extend([f"goto({docker_id})", "interact()"])
                    plan.extend([f"Go to the {docker_name}.", f"Open the {docker_name}."])
                else:
                    plan.extend([f"Go to the {on_name}."])
                solution.extend([f'speak("{reply}")'])
                plan.extend([f"Check the {on_name}.", f"Reply to the user:YES."])
                index = random.choice([1, 2])
                sample = {
                    "task": task,
                    "scene": get_room(robot_pos) + "_" + str(index) + ".png",
                    "plan": plan,
                    "robot_room": get_room(robot_pos),
                    "image": str(object_id) + ".png",
                    "id": object_id,
                    "color": object_color
                }
                all_samples.append(sample)
    return all_samples


def write_in_file():
    with open("json/scene.json", 'r') as file:
        scene = json.load(file)
    # samples = create_text_task("put", scene=scene, num=7500)
    # with open("result/put.json", 'w') as file:
    #     json.dump(samples, file)
    # samples = create_text_task("exist", scene=scene, num=8000)
    # with open("result/exist.json", 'w') as file:
    #     json.dump(samples, file)
    # samples = test_object(scene,"new_where")
    # with open("result/where.json", 'w') as file:
    #     json.dump(samples, file)
    samples = test_object(scene,"bring")
    with open("result/bring.json", 'w') as file:
        json.dump(samples, file)
    # samples = test_object(scene,"take")
    # print("**************",len(samples))
    # with open("result/take.json", 'w') as file:
    #     json.dump(samples, file)
    # samples = test_object(scene,"goto")
    # print("**************",len(samples))
    # with open("result/goto.json", 'w') as file:
    #     json.dump(samples, file)
    # samples = test_object(scene,"exist")
    # print("**************",len(samples))
    # with open("result/exist_yes.json", 'w') as file:
    #     json.dump(samples, file)
    # room_list = []
    # for robot_pos in robot_possable_pos:
    #     room_list.append(get_room(robot_pos))
    # human_room_list = []
    # for human_pos in human_possable_pos:
    #     human_room_list.append(get_room(human_pos))
    # room = {"robot":room_list,"human":human_room_list}
    # with open("result/room_list.json", 'w') as file:
    #     json.dump(room, file)


if __name__ == "__main__":
    with open("json/scene.json", 'r') as file:
        scene = json.load(file)
    name_id = {}
    for i,instance in enumerate(scene["instances"]):
        pos = instance["position"]
        room = get_room(pos)
        name = instance["prefab"].split("LowPolyInterior2_")[1]
        if str(i) in docker.keys():
            docker_id = docker[str(i)]["id"]
            docker_name = docker[str(i)]["name"]
            docker_key = room + docker_name
            if docker_key not in name_id.keys():
                name_id[docker_key] = [i]
                name_id[docker_key.lower()] = [i]
            else:
                name_id[docker_key].append(i)
                name_id[docker_key.lower()].append(i)
        key = room + name
        if key not in name_id.keys():
            name_id[key] = [i]
            name_id[key.lower()] = [i]
        else:
            name_id[key].append(i)
            name_id[key.lower()].append(i)
    with open("json/name_id.json", 'w') as file:
        json.dump(name_id, file)
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
    # write_in_file()
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
    with open("json/scene.json", 'r') as file:
        scene = json.load(file)
