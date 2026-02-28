# coding=utf-8
# 根据环境数据集生成双语任务
import os
import os.path as path
import json
import shutil
import re
import random

with open("json/interactable.json", 'r') as file:
    save_dict = json.load(file)
docker = save_dict["docker"]
translate_plan = {
    "Go upstair.": "上楼", "Go to": "前往", "Open": "打开", "pick up": "拿起", "Pick up": "拿起", "Release": "放下",
    "It's not on": "这个物体不在", "It's on": "这个物体在", "Yes.": "有", "No.": "没有", "No": "没有",
    "Task done.": "任务结束", "Go downstair.": "下楼", "user": "用户", 'Grab': "拿起", "Look down.": "看向地板",
    "Reply to": "回复", "Sink2": "水槽2",

    'Carpet': "地毯", 'Carpet1': "地毯1", 'Carpet2': "地毯2", 'Carpet3': "地毯3", 'Carpet4': "地毯4",
    'Carpet5': "地毯5", "Floor": "地板", "Shoe": "鞋",
    'Clothes2': "衣服2", 'Clothes3': "衣服3", 'Clothes4': "衣服4", 'Clothes5': "衣服5", 'Clothes6': "衣服6",
    'Clothes7': "衣服7", 'Clothes9': "衣服9", 'Clothes10': "衣服10", 'Wardrobe12': "衣服12",
    'Wardrobe5': "衣柜5", 'Wardrobe6': "衣柜6", 'Wardrobe8': "衣柜8", 'Wardrobe9': "衣柜9",
    'Plant': "植物", 'Plate1': "植物1", 'Plate2': "植物2", 'Plate3': "植物3", 'Plate5': "植物5", 'Plate6': "植物6",
    'Curtains1': "窗帘1", 'Curtains3': "窗帘3", 'Curtains10': "窗帘10", 'Curtains13': "窗帘13",
    'Switch1': "开关1", 'Switch2': "开关2", 'Plumbing1': "水龙头1", 'Plumbing2': "水龙头2",
    'BedTable2': "床头柜2", 'BedTable3': "床头柜3", 'Dresser1': "梳妆台1", 'Dresser3': "梳妆台3",
    'Bed3': "床3", 'Bed5': "床5", 'Cup1': "杯子1", 'Cup2': "杯子2",
    'Clock1': "闹钟1", 'Clock2': "闹钟2", 'Socket4': "插座4", 'Socket5': "插座5",
    'Toothpaste': "牙膏", 'ToothbrushCup': "牙刷杯", 'Toothbrush': "牙刷",
    'BathroomProps': "卫生间里的化妆品瓶子", 'Bathroom': "卫生间", 'ToiletPaper': "卫生纸",
    'Mirror': "镜子", 'Towel': "毛巾", 'TowelRail': "毛巾架", 'Ventilation': "通风口",
    'Bin': "垃圾桶", 'Washer': "洗衣机", 'Painting': "画", 'Light': "灯",
    'AirConditioner': "空调", 'Box': "盒子", 'Book': "书", 'TV': "电视",
    'Toilet1': "厕所1", 'Shower1': "淋浴器1", 'Bench2': "板凳", 'Kitchen1': "厨房",
    'Table': "桌子", 'Chair': "椅子“", 'Wineglass1': "酒杯1", 'Wine': "红酒",
    'Reward': "奖杯", 'Car': "玩具车", 'Cupcake': "蛋糕", 'Soda': "苏打水",
    'Burger': "汉堡", 'Vase': "花瓶", 'Pumpkin': "南瓜", 'Pie': "馅饼",
    'Pineapple': "菠萝", 'Chicken': "烤鸡", 'Butter': "黄油", 'Pepper': "胡椒",
    'Cake': "蛋糕", 'Teapot': "茶壶", 'Toaster': "烤面包机", 'Knife': "刀",
    'Spoon': "勺子", 'Paper': "纸张", 'Salt': "盐", 'Pan': "平底锅", "Papper": "白胡椒粉",
    'PanPart': "平底锅", 'KitchenProps': "厨房里的调料瓶", 'Kettle1': "水壶",
    'Hanger': "衣架", 'CuttingBoard': "砧板", 'CoffeeMachine': "咖啡机", 'Cezve': "咖啡机",
    'Microwave': "微波", 'Hood1': "头罩1", 'Hob1': "炉盘", 'Drainer': "排水器",
    'Dishwasher': "洗碗机", 'Refrigerator3': "冰箱", 'Sofa8': "沙发8",
    'SmallTable': "小桌子", 'Shelf': "架子", 'Globe': "球",
    'PC': "个人电脑", 'Dumbbell': "哑铃", 'OfficeProps': "文具",
    'Frame': "架子", 'Pendulum': "钟摆", 'Fireplace': "壁炉", 'Sushi': "寿司",
    'Laptop': "笔记本电脑", 'Soy': "豆子", 'Wok': "锅", 'Champagne': "香槟酒", 'Sofa1': "沙发1", 'Wall1': "墙",

    "Bathroom_Washbasin_drawers_07": "卫生间洗手盆抽屉7",
    "Bathroom_Washbasin_drawers_5_Right": "卫生间洗手盆抽屉5",
    "Bathroom_Washbasin_drawers_9": "卫生间洗手盆抽屉9",
    "Bathroom_Washbasin_drawers_5_Left": "卫生间洗手盆抽屉5",
    "Bathroom_Washbasin_drawers_5_R": "卫生间洗手盆抽屉5",
    "Bathroom_C3_07": "卫生间",
    "Bathroom_C3_05R": "卫生间",
    "Kitchen_Cupboard_1": "厨房橱柜1",
    "Kitchen_Cupboard_1_Right": "厨房右侧橱柜1",
    "Kitchen_Cupboard_3": "厨房橱柜3",
    "Kitchen_Cupboard_1_Left": "厨房左侧橱柜1",
    'Kitchen1_C1_01R': "厨房橱柜",
    "Refrigerator_3": "冰箱3",
    "Wardrobe_1": "衣柜1",
    "Wardrobe_9": "衣柜9",
    "Wardrobe_8": "衣柜8",
    "Wardrobe_6": "衣柜6",
    "Dresser_1": "梳妆台1",
    "TV_Table_2": "电视柜"
}

start = [
    "Grab",
    "Release",
    "Speak",
    "Interact",
    "LookDown"]


def get_index(image_actions, type):
    image_index = []
    docker = False
    for i, action in enumerate(image_actions):
        if "0000.png" in action["image"]:
            image_index.append(action["image"])
        if action["actions"] in start or action["action"] == "finish()":
            image_index.append(action["image"])
        if type in ["where", "bring", "put"]:
            if action["action"] != "finish()":
                if (action["actions"] in ["Speak", "Grab", "Release"] and image_actions[i + 1]["action"] != "finish()" and image_actions[i + 1]["actions"] != "Grab") or \
                        (image_actions[i + 1]["actions"] == "LookStraightAhead" and action["actions"] != "LookStraightAhead"):
                    image_index.append(image_actions[i + 1]["image"])
        else:
            if action["actions"] == "LookStraightAhead":
                image_index.append(action["image"])
    return docker, image_index


def process_plan(plan, type, solution):
    plan_cn = []
    # if type == "goto":
    # for i, step in enumerate(plan):
    #     if "Open" in step:
    #         Open = step.split(" and ")[0] + "."
    #         Pick = step.split(" and ")[1]
    #         plan.pop(i)
    #         plan.insert(i, Open)
    #         plan.insert(i + 1, Pick)
    for i, step in enumerate(plan):
        # if "Open" in step:
        #     step = step + "."
        if "House4" in step:
            step = step.replace("House4", "Floor")
        # print(plan,solution)
        if "Reply" in step:
            if type == "where":
                action = step.split(" the ")[0]
                object = step.split(" the ")[1][:-1]
                sentence = solution[i].split("\"")[1]
                sentence_action = sentence.split(" the ")[0]
                sentence_object = sentence.split(" the ")[1][:-1]
                plan_cn.append(translate_plan[action] + translate_plan[object] + ":" + translate_plan[sentence_action] +
                               translate_plan[sentence_object] + "上")
                plan[i] = step[:-1] + ":" + sentence
            elif type == "exist":
                action = step.split(" the ")[0]
                object = step.split(" the ")[1][:-1]
                sentence = solution[i].split("\"")[1]
                plan_cn.append(translate_plan[action] + translate_plan[object] + ":" + translate_plan[sentence])
                plan[i] = step[:-1] + ":" + sentence
        elif "the" in step:
            if step[-1] == ".":
                action = step.split(" the ")[0]
                object = step.split(" the ")[1][:-1]
            else:
                action = step.split(" the ")[0]
                object = step.split(" the ")[1]
            plan_cn.append(translate_plan[action] + translate_plan[object])
        else:
            plan_cn.append(translate_plan[step])
    # print(plan, plan_cn)
    return plan, plan_cn


def process_task(task, type):
    task_cn = ""
    if type == "goto":
        object = task.split(" the ")[1][:-1]
        task_cn = "前往" + translate_plan[object] + "."
    if type == "bring":
        object = task.split(" the ")[1][:-1]
        part1 = ["把", "将"]
        part2 = ["拿给我", "带给我", "交给我"]
        task_cn = random.choice(part1) + translate_plan[object] + random.choice(part2) + "."
    if type == "where":
        object = task.split(" the ")[1][:-1]
        part1 = ["在哪里?", "在什么地方?"]
        part2 = "找到"
        task_cn_1 = translate_plan[object] + random.choice(part1)
        task_cn_2 = part2 + translate_plan[object] + "."
        task_cn = random.choice([task_cn_1, task_cn_2])
    if type == "exist":
        if "House4" in task:
            task = task.replace("House4", "Floor")
        if "Clothes9" in task:
            task = task.replace("Clothes9", "Shoe")
        if "Clothes10" in task:
            task = task.replace("Clothes10", "Shoe")
        object = task[11:-1].split(" ")[0]
        target = task[11:-1].split(" ")[-1]
        if "on" in task:
            task_cn = translate_plan[target] + "上有" + translate_plan[object] + "吗?"
        elif "in" in task:
            task_cn = translate_plan[target] + "里有" + translate_plan[object] + "吗?"
    if type == "put":
        if "House4" in task:
            task = task.replace("House4", "Floor")
        if "Clothes9" in task:
            task = task.replace("Clothes9", "Shoe")
        if "Clothes10" in task:
            task = task.replace("Clothes10", "Shoe")
        object = task.split(" ")[2]
        target = task.split(" ")[5][:-1]
        docker_name = [i["name"] for i in docker.values()]
        if target == "Bathroom" or target == "Kitchen1" or target in docker_name:
            task = task.replace("on", "in")
        if "on" in task:
            task_cn = "把" + translate_plan[object] + "放到" + translate_plan[target] + "上。"
        elif "in" in task:
            task_cn = "把" + translate_plan[object] + "放到" + translate_plan[target] + "里。"
    task = "Your task is to: " + task + " > "
    task_cn = "你的任务是：" + task_cn + " > "
    # print(task, task_cn)
    return task, task_cn


type_path = {
    # "goto": ['goto'],
    # "take": ["take"],
    # "bring":["bring"],
    # "exist":["exist_yes"],
    "where": ["where"],
    # "exist_no":["exist_no"],
    # "put": ["put"]

}
root = "D:\legent\LEGENT\.legent\dataset"
train_path = "D:\legent\LEGENT\.legent\\train"
train_jsons_path = "D:\legent\LEGENT\.legent\\train_jsons"
train_jsons_path_cn = "D:\legent\LEGENT\.legent\\train_jsons_cn"

if not path.exists(train_path):
    os.makedirs(train_path)
if not path.exists(train_jsons_path):
    os.makedirs(train_jsons_path)
if not path.exists(train_jsons_path_cn):
    os.makedirs(train_jsons_path_cn)

#files = os.listdir(root)
number = 8332
for key, value in type_path.items():  #key:goto #value['goto', 'goto_410', 'goto_98']

    with open("D:\legent\LEGENT\.legent\\train_jsons\where_train_jsons.json", 'r') as file:
        train_jsons_list = json.load(file)
    with open("D:\legent\LEGENT\.legent\\train_jsons_cn\where_train_jsons_cn.json", 'r') as file:
        train_jsons_list_cn = json.load(file)
    task_id = 8332
    for file in value:
        trajs = os.listdir(path.join(root, file))
        for traj in trajs:
            number += 1
            print(number)
            if not os.path.isdir(path.join(root, file, traj)):
                continue
            task_id += 1
            image_id = 0

            with open(path.join(root, file, traj, 'task_setting.json'), 'r') as f:
                task_setting = json.load(f)
                plan = task_setting["plan"]
                task = task_setting["task"]
                solution = task_setting["solution"]
                plan.append("Task done.")
            with open(path.join(root, file, traj, 'trajectory.json'), 'r') as f:
                trajectory = json.load(f)
                image_actions = trajectory["interactions"][1]["trajectory"]

            if_docker, image_index = get_index(image_actions, key)
            plan, plan_cn = process_plan(plan, key, solution)
            task, task_cn = process_task(task, key)

            if len(plan) != len(image_index):
                print("\n\n")
                print(image_index, len(image_index))
                print(plan, len(plan))
                print("\n\n")
                continue
            text_input = task
            text_input_cn = task_cn
            for index, image in enumerate(image_index):
                image_name = key + str(task_id) + "_" + str(image_id) + ".png"
                image_path = path.join(train_path, image_name)
                shutil.copyfile(path.join(root, file, image), image_path)
                train_dir = {
                    "image": path.join("train", image_name),
                    "text_input": text_input,
                    "text_output": plan[index],
                    "task_id": task_id
                }
                train_dir_cn = {
                    "image": path.join("train", image_name),
                    "text_input": text_input_cn,
                    "text_output": plan_cn[index],
                    "task_id": task_id
                }
                image_id += 1
                train_jsons_list.append(train_dir)
                train_jsons_list_cn.append(train_dir_cn)
                text_input = text_input + plan[index] + " > "
                text_input_cn = text_input_cn + plan_cn[index] + " > "

    os.chmod(train_jsons_path, 0o777)
    os.chmod(train_jsons_path_cn, 0o777)
    train_jsons_path = path.join(train_jsons_path, key + "_" + "train_jsons.json")
    train_jsons_path_cn = path.join(train_jsons_path_cn, key + "_" + "train_jsons_cn.json")
    with open(train_jsons_path, 'w') as file:
        json.dump(train_jsons_list, file)
    with open(train_jsons_path_cn, 'w') as file:
        json.dump(train_jsons_list_cn, file)
