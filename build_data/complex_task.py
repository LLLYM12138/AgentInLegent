# coding=utf-8
#生成更多复杂任务
from typing import Literal
import numpy as np
import random
import json
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
         48, 50, 51, 66, 67, 68, 71, 82, 83,
         84, 85, 112, 113, 114, 176, 183, 184, 196, 201,
         205, 217, 218, 220, 228, 229, 233, 234, 243, 241,
         244, 268, 271, 274, 275, 312, 318, 328, 335, 336,
         337, 343, 348, 353, 381, 382, 388, 389, 390, 391,
         405, 414, 415]
with open("json/history_task.json", 'r') as file:
    history_task = json.load(file)
with open("addressables.json", 'r') as file:
    prefabs = json.load(file)["prefabs"]
prefabs = {prefab["name"]: prefab for prefab in prefabs}


def create_complex_task(task_type=Literal["find_and_bring","collect","block","pyramid","fruit","cup"], scene=None):
    # TODO: verified the correctness of all cases
    global exist

    def get_random_object(scene):
        object_id = random.choice(interactable_id)
        object_name = scene["instances"][object_id]["prefab"].split("_")[1]
        # print(object_id, object_name)
        return object_id, object_name

    def get_random_target(scene):
        target_id = random.choice(target)
        target_name = scene["instances"][target_id]["prefab"].split("_")[1]
        return target_id, target_name

    def get_random_place(scene):
        object_id = random.choice(interactable_id + target)
        object_name = scene["instances"][object_id]["prefab"].split("_")[1]
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
            on_name = scene["instances"][on_id]["prefab"].split("_")[1]
        if on_id is None and on_name is None:
            on_id = 0
            on_name = "House4"
        if str(on_id) in docker.keys():
            on_name = docker[str(on_id)]["name"]
        return on_id, on_name

    # generate (task, plan, solution) triplets
    if task_type == "find_and_bring":
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

    sample = {"task": task, "plan": plan, "solution": solution, "scene": scene}
    samples = [sample]
    return samples


def ComplexTask(scene, task_type=None, scene_num=1):
    all_samples = []
    for scene_id in range(scene_num):
        samples = create_complex_task(task_type, scene=scene)
        all_samples.extend(samples)
    return all_samples
