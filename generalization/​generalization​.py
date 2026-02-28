import json
import os
# D:\legent\LEGENT\.legent\env\env_data\env_data-20240511-171612-720601\procthor\asset_groups\television-sofa.json,33:"LowPolyInterior2_TVTable2_C1",
from legent import Environment, ResetInfo, generate_scene,Action

# scene = generate_scene(room_num=4)
# # print(scene)
# # 确保目录存在
# os.makedirs("generalization", exist_ok=True)
# with open(f"generalization/generalization_scene.json", 'w') as file:
#     json.dump(scene, file)
# env = Environment(env_path="auto")
# try:
#     env.reset(ResetInfo(scene))
#     while True:
#         action = Action()
#         obs = env.step(action)
# finally:
#     env.close()


with open("generalization/generalization_scene.json","r"):
    