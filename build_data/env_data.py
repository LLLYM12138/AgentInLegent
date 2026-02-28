# coding=utf-8
#生成环境数据集
import os.path

from legent import Environment, ResetInfo, TaskCreator, Controller, TrajectorySaver, load_json, Action, Observation
import pkg_resources
import json
import random

random_pos = [
    {"position": [0.847, 0.131, 2.9777], "rotation": [-1.0, 0.0, 0.13]},
    {"position": [0.20892, 0.3021, -4.5404], "rotation": [-0.73, 0.0, 0.68]},
    {"position": [0.84, 0.132, -2.43], "rotation": [-0.93, 0.00, 0.34]},
    {"position": [-1.69, 0.132, 2.895], "rotation": [-0.933, 0.00, 0.359]},
    {"position": [5.848, 0.1321, -4.48], "rotation": [-0.76, 0.00, 0.647]},
    {"position": [5.848, 0.1321, -4.48], "rotation": [-0.76, 0.00, 0.647]},
]


def reset_player(scene):
    pos = random.choice(random_pos)
    scene["player"]["position"] = pos["position"]
    scene["player"]["rotation"] = pos["rotation"]
    return scene


def save_task_info(task, task_info):
    if "Go to" in task["task"]:
        if "grab" in task['solution'][-1]:
            task_info["goto_docker"] += 1
        else:
            task_info["goto"] += 1
    elif "Take" in task["task"]:
        if "Open" in task['plan'][-1]:
            task_info["take_docker"] += 1
        else:
            task_info["take"] += 1
    elif "Bring" in task["task"]:
        if "Open" in task['plan'][-2]:
            task_info["bring_docker"] += 1
        else:
            task_info["bring"] += 1
    elif "Put" in task["task"]:
        if any(["Open" in plan for plan in task['plan']]):
            task_info["put_docker"] += 1
        else:
            task_info["put"] += 1
    return task_info


mode = "gen"  #test,gen
# env = Environment(env_path='auto')  # significantly increase the sampling rate without using animations
# scene = load_json(pkg_resources.resource_filename('legent', 'scenes/scene-default.json'))
# with open("json/scene.json",'w') as file:
#     json.dump(scene,file)
with open("json/scene.json", 'r') as file:
    scene = json.load(file)

if mode == "gen":
    if os.path.exists("task_info.json"):
        with open("task_info.json", 'r') as file:
            task_info = json.load(file)
    else:
        task_info = {
            "come": 0,
            "goto": 0,
            "goto_docker": 0,
            "take": 0,
            "take_docker": 0,
            "bring": 0,
            "bring_docker": 0,
            "put": 0,
            "put_docker": 0,
            "where": 0,
            "where_docker": 0
        }
try:
    saver = TrajectorySaver()
    # tasks = TaskCreator().test_object(scene, type="exist")
    tasks = TaskCreator().create_tasks(task_types=['put'], method="hardcoding", scene_num=5,scene=scene)  # or load from task files
    print("生成任务完毕 ")
    # env.reset(ResetInfo(scene=scene))
    for index,task in enumerate(tasks):
        if index % 100 == 0:
            env = Environment(env_path='auto')
        env.reset(ResetInfo(scene=scene))
        actions = None
        solu_index = 0
        fail_traj = None
        task_solu_input = task['solution']
        for i in range(8):
            try:
                if fail_traj is not None:
                    task_solu_input = task_solu_input[solu_index:]
                    controller = Controller(env, task_solu_input, fail_traj)
                else:
                    controller = Controller(env, task_solu_input)
                traj = controller.collect_trajectory(task,max_step=200)
                if traj:
                    # The task has been completed successfully
                    if mode == "gen":
                        saver.save_traj(traj=traj)
                        task_info = save_task_info(task, task_info)
                    print(f'Complete task "{task["task"]}" in {traj.steps} steps.', task['solution'], "***{}***".format(index))
                    break
                else:
                    env.reset(ResetInfo(scene=scene))
                    # print(task['task'], task['solution'], end='')
                    # print(f'Complete task "{task["task"]}" failed. Deserted.')
                    if i >= 7:
                        print(f'Complete task "{task["task"]}" failed. Deserted.',task['task'], task['solution'], "***{}***".format(index))
                        break

            except TypeError as e:
                actions = controller.actions
                solu_index = controller.solu_traj[0]
                fail_traj = controller.traj
                # print(task['task'], task['solution'], end='')
                # print(e)
                if i >= 7:
                    print(task['task'], task['solution'],e,"***{}***".format(index))
                    break
        if index % 100 == 99:
            env.close()
    if mode == "gen":
        saver.save()
        with open("task_info.json", 'w') as file:
            json.dump(task_info, file)
finally:
    if env is not None:
        env.close()
