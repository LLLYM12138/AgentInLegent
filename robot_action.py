# coding=utf-8
import random
import re

import json
from legent import Environment, Action, Observation, ResetInfo, Controller, TaskCreator, TrajectorySaver, save_image
from legent.utils.math import is_point_on_box
import legent.server.scene_generator as scene_generator
import numpy as np
from build_data.gen_data import test_object, create_text_task
import os
import os.path as path

with open("json/name_id.json", 'r') as file:
    name_id = json.load(file)
with open("json/interactable.json", 'r') as file:
    interactable = json.load(file)
on = interactable["on"]
room_id = {
    "First Floor Living Room and Kitchen": 200,
    "First Floor Bathroom1": 22,
    "First Floor Cloakroom1": 241,
    "First Floor Bedroom1": 48,
    "First Floor Cloakroom2": 415,
    "First Floor Bathroom2": 212,
    "Second Floor Corridor": 268,
    "Second Floor Cloakroom1": 259,
    "Second Floor Bedroom1": 382,
    "Second Floor Bathroom1": 305,
    "Second Floor Cloakroom2": 346,
    "Second Floor Bedroom2": 358,
    "Second Floor Bathroom2": 275,
    "user": "",
    "first floor living room and kitchen": 200,
    "first floor bathroom1": 22,
    "first floor cloakroom1": 241,
    "first floor bedroom1": 48,
    "first floor cloakroom2": 415,
    "first floor bathroom2": 212,
    "second floor corridor": 268,
    "second floor cloakroom1": 259,
    "second floor bedroom1": 382,
    "second floor bathroom1": 305,
    "second floor cloakroom2": 346,
    "second floor bedroom2": 358,
    "second floor bathroom2": 275,
}
stair = {"Go upstair.": 268,
         "Go downstair.": 51,
         "go upstair.": 268,
         "go downstair.": 51,
         }
plan_action = {
    "Go": "goto",
    "Open": "interact",
    "Pick up": "grab",
    "Grab": "grab",
    "Release": "release",
    "Reply": "speak",
    "Give": "interact",
    "LookDown": "lookDown",
    "go": "goto",
    "open": "interact",
    "pick up": "grab",
    "grab": "grab",
    "release": "release",
    "reply": "speak",
    "give": "interact",
    "lookdown": "lookdown"
}
robot_init_pos = {
    "First Floor Living Room and Kitchen": [-2.084861993789673, 0.1319998800754547, 0.86406409740448],
    "First Floor Bathroom1": [-3.404572010040283, 0.1319996416568756, 4.572017669677734],
    "First Floor Cloakroom1": [2.634119987487793, 0.13199952244758606, 4.494143962860107],
    "First Floor Bedroom1": [2.3977620601654053, 0.13199999928474426, -2.417731523513794],
    "First Floor Cloakroom2": [2.735677719116211, 0.1319998800754547, 0.5322930812835693],
    "First Floor Bathroom2": [5.005429267883301, 0.1319996416568756, 4.487617015838623],
    "Second Floor Corridor": [-3.7597429752349854, 3.131999969482422, -1.516936182975769],
    "Second Floor Bedroom1": [0.8792527318000793, 3.1319994926452637, 3.5652897357940674],
    "Second Floor Bathroom1": [5.130310535430908, 3.1319994926452637, -1.1944429874420166],
    "Second Floor Cloakroom1": [-5.040546894073486, 3.131999969482422, 2.9457812309265137],
    "Second Floor Bedroom2": [0.14077933132648468, 3.131999969482422, -1.7900400161743164],
    "Second Floor Bathroom2": [-5.042611122131348, 3.1319994926452637, -3.5251009464263916],
    "Second Floor Cloakroom2": [-2.92553973197937, 3.1319994926452637, -3.886068820953369]
}

human_init_pos = {
    "First Floor Living Room and Kitchen": [-2.284861993789673, 0.1319998800754547, 0.96406409740448],
    "First Floor Bathroom1": [-3.604572010040283, 0.1319996416568756, 4.772017669677734],
    "First Floor Cloakroom1": [2.434119987487793, 0.13199952244758606, 4.694143962860107],
    "First Floor Bedroom1": [2.6977620601654053, 0.13199999928474426, -2.217731523513794],
    "First Floor Cloakroom2": [2.935677719116211, 0.1319998800754547, 0.7322930812835693],
    "First Floor Bathroom2": [5.205429267883301, 0.1319996416568756, 4.687617015838623],
    "Second Floor Corridor": [-3.9597429752349854, 3.131999969482422, -1.716936182975769],
    "Second Floor Bedroom1": [1.0792527318000793, 3.1319994926452637, 3.7652897357940674],
    "Second Floor Bathroom1": [5.330310535430908, 3.1319994926452637, -1.3944429874420166],
    "Second Floor Cloakroom1": [-5.340546894073486, 3.131999969482422, 2.7457812309265137],
    "Second Floor Bedroom2": [0.34077933132648468, 3.131999969482422, -1.5900400161743164],
    "Second Floor Bathroom2": [-5.342611122131348, 3.1319994926452637, -3.7251009464263916],
    "Second Floor Cloakroom2": [-2.72553973197937, 3.1319994926452637, -3.686068820953369]
}


# def gen_solution(input, task_type):
#     solution = []
#     room = input["robot_room"]
#     change_id = -1
#     change_name = ""
#     for i, sub_plan in enumerate(input["plan"]):
#         if "check" in sub_plan:
#             continue
#         if "go to the " in sub_plan:
#             name = sub_plan[10:-1]
#             if name in room_id.keys():
#                 object_id = room_id[name]
#                 room = name
#             else:
#                 object_id = random.choice(name_id[room.lower() + name])
#         elif sub_plan in stair.keys():
#             object_id = stair[sub_plan]
#         elif "reply" in sub_plan:
#             object_id = sub_plan[18:-1]
#         elif "grab" in sub_plan or "pick up" in sub_plan:
#             change_id = object_id
#             change_name = name
#         elif "release" in sub_plan:
#             if room + change_name not in name_id:
#                 name_id[room + change_name] = [change_id]
#             else:
#                 name_id[room + change_name].append(change_id)
#         else:
#             object_id = ""
#         for key in plan_action.keys():
#             if key in sub_plan:
#                 action = plan_action[key]
#                 break
#
#         if task_type == "put" or "Put" in input["task"]:
#             if i < len(input["plan"]) - 1 and action == "release":
#                 solution.extend(["lookDown()", f"{action}({object_id})"])
#             else:
#                 solution.extend([f"{action}({object_id})"])
#         elif task_type == "bring" or "Bring" in input["task"]:
#             if sub_plan == "go to the user.":
#                 solution.extend(["goto_user()"])
#             else:
#                 solution.extend([f"{action}({object_id})"])
#         elif task_type == "test":
#             if sub_plan == "go to the user.":
#                 solution.extend(["goto_user()"])
#             else:
#                 solution.extend([f"{action}({object_id})"])
#         else:  #task_type in ["exist_no", "take", "goto", "exist_yes"]
#             solution.extend([f"{action}({object_id})"])
#     return solution


# def bring_success(obs, task, solution):
#     name = task[10:-7]
#     id = obs.game_states["agent_grab_instance"]
#     player_pos = obs.game_states['player']['position']
#     robot_pos = obs.game_states['agent']['position']
#     if obs.game_states['instances'][id]['prefab'].split("LowPolyInterior2_")[1] == name:
#         return True
#     else:
#         return False
#
#
# def exist_success(obs, task, solution):
#     ret = re.match("Is there a (.*) [i,o]n the (.*)\?", task)
#     object_name = ret.group(1)
#     on_name = ret.group(2)
#     for solu in reversed(solution):
#         if "goto" in solu:
#             break
#     ret = re.match("goto\((.*)\)", solu)
#     on_id = ret.group(1)
#     ret = re.match("speak\((.*)\)", solution[-1])
#     replay = ret.group(1)
#     if replay == "No":
#         answer = False
#     elif replay == "Yes":
#         answer = True
#     else:
#         raise Exception('replay parse error')
#     truth = False
#     for id in on[str(on_id)]:
#         if obs.game_states['instances'][id]['prefab'].split("LowPolyInterior2_")[1] == object_name:
#             truth = True
#             break
#     if truth == answer:
#         return True
#     else:
#         return False
#
# def put_success(obs, task, solution):
#     ret = re.match("Is there a (.*) [i,o]n the (.*)\?", task)
#     object_name = ret.group(1)
#     on_name = ret.group(2)
#     for solu in reversed(solution):
#         if "goto" in solu:
#             break
#     ret = re.match("goto\((.*)\)", solu)
#     on_id = ret.group(1)
#     ret = re.match("speak\((.*)\)", solution[-1])
#     replay = ret.group(1)
#     if replay == "No":
#         answer = False
#     elif replay == "Yes":
#         answer = True
#     else:
#         raise Exception('replay parse error')
#     truth = False
#     for id in on[str(on_id)]:
#         if obs.game_states['instances'][id]['prefab'].split("LowPolyInterior2_")[1] == object_name:
#             truth = True
#             break
#     if truth == answer:
#         return True
#     else:
#         return False
#
#
# success_func = {
#     "bring": bring_success,
#     "exist": exist_success
# }


# def env_complete(inputs, task_type):
#     with open("json/scene.json", 'r') as file:
#         scene = json.load(file)
#
#     success = 0
#     env_error = 0
#     plan_error = 0
#     unknown_error = 0
#     unknown = []
#     env = Environment(env_path='auto')
#     obs = env.reset(ResetInfo(scene=scene))
#     for task_num, input in enumerate(inputs):
#
#         if task_num % 100 == 99:
#             env.close()
#             env = Environment(env_path='auto')
#             obs = env.reset(ResetInfo(scene=scene))
#         solution = gen_solution(input, task_type)
#         task_solu_input = solution
#         plan = input["plan"]
#         sample = {"task": input["task"], "plan": input["plan"], "solution": solution, "scene": scene}
#         scene["agent"]["position"] = robot_init_pos[input["robot_room"]]
#         obs = env.reset(ResetInfo(scene=scene))
#
#         solu_index = 0
#         fail_traj = None
#         env_error_flag = False
#         for i in range(8):
#             try:
#                 if fail_traj is not None:
#                     task_solu_input = task_solu_input[solu_index:]
#                     plan = plan[solu_index:]
#                     controller = Controller(env, task_solu_input, fail_traj, plan)
#                 else:
#                     controller = Controller(env, task_solu_input, plan=plan)
#                 traj = controller.collect_trajectory(sample, max_step=100)
#                 if traj:
#                     print("success:", input["task"], solution)
#                     break
#                 else:
#                     env.reset(ResetInfo(scene=scene))
#                     if i >= 7:
#                         print("fail:", input["task"], solution)
#                         env_error_flag = True
#                         break
#
#             except TypeError as e:
#                 actions = controller.actions
#                 solu_index = controller.solu_traj[0]
#                 fail_traj = controller.traj
#                 if i >= 7:
#                     print(solution, e, solution)
#                     env_error_flag = True
#                     break
#     #     if env_error_flag:
#     #         env_error += 1
#     #     else:
#     #         action = Action()
#     #         obs = env.step(action)
#     #         flag = success_func[task_type](obs, sample["task"], solution)
#     #         if flag:
#     #             success += 1
#     #         elif not flag:
#     #             plan_error += 0
#     #         else:
#     #             unknown_error += 1
#     #             unknown.append(input)
#     # with open("test/" + task_type + ".txt", "w") as f:
#     #     f.write(f"success:{success}\nenv_error:{env_error}\nplan_error:{plan_error}\nunknown_error:{unknown_error}\n")
#     #     for error in unknown:
#     #         f.write(str(error))
#     env.close()

class Env:
    def __init__(self):
        with open("json/scene.json", 'r',encoding="gbk") as file:
            self.scene = json.load(file)
        self.env = Environment(env_path=None)
        obs = self.env.reset(ResetInfo(scene=self.scene))
        self.history = []

    def reset(self, robot_room, human_room):
        """

        :param robot_room: 初始时刻机器人的房间
        :param human_room: 初始时刻用户房间
        :return:
        """
        with open("json/scene.json", 'r') as file:
            self.scene = json.load(file)
        self.scene["agent"]["position"] = robot_init_pos[robot_room]
        if human_room is not None:
            self.scene["player"]["position"] = human_init_pos[human_room]
        obs = self.env.reset(ResetInfo(scene=self.scene))
        self.history = []
        return obs.image

    # "go": "goto",
    # "open": "interact",
    # "pick up": "grab",
    # "grab": "grab",
    # "release": "release",
    # "reply": "speak",
    # "give": "interact",
    # "lookdown": "lookdown"
    def gen_solution(self, actions):
        solution = []
        room = actions["robot_room"]
        change_id = -1
        change_name = ""
        try:
            for i, sub_plan in enumerate(actions["plan"]):
                if "check" in sub_plan.lower():
                    continue
                if "go to the " in sub_plan.lower():
                    name = sub_plan[10:-1]
                    if name in room_id.keys():
                        object_id = room_id[name]
                        room = name
                    else:
                        object_id = random.choice(name_id[room.lower() + name])
                elif sub_plan.lower() in stair.keys():
                    object_id = stair[sub_plan]
                elif "reply" in sub_plan.lower():
                    object_id = sub_plan[18:-1]
                elif "grab" in sub_plan or "pick up" in sub_plan.lower():
                    change_id = object_id
                    change_name = name
                elif "release" in sub_plan.lower():
                    if room + change_name not in name_id:
                        name_id[room + change_name] = [change_id]
                    else:
                        name_id[room + change_name].append(change_id)
                elif "finish" in sub_plan.lower():
                    return []
                else:
                    object_id = ""
                object_id = str(object_id)

                action = None
                for key in plan_action.keys():
                    if key in sub_plan:
                        action = plan_action[key]
                        break
                if action is None:
                    raise ValueError("格式错误")

                if "put" in actions["task"].lower():
                    if action == "release":
                        solution.extend(["lookDown()", f"{action}({object_id})"])
                    else:
                        solution.extend([f"{action}({object_id})"])
                elif "bring" in actions["task"].lower():
                    if sub_plan == "go to the user.":
                        solution.extend(["goto_user()"])
                    else:
                        solution.extend([f"{action}({object_id})"])
                else:  # task_type in ["exist_no", "take", "govto", "exist_yes"]
                    solution.extend([f"{action}({object_id})"])
                if not object_id.isdigit() and object_id not in ["", "yes", "no", "Yes", "No"]:
                    raise ValueError("格式错误")
        except (KeyError, TypeError, ValueError, NameError) as e:
            print("*" * 50)
            print("生成命令错误：", e)
            print("原始命令为：", actions["plan"])
            print("*" * 50)
            return None
        return solution

    def step(self, action):
        """

        :param action: 输入格式: {"task":任务名称, "robot_room":机器人初始位置, "plan":命令}
        :return: None:命令错误；-1:环境中命令执行失败；图片:命令执行成功,numpy.ndarray格式
        """
        solu = self.gen_solution(action)
        # print(solu)
        solution = solu[len(self.history):]
        self.history = solu

        if solu is None:
            return None
        if len(solu) == 0:
            obs = self.env.step(Action())
            return obs.image
        task_solu_input = solution
        plan = action["plan"]
        sample = {"task": action["task"], "plan": action["plan"], "solution": solution, "scene": self.scene}

        solu_index = 0
        fail_traj = None
        for i in range(8):
            try:
                if fail_traj is not None:
                    task_solu_input = task_solu_input[solu_index:]
                    plan = plan[solu_index:]
                    controller = Controller(self.env, task_solu_input, fail_traj, plan)
                else:
                    # print("task_solu_input:", task_solu_input)
                    # print("plan:", plan)
                    controller = Controller(self.env, task_solu_input, plan=plan)
                traj = controller.collect_trajectory(sample, max_step=100)
                if traj:
                    print("success:", action["task"], solution)
                    break
                else:
                    self.env.reset(ResetInfo(scene=self.scene))
                    if i >= 7:
                        print("fail:", action["task"], solution)
                        break

            except TypeError as e:
                actions = controller.actions
                solu_index = controller.solu_traj[0]
                fail_traj = controller.traj
                if i >= 7:
                    print("*" * 50)
                    print("命令执行失败:", action["task"], solution)
                    print("错误为:", e)
                    print("*" * 50)
                    break
        obs = self.env.step(Action())
        return obs.image

    def close(self):
        self.env.close()


if __name__ == "__main__":
    #使用样例
    data = {
        "caption": "go to the second floor bedroom1.\ngo to the wineglass1_c2.\ngrab the wineglass1_c2.\ngo downstair.\ngo to the first floor bathroom2.\ngo to the user.\ngive the wineglass1_c2 to the user.",
        "image_id": 0,
        "task_id": "bring_test_0",
        "task": "Bring the Wineglass1_C2 to me.",
        "robot_room": "Second Floor Bathroom1",
        "human_room": "First Floor Bathroom2",
        "plan": [
            "go to the second floor bedroom1.",
            "go to the wineglass1_c2.",
            "grab the wineglass1_c2.",
            "go downstair.",
            "go to the first floor bathroom2.",
            "go to the user.",
            "give the wineglass1_c2 to the user."
        ]
    }
    env = Env()
    env.reset(data["robot_room"], data["human_room"])  #不是bring任务human_room填None

    #每次要把全部历史动作输入进去,便于生成命令，但环境不会重头模拟
    for index, j in enumerate(data["plan"]):
        use_input = data.copy()
        use_input["plan"] = data["plan"][:index + 1]
        ans = env.step(use_input)

    ################################################################################################################################
    # with open("json/scene.json", 'r') as file:
    #     scene = json.load(file)
    # # 测试样例
    # # with open("test/exist.json", 'r') as file:
    # #     exist = json.load(file)
    # #
    # # jsons = os.listdir("result/original")
    # # for json_name in jsons:
    # with open("演示任务.json", 'r') as file:
    #     data = json.load(file)
    # # for i,input in enumerate(data):
    # #     try:
    # #         solution = gen_solution(input, "put")
    # #         # print(i)
    # #     except Exception as e:
    # #         print(input["plan"],input["task"])
    # #         print(e)
    #
    # # with open("result/original/where.json", 'r') as file:
    # #     data = json.load(file)
    # # inputs = random.choices(data,k=5)
    # data = random.choices(data,k=5)
    # env = Env()
    # for i, input in enumerate(data):
    #     print(i)
    #     env.reset(input["robot_room"],None)
    #     for index,j in enumerate(input["plan"]):
    #         use_input = input.copy()
    #         use_input["plan"] = input["plan"][:index+1]
    #         ans = env.step(use_input)
    #         print(type(ans))
    # env_complete(data, "put")
    ############################################################################
    # #生成测试集
    # with open("test/test_no_KG.json", 'r') as file:
    #     tests = json.load(file)
    # # with open("test/test_no_KG_epochbest_rank0.json", 'r') as file:
    # #     tests = json.load(file)
    # inputs = []
    # for data in tests:
    #     room = data["scene"].split("_")[0]
    #     task = data["task_name"]
    #     plan = data["text_output"].split("\n")
    #     inputs.append({
    #         "task": task,
    #         "robot_room": room,
    #         "plan": plan,
    #     })
    # # # for i, input in enumerate(inputs):
    # # #     try:
    # # #         solution = gen_solution(input, "put")
    # # #         print(i)
    # # #     except KeyError as e:
    # # #         print(input["plan"], input["task"])
    # # #         print(e)
    # put = []
    # bring = []
    # take = []
    # exist = []
    # goto = []
    # where = []
    # for i,input in enumerate(inputs):
    #     print(i)
    #     if "put" in input["task_id"]:
    #         put.append(input)
    #     elif "bring" in input["task_id"]:
    #         bring.append(input)
    #     elif "take" in input["task_id"]:
    #         take.append(input)
    #     elif "exist" in input["task_id"]:
    #         exist.append(input)
    #     elif "go" in input["task_id"]:
    #         goto.append(input)
    #     elif "where" in input["task_id"]:
    #         where.append(input)
    #     else:
    #         print(input)
    #         # raise()
    #     with open("test/task/put.json", 'w') as file:
    #         json.dump(put, file)
    #     with open("test/task/bring.json", 'w') as file:
    #         json.dump(bring, file)
    #     with open("test/task/take.json", 'w') as file:
    #         json.dump(take, file)
    #     with open("test/task/exist.json", 'w') as file:
    #         json.dump(exist, file)
    #     with open("test/task/goto.json", 'w') as file:
    #         json.dump(goto, file)
    #     with open("test/task/where.json", 'w') as file:
    #         json.dump(where, file)
    ############################################################################
    # 在环境中测试
    # env = Environment(env_path='auto')
    # for i in range(417):
    #     env.reset(ResetInfo(scene=scene))
    #     task = TaskCreator().test_object(scene, i)[0]
    #     for j in range(8):
    #         try:
    #             controller = Controller(env, task['solution'])
    #             traj = controller.collect_trajectory(task)
    #             if traj:
    #                 print(f'goto {i} success')
    #                 success.append(i)
    #                 break
    #             else:
    #                 env.reset(ResetInfo(scene=scene))
    #                 if j >= 7:
    #                     print(f'goto {i} failed')
    #                     fail.append(i)
    #                     break
    #         except TypeError as e:
    #             if j >= 7:
    #                 print(f'goto {i} failed', end='')
    #                 print(e)
    #                 fail.append(i)
    #                 break
    # with open("goto.json", 'w') as file:
    #     json.dump(success, file)
    # with open("cannot_goto.json", 'w') as file:
    #     json.dump(fail, file)
