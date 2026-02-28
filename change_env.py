# coding=utf-8
import json
from legent import Environment, Action, Observation, ResetInfo, Controller, TaskCreator, TrajectorySaver, save_image
from legent.utils.math import is_point_on_box
import legent.server.scene_generator as scene_generator
import numpy as np

env = Environment(env_path='auto')
with open("json/scene.json", 'r') as file:
    scene = json.load(file)
target_i = 0
pos = 0

try:
    obs: Observation = env.reset(ResetInfo(scene))
    while True:
        action = Action()
        if "saveimage" in obs.text:
            save_image(obs.image, "D:\\LYM python homework\\legent\\KG\\" + obs.text[-2:] + ".png")
            print(obs.game_states['player_camera'])
        if "down" in obs.text:
            angel = int(obs.text[4:])
            action = Action(rotate_down=angel)
        if obs.text == "pos":
            action = Action(text=str(obs.game_states['player']['position']) + str(obs.game_states['player']['forward']))
            print(obs.game_states['player']['position'], obs.game_states['player']['forward'])
        if obs.text == "object":
            name = obs.game_states['instances'][target_i]
            print(target_i, name)
            action = Action(text=name['prefab'])
            pos = obs.game_states['instances'][target_i]['position']
        if obs.text == "save":
            with open("json/scene.json", 'r') as file:
                scene = json.load(file)
            name = obs.game_states['instances'][target_i]
            print(target_i, name)
            action = Action(text=name['prefab'])
            pos = obs.game_states['instances'][target_i]['position']
            rot = obs.game_states['instances'][target_i]['rotation']
            scene["instances"][target_i]["position"] = [pos["x"], pos["y"], pos["z"]]
            scene["instances"][target_i]["rotation"] = [rot["x"], rot["y"], rot["z"]]
            with open("json/scene.json", 'w') as file:
                json.dump(scene, file)
        if obs.text == "setpos":
            name = obs.game_states['instances'][target_i]
            print(target_i, name)
            action = Action(text=name['prefab'])
            pos = obs.game_states['instances'][target_i]['position']
            print(pos)
            rot = obs.game_states['instances'][target_i]['rotation']
        if obs.text == "physci":
            with open("json/scene.json", 'r') as file:
                scene = json.load(file)
            if scene["instances"][target_i]["type"] == "kinematic":
                scene["instances"][target_i]["type"] = "interactable"
                print("interactable")
            elif scene["instances"][target_i]["type"] == "interactable":
                scene["instances"][target_i]["type"] = "kinematic"
            with open("json/scene.json", 'w') as file:
                json.dump(scene, file)
        if obs.text == "set":
            # target_i = int(obs.text.split("_")[1])
            target_i = obs.game_states["player_grab_instance"]
            action = Action(text="now target index:{}".format(target_i))
        if obs.text == "reset":
            with open("json/scene.json", 'r') as file:
                scene = json.load(file)
            obs: Observation = env.reset(ResetInfo(scene))
        if "goto" in obs.text:
            mode = "gen"  # test,gen
            saver = TrajectorySaver()
            i = int(obs.text[4:])
            task = TaskCreator().test_object(scene, i)[0]
            for i in range(8):
                try:
                    controller = Controller(env, task['solution'])
                    traj = controller.collect_trajectory(task)
                    if traj:
                        # The task has been completed successfully
                        if mode == "gen":
                            saver.save_traj(traj=traj)
                        print(f'Complete task "{task["task"]}" in {traj.steps} steps.', task['solution'])
                        break
                    else:
                        env.reset(ResetInfo(scene=scene))
                        if i >= 7:
                            print(task['task'], task['solution'], end='')
                            print(f'Complete task "{task["task"]}" failed. Deserted.')
                            break

                except TypeError as e:
                    if i >= 7:
                        print(task['task'], task['solution'], end='')
                        print(e)
                        break
        if obs.text == "grab":
            action = Action(grab=True)
        if "on" in obs.text:
            i = int(obs.text[2:])
            on_id, on_name = TaskCreator().test_object(scene, id=i, type="on")
            print(on_id, on_name)
        obs = env.step(action)
finally:
    env.close()
