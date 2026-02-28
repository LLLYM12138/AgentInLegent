import time
import os
import random
import re
import time
from typing import Literal
import numpy as np
from legent.server.scene_generator import generate_scene
from legent.utils.config import TASKS_FOLDER
from legent.utils.io import store_json, load_json_from_toolkit, time_string, scene_string, log_green, log
from legent.utils.math import is_point_on_box
from legent.dataset.chat_prompt import get_prompt
import json

# 21,95,96,136,141,143,144,145,213,214,215,266,315,341,409
# 21:13
# 24,25,26:27
# 45,53,54:68
# 58,59:68
# 95,96:194
# 97,136:192
# 98,129,130,131,132,133,134,135:189
# 141,143,144:194
# 145:191
# 154,155,156:79
# 213,214,215:220
# 225,221,222,226:216
# 235,238:232
# 266:279
# 315:317
# 341:346
# 354,355:259
# 409:114
# 411,412:40
# 413:42
# 416:277
# 418:78
# 296:304
# 309,310,282,283,284,285:301
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

with open("json/history_task.json", 'r') as file:
    history_task = json.load(file)
with open("addressables.json", 'r') as file:
    prefabs = json.load(file)["prefabs"]
prefabs = {prefab["name"]: prefab for prefab in prefabs}


def get_room(pos):
    room = '未定义房间'
    if -6.18 <= pos[0] <= 1.24 and pos[1] <= 2.5 and -4.8 <= pos[2] <= 2.60:
        room = "1楼客厅和厨房"
    elif -6.18 <= pos[0] <= -1.25 and pos[1] <= 2.5 and 2.60 <= pos[2] <= 4.93:
        room = "1楼卫生间1"
    elif -1.25 <= pos[0] <= -3.6 and pos[1] <= 2.5 and 2.60 <= pos[2] <= 4.93:
        room = "1楼衣帽间1"
    elif 1.34 <= pos[0] <= 6.18 and pos[1] <= 2.5 and -4.8 <= pos[2] <= 0:
        room = "1楼卧室1"
    elif 1.34 <= pos[0] <= 6.18 and pos[1] <= 2.5 and 0 <= pos[2] <= 2.5:
        room = "1楼衣帽间2"
    elif 3.7 <= pos[0] <= 6.18 and pos[1] <= 2.5 and 2.5 <= pos[2] <= 5.0:
        room = "1楼卫生间2"
    elif -1.15 <= pos[0] <= 6.18 and pos[1] >= 2.5 and 0.5 <= pos[2] <= 5.0:
        room = "2楼卧室1"
    elif 3.75 <= pos[0] <= 6.18 and pos[1] >= 2.5 and -4.95 <= pos[2] <= 0.5:
        room = "2楼卫生间1"
    elif -6.15 <= pos[0] <= -3.75 and pos[1] >= 2.5 and 2.6 <= pos[2] <= 4.9:
        room = "2楼衣帽间1"
    elif (-3.75 <= pos[0] <= -1.23 and pos[1] >= 2.5 and -2.39 <= pos[2] <= 4.9) or \
            (-6.15 <= pos[0] <= -1.23 and pos[1] >= 2.5 and -2.39 <= pos[2] <= -0.15):
        room = "2楼走廊"
    elif -1.23 <= pos[0] <= 3.6 and pos[1] >= 2.5 and -4.9 <= pos[2] <= 0:
        room = "2楼卧室2"
    elif -3.75 <= pos[0] <= -1.23 and pos[1] >= 2.5 and -4.9 <= pos[2] <= -2.5:
        room = "2楼衣帽间2"
    elif -6.18 <= pos[0] <= -3.75 and pos[1] >= 2.5 and -4.9 <= pos[2] <= -2.5:
        room = "2楼卫生间2"
    return room


def get_on_which_object(scene, object_id):
    on_candidates = []
    object_pos = scene["instances"][object_id]["position"]
    on_id, on_name = None, None
    # get all candidates Floor->Table->Plate->Apple, [Floor, Table, Plate]
    for i, instance in enumerate(scene["instances"]):
        # TODO: get size from observation.game_states
        pos, size, rot = np.array(instance["position"]), np.array(
            prefabs[instance["prefab"]]["size"]), np.array(instance["rotation"])
        if i != object_id and is_point_on_box(object_pos, pos, size, box_rotation=rot):  # TODO: consider more
            on_candidates.append(i)
    max_y = -100
    on_id = None
    for i in on_candidates:
        if scene["instances"][i]["position"][1] > max_y:
            max_y = scene["instances"][i]["position"][1]
            on_id = i

    if on_id is not None:
        on_name = scene["instances"][on_id]["prefab"].split("_")[1]
    if on_id is None and on_name is None:
        on_id = 0
        on_name = "House4"
    if str(on_id) in docker.keys():
        on_name = docker[str(on_id)]["name"]
    return on_id, on_name


class ChatAPI:
    def __init__(self, api_key=None, base_url=None) -> None:
        import openai

        if api_key:
            self.client = openai.OpenAI(api_key=api_key, base_url=base_url)

    def send_chat(self, messages):
        response = self.client.chat.completions.create(
            model="gpt-4",  # 'gpt-3.5-turbo', 'gpt-3.5-turbo-16k', 'gpt-4', 'gpt-4-32k'
            messages=messages,
            max_tokens=None,
            n=1,
            stop=None,
            temperature=0.7,
        )
        ret = response.choices[0].message.content
        return ret



registered_api = [ChatAPI]


def chat_api():
    global registered_api

    def decorator(api_class):
        registered_api.append(api_class)
        log(f"register API: {api_class.__name__}")
        return api_class

    return decorator


class ChatBase:
    def __init__(self, api_key=None, base_url=None) -> None:
        global registered_api
        self.chat_api = registered_api[-1](api_key, base_url)

    def send_chat(self, messages):
        return self.chat_api.send_chat(messages)


class TaskCreator(ChatBase):

    def create_task_for_scene_by_hardcoding(self,
                                            task_type=Literal["come", "goto", "take", "bring", "put", "where", "exist"],
                                            scene=None, room_num=2):
        # TODO: verified the correctness of all cases
        global exist

        def get_random_object(scene):
            # object_candidates = []
            # for i, instance in enumerate(scene["instances"]):
            #     if instance["type"] == "interactable":
            #         object_candidates.append(i)
            object_id = random.choice(interactable_id)
            object_name = scene["instances"][object_id]["prefab"].split("_")[1]
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
            target_name = scene["instances"][target_id]["prefab"].split("_")[1]
            return target_id, target_name

        def get_random_place(scene):
            object_id = random.choice(interactable_id + target)
            object_name = scene["instances"][object_id]["prefab"].split("_")[1]
            return object_id, object_name

        # eg.pos = [1.0, 1.0, 1.0]
        def get_room(pos):
            room = '未定义房间'
            if -6.18 <= pos[0] <= 1.24 and pos[1] <= 2.5 and -4.8 <= pos[2] <= 2.60:
                room = "1楼客厅和厨房"
            elif -6.18 <= pos[0] <= -1.25 and pos[1] <= 2.5 and 2.60 <= pos[2] <= 4.93:
                room = "1楼卫生间1"
            elif -1.25 <= pos[0] <= -3.6 and pos[1] <= 2.5 and 2.60 <= pos[2] <= 4.93:
                room = "1楼衣帽间1"
            elif 1.34 <= pos[0] <= 6.18 and pos[1] <= 2.5 and -4.8 <= pos[2] <= 0:
                room = "1楼卧室1"
            elif 1.34 <= pos[0] <= 6.18 and pos[1] <= 2.5 and 0 <= pos[2] <= 2.5:
                room = "1楼衣帽间2"
            elif 3.7 <= pos[0] <= 6.18 and pos[1] <= 2.5 and 2.5 <= pos[2] <= 5.0:
                room = "1楼卫生间2"
            elif -1.15 <= pos[0] <= 6.18 and pos[1] >= 2.5 and 0.5 <= pos[2] <= 5.0:
                room = "2楼卧室1"
            elif 3.75 <= pos[0] <= 6.18 and pos[1] >= 2.5 and -4.95 <= pos[2] <= 0.5:
                room = "2楼卫生间1"
            elif -6.15 <= pos[0] <= -3.75 and pos[1] >= 2.5 and 2.6 <= pos[2] <= 4.9:
                room = "2楼衣帽间1"
            elif (-3.75 <= pos[0] <= -1.23 and pos[1] >= 2.5 and -2.39 <= pos[2] <= 4.9) or \
                    (-6.15 <= pos[0] <= -1.23 and pos[1] >= 2.5 and -2.39 <= pos[2] <= -0.15):
                room = "2楼走廊"
            elif -1.23 <= pos[0] <= 3.6 and pos[1] >= 2.5 and -4.9 <= pos[2] <= 0:
                room = "2楼卧室2"
            elif -3.75 <= pos[0] <= -1.23 and pos[1] >= 2.5 and -4.9 <= pos[2] <= -2.5:
                room = "2楼衣帽间2"
            elif -6.18 <= pos[0] <= -3.75 and pos[1] >= 2.5 and -4.9 <= pos[2] <= -2.5:
                room = "2楼卫生间2"
            return room

        def get_on_which_object(scene, object_id):
            on_candidates = []
            object_pos = scene["instances"][object_id]["position"]
            on_id, on_name = None, None
            # get all candidates Floor->Table->Plate->Apple, [Floor, Table, Plate]
            for i, instance in enumerate(scene["instances"]):
                # TODO: get size from observation.game_states
                pos, size, rot = np.array(instance["position"]), np.array(
                    prefabs[instance["prefab"]]["size"]), np.array(instance["rotation"])
                if i != object_id and is_point_on_box(object_pos, pos, size, box_rotation=rot):  # TODO: consider more
                    on_candidates.append(i)
            max_y = -100
            on_id = None
            for i in on_candidates:
                if scene["instances"][i]["position"][1] > max_y:
                    max_y = scene["instances"][i]["position"][1]
                    on_id = i

            if on_id is not None:
                on_name = scene["instances"][on_id]["prefab"].split("_")[1]
            if on_id is None and on_name is None:
                on_id = 0
                on_name = "House4"
            if str(on_id) in docker.keys():
                on_name = docker[str(on_id)]["name"]
            return on_id, on_name

        # generate a scene
        if not scene:
            scene = generate_scene(room_num=room_num)

        # generate (task, plan, solution) triplets
        if task_type == "come":
            task = "Come here."
            solution = ["goto_user()"]
            plan = ["Go to the user."]

        elif task_type == "goto":
            object_id, object_name = get_random_object(scene)
            task = f"Go to the {object_name}."
            solution = []
            plan = []
            if object_id in upstair:
                solution.extend([f"goto(268)"])
                plan.extend([f"Go upstair."])
            if str(object_id) in docker.keys():
                docker_id = docker[str(object_id)]["id"]
                docker_name = docker[str(object_id)]["name"]
                solution.extend([f"goto({docker_id})", "interact()", "grab()"])
                plan.extend([f"Go to the {docker_name}.", f"Open the {docker_name}.", f"Pick up the {object_name}."])
            else:
                solution.extend([f"goto({object_id})"])
                plan.extend([f"Go to the {object_name}."])

        elif task_type == "take":
            object_id, object_name = get_random_object(scene)
            task = f"Take the {object_name}."
            solution = []
            plan = []
            if object_id in upstair:
                solution.extend([f"goto(268)"])
                plan.extend([f"Go upstair."])
            if str(object_id) in docker.keys():
                docker_id = docker[str(object_id)]["id"]
                docker_name = docker[str(object_id)]["name"]
                solution.extend([f"goto({docker_id})", "interact()", "grab()"])
                plan.extend([f"Go to the {docker_name}.", f"Open the {docker_name}.", f"Pick up the {object_name}."])
            else:
                solution.extend([f"goto({object_id})", "grab()"])
                plan.extend([f"Go to the {object_name}.", f"Grab the {object_name}."])

        elif task_type == "bring":
            object_id, object_name = get_random_object(scene)
            task = f"Bring the {object_name}."
            solution = []
            plan = []
            if object_id in upstair:
                solution.extend([f"goto(268)"])
                plan.extend([f"Go upstair."])
            if str(object_id) in docker.keys():
                docker_id = docker[str(object_id)]["id"]
                docker_name = docker[str(object_id)]["name"]
                solution.extend([f"goto({docker_id})", "interact()", "grab()"])
                plan.extend([f"Go to the {docker_name}.", f"Open the {docker_name}.", f"Pick up the {object_name}."])
            else:
                solution.extend([f"goto({object_id})", "grab()"])
                plan.extend([f"Go to the {object_name}.", f"Grab the {object_name}."])
            if object_id in upstair:
                solution.extend([f"goto(51)"])
                plan.extend([f"Go downstair."])
            solution.extend(["goto_user()"])
            plan.extend(["Go to the user."])

        elif task_type == "put":
            while True:
                object_id, object_name = get_random_object(scene)
                target_id, target_name = get_random_target(scene, object_id)
                if [object_id, target_id] not in history_task["put"]:
                    history_task["put"].append([object_id, target_id])
                    break
            task = f"Put the {object_name} on the {target_name}."
            solution = []
            plan = []
            if object_id in upstair:
                solution.extend([f"goto(268)"])
                plan.extend([f"Go upstair."])
            if str(object_id) in docker.keys():
                docker_id = docker[str(object_id)]["id"]
                docker_name = docker[str(object_id)]["name"]
                solution.extend([f"goto({docker_id})", "interact()", "grab()"])
                plan.extend([f"Go to the {docker_name}.", f"Open the {docker_name}.", f"Pick up the {object_name}."])
            else:
                solution.extend([f"goto({object_id})", "grab()"])
                plan.extend([f"Go to the {object_name}.", f"Grab the {object_name}."])
            if object_id in upstair and target_name in downstair:
                solution.extend([f"goto(51)"])
                plan.extend([f"Go downstair."])
            elif object_id in downstair and target_name in upstair:
                solution.extend([f"goto(268)"])
                plan.extend([f"Go upstair."])
            solution.extend([f"goto({target_id})"])
            plan.extend([f"Go to the {target_name}."])
            if target_id in box:
                solution.extend([f"lookDown()", "release()"])
                plan.extend([f"Look down.", f"Release the {object_name}."])
                solution.extend([f"goto({target_id})", "interact()"])
                plan.extend([f"Go to the {target_name}.", f"Open the {target_name}."])
                solution.extend([f"goto({object_id})", "grab()"])
                plan.extend([f"Go to the {object_name}.", f"Grab the {object_name}."])
                solution.extend([f"goto({target_id})", f"release()"])
                plan.extend([f"Go to the {target_name}.", f"Release the {object_name}."])
            else:
                solution.extend([f"release()"])
                plan.extend([f"Release the {object_name}."])

        elif task_type == "where":
            # TODO: use ChatGPT
            while True:
                object_id, object_name = get_random_object(scene)
                on_id, on_name = get_on_which_object(scene, object_id)
                if on_id != 0:
                    history_task["where"].append(object_id)
                    break
            task = f"Where is the {object_name}?"
            reply = f"It's on the {on_name}."
            solution = []
            plan = []
            random_object_id_old = 4
            wrong_times = random.choice([1, 2, 3, 4])
            for i in range(0, wrong_times):
                random_object_id, random_object_name = get_random_place(scene)
                if random_object_id in upstair and random_object_id_old in downstair:
                    solution.extend([f"goto(268)"])
                    plan.extend([f"Go upstair."])
                elif random_object_id in downstair and random_object_id_old in upstair:
                    solution.extend([f"goto(51)"])
                    plan.extend([f"Go downstair."])
                solution.extend([f"goto({random_object_id})", f'speak("It\'s not on the {random_object_name}.")'])
                plan.extend([f"Go to the {random_object_name}.", "Reply to the user."])
                random_object_id_old = random_object_id
            if on_id in upstair and random_object_id_old in downstair:
                solution.extend([f"goto(268)"])
                plan.extend([f"Go upstair."])
            elif on_id in downstair and random_object_id_old in upstair:
                solution.extend([f"goto(51)"])
                plan.extend([f"Go downstair."])
            solution.extend([f"goto({on_id})", f'speak("{reply}")'])
            plan.extend([f"Go to the {on_name}.", "Reply to the user."])

        elif task_type == "exist":

            random_number = random.random()
            if False:
                # create "Yes"
                while True:
                    object_id, object_name = get_random_object(scene)
                    on_id, on_name = get_on_which_object(scene, object_id)
                    if on_id != 0 and [object_id, on_id] not in history_task["exist"]:
                        history_task["exist"].append([object_id, on_id])
                        break
                task = f"Is there a {object_name} on the {on_name}?"
                reply = "Yes."
                solution = [f"goto({on_id})"]
                plan = [f"Go to the {on_name}."]
                if str(object_id) in docker.keys():
                    solution.extend(["interact()"])
                    guizi = docker[str(object_id)]["name"]
                    plan.extend([f"Open the {guizi}."])
                solution.extend([f'speak("{reply}")'])
                plan.extend(["Reply to the user."])
            else:
                # TODO: create "No" (select a on_id and get all objects on it. random select one object not included.)
                # create "No"
                while True:
                    object_id = random.choice(exist)
                    object_name = scene["instances"][object_id]["prefab"].split("_")[1]
                    on_id_no, on_name_no = get_on_which_object(scene, object_id)
                    flag = 0
                    for on_id in target:
                        on_name = scene["instances"][on_id]["prefab"].split("_")[1]
                        if on_id != on_id_no and [object_name, on_id] not in history_task[
                            "exist"]:  # 如果新随机出来的物品与之前的物品在同一个桌子上
                            history_task["exist"].append([object_name, on_id])
                            flag = 1
                            break
                    if flag == 0:
                        exist = list(set(exist) - set([object_id]))
                    else:
                        break

                if on_name == "Bathroom" or on_name == "Kitchen1" or str(on_id) in docker.keys():
                    task = f"Is there a {object_name} in the {on_name}?"
                else:
                    task = f"Is there a {object_name} on the {on_name}?"
                reply = "No"
                solution = [f"goto({on_id})"]
                plan = [f"Go to the {on_name}."]
                if str(object_id) in docker.keys():
                    solution.extend(["interact()"])
                    guizi = docker[str(object_id)]["name"]
                    plan.extend([f"Open the {guizi}."])
                solution.extend([f'speak("{reply}")'])
                plan.extend(["Reply to the user."])
            # # create "Yes"
            # object_id, object_name = get_random_object()
            # on_id, on_name = get_on_which_object(scene, object_id)
            # task = f"Is there a {object_name} on the {on_name}."
            # reply = "Yes."
            # solution = [f"goto({on_id})", f'speak("{reply}")']
            # plan = [f"Go to the {on_name}.", "Reply to the user."]
            # # TODO: create "No" (select a on_id and get all objects on it. random select one object not included.)

        sample = {"task": task, "plan": plan, "solution": solution, "scene": scene}
        if task_type == 'put':
            sample["object"] = object_id
            sample["target"] = target_id
            if str(object_id) in docker.keys():
                sample["docker"] = docker_id
        samples = [sample]
        return samples

    def test_object(self, scene, id=None, target=None, type="goto"):
        all_samples = []
        if id is None and type == "bring":
            for object_id in interactable_id:
                object_name = scene["instances"][object_id]["prefab"].split("_")[1]
                task = f"Bring the {object_name}."
                solution = []
                plan = []
                if object_id in upstair:
                    solution.extend([f"goto(268)"])
                    plan.extend([f"Go upstair."])
                if str(object_id) in docker.keys():
                    docker_id = docker[str(object_id)]["id"]
                    docker_name = docker[str(object_id)]["name"]
                    solution.extend([f"goto({docker_id})", "interact()", "grab()"])
                    plan.extend(
                        [f"Go to the {docker_name}.", f"Open the {docker_name}.", f"Pick up the {object_name}."])
                else:
                    solution.extend([f"goto({object_id})", "grab()"])
                    plan.extend([f"Go to the {object_name}.", f"Grab the {object_name}."])
                if object_id in upstair:
                    solution.extend([f"goto(51)"])
                    plan.extend([f"Go downstair."])
                solution.extend(["goto_user()"])
                plan.extend(["Go to the user."])
                sample = {"task": task, "plan": plan, "solution": solution, "scene": scene}
                samples = [sample]
                all_samples.extend(samples)
        elif id is None and type == "take":
            for object_id in interactable_id:
                object_name = scene["instances"][object_id]["prefab"].split("_")[1]
                task = f"Take the {object_name}."
                solution = []
                plan = []
                if object_id in upstair:
                    solution.extend([f"goto(268)"])
                    plan.extend([f"Go upstair."])
                if str(object_id) in docker.keys():
                    docker_id = docker[str(object_id)]["id"]
                    docker_name = docker[str(object_id)]["name"]
                    solution.extend([f"goto({docker_id})", "interact()", "grab()"])
                    plan.extend(
                        [f"Go to the {docker_name}.", f"Open the {docker_name}.", f"Pick up the {object_name}."])
                else:
                    solution.extend([f"goto({object_id})", "grab()"])
                    plan.extend([f"Go to the {object_name}.", f"Grab the {object_name}."])
                sample = {"task": task, "plan": plan, "solution": solution, "scene": scene}
                samples = [sample]
                all_samples.extend(samples)
        elif type == "goto":
            # for object_id in interactable_id:
            object_id = id
            object_name = scene["instances"][object_id]["prefab"].split("_")[1]
            task = f"Go to the {object_name}."
            solution = []
            plan = []
            if object_id in upstair:
                solution.extend([f"goto(268)"])
                plan.extend([f"Go upstair."])
            if str(object_id) in docker.keys():
                docker_id = docker[str(object_id)]["id"]
                docker_name = docker[str(object_id)]["name"]
                solution.extend([f"goto({docker_id})", "interact()"])
                plan.extend([f"Go to the {docker_name}.", f"Open the {docker_name}."])
            else:
                solution.extend([f"goto({object_id})"])
                plan.extend([f"Go to the {object_name}."])
            sample = {"task": task, "plan": plan, "solution": solution, "scene": scene}
            samples = [sample]
            all_samples.extend(samples)
        elif id is None and type == "exist":
            def get_on_which_object(scene, object_id):
                on_candidates = []
                object_pos = scene["instances"][object_id]["position"]
                on_id, on_name = None, None
                # get all candidates Floor->Table->Plate->Apple, [Floor, Table, Plate]
                for i, instance in enumerate(scene["instances"]):
                    # TODO: get size from observation.game_states
                    pos, size, rot = np.array(instance["position"]), np.array(
                        prefabs[instance["prefab"]]["size"]), np.array(instance["rotation"])
                    if i != object_id and is_point_on_box(object_pos, pos, size,
                                                          box_rotation=rot):  # TODO: consider more
                        on_candidates.append(i)
                max_y = -100
                on_id = None
                for i in on_candidates:
                    if scene["instances"][i]["position"][1] > max_y:
                        max_y = scene["instances"][i]["position"][1]
                        on_id = i

                if on_id is not None:
                    on_name = scene["instances"][on_id]["prefab"].split("_")[1]
                if (on_id is None and on_name is None) or on_id == 0:
                    on_id = 0
                    on_name = "Floor"
                if str(on_id) in docker.keys():
                    on_name = docker[str(on_id)]["name"]
                return on_id, on_name

            for object_id in range(1, 417):
                object_name = scene["instances"][object_id]["prefab"].split("_")[1]
                on_id, on_name = get_on_which_object(scene, object_id)
                if on_id == 0 and object_id not in floor:
                    continue
                history_task["exist"].append([object_id, on_id])
                # print(object_id,end = ",")
                if on_name == "Bathroom" or on_name == "Kitchen1" or str(on_id) in docker.keys():
                    task = f"Is there a {object_name} in the {on_name}?"
                else:
                    task = f"Is there a {object_name} on the {on_name}?"
                reply = "Yes."
                solution = [f"goto({object_id})"]
                plan = [f"Go to the {on_name}."]
                if str(object_id) in docker.keys():
                    solution.extend(["interact()"])
                    guizi = docker[str(object_id)]["name"]
                    plan.extend([f"Open the {guizi}."])
                solution.extend([f'speak("{reply}")'])
                plan.extend(["Reply to the user."])
                sample = {"task": task, "plan": plan, "solution": solution, "scene": scene}
                samples = [sample]
                all_samples.extend(samples)
        elif type == "on":
            on_candidates = []
            object_pos = scene["instances"][id]["position"]
            on_id, on_name = None, None
            # get all candidates Floor->Table->Plate->Apple, [Floor, Table, Plate]
            for i, instance in enumerate(scene["instances"]):
                # TODO: get size from observation.game_states
                pos, size, rot = np.array(instance["position"]), np.array(
                    prefabs[instance["prefab"]]["size"]), np.array(instance["rotation"])
                if i != id and is_point_on_box(object_pos, pos, size, box_rotation=rot):  # TODO: consider more
                    on_candidates.append(i)
            max_y = -100
            on_id = None
            for i in on_candidates:
                if scene["instances"][i]["position"][1] > max_y:
                    max_y = scene["instances"][i]["position"][1]
                    on_id = i

            if on_id is not None:
                on_name = scene["instances"][on_id]["prefab"].split("_")[1]
            if on_id is None and on_name is None:
                on_id = 0
                on_name = "House4"
            return on_id, on_name

        elif type == "put":
            object_id = id
            target_id = target
            object_name = scene["instances"][id]["prefab"].split("_")[1]
            target_name = scene["instances"][target]["prefab"].split("_")[1]
            task = f"Put the {object_name} on the {target_name}."
            solution = []
            plan = []
            if object_id in upstair:
                solution.extend([f"goto(268)"])
                plan.extend([f"Go upstair."])
            if str(object_id) in docker.keys():
                docker_id = docker[str(object_id)]["id"]
                docker_name = docker[str(object_id)]["name"]
                solution.extend([f"goto({docker_id})", "interact()", "grab()"])
                plan.extend([f"Go to the {docker_name}.", f"Open the {docker_name}.", f"Pick up the {object_name}."])
            else:
                solution.extend([f"goto({object_id})", "grab()"])
                plan.extend([f"Go to the {object_name}.", f"Grab the {object_name}."])
            if object_id in upstair and target_name in downstair:
                solution.extend([f"goto(51)"])
                plan.extend([f"Go downstair."])
            elif object_id in downstair and target_name in upstair:
                solution.extend([f"goto(268)"])
                plan.extend([f"Go upstair."])
            solution.extend([f"goto({target_id})"])
            plan.extend([f"Go to the {target_name}."])
            if target_id in box:
                solution.extend([f"lookDown()", "release()"])
                plan.extend([f"Look down.", f"Release the {object_name}."])
                solution.extend([f"goto({target_id})", "interact()"])
                plan.extend([f"Go to the {target_name}.", f"Open the {target_name}."])
                solution.extend([f"goto({object_id})", "grab()"])
                plan.extend([f"Go to the {object_name}.", f"Grab the {object_name}."])
                solution.extend([f"goto({target_id})", f"release()"])
                plan.extend([f"Go to the {target_name}.", f"Release the {object_name}."])
            elif target_id in [39, 406, 81, 180]:
                solution.extend(["moveForward()", f"lookat({target_id})", f"release()"])
                plan.extend([f"Release the {object_name}."])
            else:
                solution.extend([f"release()"])
                plan.extend([f"Release the {object_name}."])

            sample = {"task": task, "plan": plan, "solution": solution, "scene": scene}
            samples = [sample]
            all_samples.extend(samples)

        return all_samples

    def create_task_for_scene_by_prompting(self,
                                           task_type=Literal["come", "goto", "take", "bring", "put", "where", "exist"],
                                           scene=None, sample_num=1):
        if not scene:
            scene = generate_scene()

        task_prompt = {p["type"]: p for p in load_json_from_toolkit("dataset/task-prompts.json")}[task_type]
        if task_prompt["TYPE"] == "instrution following":
            system_message = "You are a user in the room. You need to ask a robot do something."
        else:
            system_message = "You are a user in the room. You need to ask a robot some questions."

        scene_str = scene_string(scene)

        scene_description = f"You are in a room with the following objects(in table format):\n{scene_str}"

        # TODO: give more examples to improve the results. use inputs and outputs from hardcoding as examples
        examples = [f"Task: {e['example']}; Plan: {e['plan']}; Solution: {e['solution']}" for e in
                    task_prompt["examples"]]
        task_prompt["example"] = "\n".join(examples)
        # TODO: Add descriptions for functions goto_user(), goto(object_id), grab(), release().
        task_description = f"""You need to {task_prompt['message']}
You need to propose {sample_num} independent tasks and corresponding solutions, in the format of "Task: task; Plan: plan; Solution: solution.", with no line breaks between the three (use ';' to seperate). 
One sentence in Plan should match one function call in Solution, and the Solution should contain only the following instructions and no other irrelevant output:
1. goto_user()
2. goto(object_id): go to the object and look at it
3. find(object_id): find the object to answer where it is (no need to approach it)
4. grab(): grab the object you are looking at
5. release(): put the grabbed object onto what you have gone to
6. speak(text)
For example (The examples are from other scenes. The number means object_id):
{task_prompt['example']}
"""
        content = f"{scene_description}\n{task_description}"
        messages = [
            {"role": "system", "content": system_message},
            {"role": "assistant", "content": task_prompt["example"]},  # this message can ensure the format correct
            {"role": "user", "content": content},
        ]

        ret = self.send_chat(messages)

        log_green(f"<g>Send to LLM</g>:\n{content}\n<g>Received from LLM</g>:\n{ret}")

        task_lines = [task for task in ret.split("\n") if task]
        samples = []
        for task in task_lines:
            task, plan, solution = task.split("; ")
            task, plan, solution = task.split(": ")[1], plan.split(": ")[1], solution.split(": ")[1]
            sample = {"task": task, "plan": plan.split(". "), "solution": solution.split(", "), "scene": scene}
            samples.append(sample)
        print({"task": task, "plan": plan, "solution": solution})
        time.sleep(0.5)
        return samples

    def create_task_for_scene_by_chatting(self, scene=None):
        raise NotImplementedError

    def create_tasks(self, scene, task_types=None,
                     method: Literal["hardcoding", "prompting", "chatting"] = "hardcoding", scene_num=1):
        if not task_types:
            task_types = [p["type"] for p in load_json_from_toolkit("dataset/task-prompts.json")]
        save_path = f"{TASKS_FOLDER}/{method}/{time_string()}"
        create_func = {
            "hardcoding": self.create_task_for_scene_by_hardcoding,
            "prompting": self.create_task_for_scene_by_prompting,
            "chatting": self.create_task_for_scene_by_chatting,
        }[method]
        all_samples = []

        for task_type in task_types:
            task_save_path = f"{save_path}/{task_type}"
            os.makedirs(task_save_path)

            for scene_id in range(scene_num):
                samples = create_func(task_type, scene=scene)
                all_samples.extend(samples)
                for sample_id, sample in enumerate(samples):
                    store_json(sample, f"{task_save_path}/scene{scene_id}_task{sample_id}.json")
        return all_samples

    def create_scene_for_task_by_hardcoding(self, task_type="where", object_cands=None, receptacle_cands=None,
                                            room_num=1):
        # TODO: add goto task to this function
        if task_type == "where":
            if object_cands is None:
                object_cands = ["Orange", "Apple", "Banana", "Cola"]
            object_text = {"Orange": "orange", "Apple": "apple", "Banana": "banana", "Cola": "cola"}
            object_prefab = {"Orange": "LowPolyInterior_Orange", "Apple": "LowPolyInterior_Apple",
                             "Banana": "LowPolyInterior_Banana", "Cola": "LowPolyInterior_Cola"}

            if receptacle_cands is None:
                receptacle_cands = ["Sofa", "Kitchen_Chair", "Table", "Bar", "Dresser"]  # Kitchenchair, Giftbox
            receptacle_text = {"Sofa": "sofa", "Kitchen_Chair": "chair", "Table": "table", "Bar": "countertop",
                               "Dresser": "dresser"}

            exclusions = {"Banana-Kitchen_Chair"}
            while True:
                object_name = random.choice(object_cands)
                receptacle_name = random.choice(receptacle_cands)
                if f"{object_name}-{receptacle_name}" not in exclusions:
                    break

            receptacle_object_counts = {receptacle_name: {"count": 1, "objects": [{object_name: 1}]}}
            # receptacle_object_counts = {"Sofa": {"count": 1, "objects": [{"Apple": 1}]}}
            object_id = -1
            loop_count = 0
            # Banana KitchenChair
            # Apple Sofa
            while object_id == -1:  # Failed to put the object
                # print(".", end="", flush=True)
                # print(receptacle_object_counts)
                scene = generate_scene(receptacle_object_counts=receptacle_object_counts, room_num=room_num)
                loop_count += 1
                if loop_count > 4:
                    raise Exception(f"failed to put {object_name} on {receptacle_name} after many attempts")
                for i, instance in enumerate(scene["instances"]):
                    if instance["prefab"] == object_prefab[object_name]:
                        object_id = i
                        break
            question_text = object_text[object_name]
            answer_text = receptacle_text[receptacle_name]
            task = f"Where is the {question_text}?"
            reply = f"It's on the {answer_text}."
            solution = [f"find({object_id})", f'speak("{reply}")']
            plan = [f"Go to the {question_text}.", "Reply to the user."]
            sample = {"task": task, "plan": plan, "solution": solution, "scene": scene, "answer": answer_text}
            return sample
        else:
            raise NotImplementedError

    def create_scenes_for_task_by_hardcoding(self, task_type="where", scene_num=1):
        return [self.create_scene_for_task_by_hardcoding(task_type=task_type) for i in range(scene_num)]


class ChatAnnotator(ChatBase):
    def __init__(self, api_key=None, base_url=None, add_history=False):
        super().__init__(api_key, base_url)
        self.add_history = add_history
        self.messages = [{"role": "system", "content": "You are a helpful assistant."}]

    def _annotate_solution(self, user_chat, game_states):
        prompt = get_prompt(user_chat, game_states)
        messages = self.messages + [{"role": "user", "content": prompt}]
        return self.send_chat(messages)

    def annotate_solution(self, user_chat, game_states):
        solution = self._annotate_solution(user_chat, game_states)
        if self.add_history:
            messages += [{"role": "user", "content": user_chat}, {"role": "assistant", "content": solution}]
            reserved_turn = 3
            if len(messages) > 1 + reserved_turn * 2:
                messages = messages[:1] + messages[-reserved_turn * 2:]
        log_green(f"<g>user:</g>\n{user_chat}")
        log_green(f"<g>agent:</g>\n{solution}")
        if solution == "" or solution.startswith("<!doctype html>"):
            solution = 'speak("Request failed.")'

        apis = ["speak", "speak_without_look", "play", "goto_user", "goto", "goto_point", "toggle", "put_in_drawer",
                "goto_and_grab", "grab", "goto_and_grab", "release", "look", "open", "speak_and_play"]

        def is_valid(p):
            for action in p.split("\n"):
                action = action.strip()
                if any([action.startswith(f"{api}(") for api in apis]) and action.endswith(")"):
                    continue
                else:
                    print(f"solution '{action}' not valid, skip")
            return True

        def post_process(p):
            if is_valid(p):
                res = []
                for action in p.split("\n"):
                    action = action.strip()
                    try:
                        func = action.split("(", maxsplit=1)[0]
                        arg = action.split("(", maxsplit=1)[1][:-1].strip('"')
                    except:
                        continue
                    res.append(func + ":" + arg)
                for i in range(len(res) - 1):
                    if res[i].startswith("look") and res[i + 1].startswith("speak"):  # TODO: refactor the logic
                        res[i + 1] = "speak_without_look:" + res[i + 1].split(":", maxsplit=1)[1]
                return "\n".join(res)
            else:
                if "\n" not in p and not re.search(r"[a-z]", p):
                    return f"speak:{p}"
                return ""

        solution = post_process(solution.strip())
        return solution
