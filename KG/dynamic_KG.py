# coding=utf-8
from KG.identify import MedKG
import json
import os
import time

os.environ["CUDA_VISIBLE_DEVICES"] = "4"
from shutil import copyfile
from openai import OpenAI
from zhipuai import ZhipuAI
from KG.prompt import *
import base64
import os.path as path
import re


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


def extract_data(ans):
    ans = ans.replace("'", "\"")
    ans = ans.replace("None", "\"None\"")
    ans = ans.replace("True", "\"True\"")
    ans = ans.replace("False", "\"False\"")
    # ret = re.match(r".*```json(.*)```.*", ans, flags=re.S | re.M)
    try:
        ret = re.match(r".*?(\[.*]).*?", ans, flags=re.S | re.M)
        if ret is not None:
            cleaned_data = ret.group(1)
        else:
            raise UnboundLocalError
        # cleaned_data = ans.strip('```json').strip('```').strip()
        parsed_data = json.loads(cleaned_data)
    except Exception as e:
        print("ans:")
        print(ans)
        if ret is not None:
            print("clean data:")
            print(cleaned_data)
        print(e)
    # print(parsed_data)
    return parsed_data


def identify(pictures, root_path, medkg):  #输入:图片列表,输出结果的路径
    attempts = 0
    max_retries = 6
    while attempts < max_retries:
        try:
            ans = medkg.generate_picture_response(identify_system, identify_user, pictures)
            # ans = ans.split("\n")
            # ans[-1] = ans[-1].replace("\n", "")
            # ans[-1] = ans[-1].replace("\"", "")
            # print(ans[-1])
            # ret_identify = re.match(r".*\[(.*)].*", ans[-1])
            # identify_list_str = ret_identify.group(1)
            # result = identify_list_str.split(",")
            result = extract_data(ans)
            if result is not None:
                break
        except Exception as e:
            attempts += 1
            print(f"\nError during generation (attempt {attempts}/{max_retries}): {e}")
            if attempts == 3:
                time.sleep(10)
                print("wait 10 seconds")
            if attempts >= max_retries:
                print("\nMaximum retry attempts reached. Returning empty response.")
                raise ()
            else:
                print("\nRetrying...")
    # if not os.path.exists(os.path.join(root_path, "identify.json")):
    #     with open(os.path.join(root_path, "identify.json"), "w") as f:
    #         json.dump([], f)
    # with open(os.path.join(root_path, "identify.json"), 'r') as file:
    #     record = json.load(file)
    # record.append([ans, result])
    # with open(os.path.join(root_path, "identify.json"), "w") as f:
    #     json.dump(record, f)
    print("identify:", flush=True)
    print(result, flush=True)
    print("*" * 50, flush=True)
    return result


def entity_alignment_en(identify, truth, root_path, medkg):
    attempts = 0
    max_retries = 3
    #返回：identify_env_dict[物体序号] = 对应对象字典 /// wrong：错误列表
    for i in range(len(identify)):
        if "object number" not in identify[i].keys():  #物体序号
            identify[i].update({"object number": i})  #物体序号
    data = {"list": str(identify), "list_truth": str(truth)}

    # ans = medkg.lym_response(entity_alignment_chinese_system, entity_alignment_chinese, data, use_system=False)
    ans = medkg.generate_response(entity_alignment_system, entity_alignment_user, data,
                                  use_system=False)
    # print(ans)
    while attempts < max_retries:
        try:
            true_ans = ans.split("</think>")[1] if "</think>" in ans else ans
            # ans = ans.split("\n")
            # ans[-1] = ans[-1].replace("\n", "")
            # ans[-1] = ans[-1].replace("\"", "")
            # print(ans[-1])
            # ret_identify = re.match(r".*\[(.*)].*", ans[-1])
            # identify_list_str = ret_identify.group(1)
            # wrong = identify_list_str.split(",")
            true_ans = true_ans.replace("Alignment Results", "Alignment results")
            true_ans = true_ans.replace("List of Error Entities", "List of error entities")
            wrong_str = true_ans.split("List of error entities")[1]  #错误实体列表

            wrong = extract_data(wrong_str)

            identify_env_dict = {}
            ret = re.match(r".*?Alignment results(.*)List of error entities.*?", true_ans,
                           flags=re.S | re.M)  #r".*?对齐结果(.*)错误实体列表.*?"
            if ret is not None:
                strr = ret.group(1)
                # strr = strr.replace("object number", "object-number")
                # strr = strr.replace(" ", "")
                # strr = strr.replace("object-number", "object number")
                strr = strr.replace("[", "")
                strr = strr.replace("]", "")
                sentences = strr.split("\n")
                sentences = [i for i in sentences if len(i) > 0]
            else:
                print(true_ans, flush=True)
                raise Exception("正则匹配错误")
            for sentence in sentences:
                if "{" not in sentence and "}" not in sentence:
                    continue
                identify_object = extract_data("[" + sentence.split("<=>")[0] + "]")[0]
                scene_object = extract_data("[" + sentence.split("<=>")[1] + "]")[0]
                if "object number" in identify_object.keys():  #物体序号
                    identify_env_dict[str(identify_object["object number"])] = scene_object  #物体序号
            if identify_env_dict is not None:
                break
            else:
                print("*" * 50, flush=True)
                print(strr, flush=True)
                print("*" * 50, flush=True)
                raise Exception("结果错误", flush=True)
        except Exception as e:
            attempts += 1
            print(f"\nError during generation (attempt {attempts}/{max_retries}): {e}", flush=True)
            print("ans:", flush=True)
            print(ans, flush=True)
            print("****************************************************", flush=True)
            if attempts >= max_retries:
                print("Maximum retry attempts reached. Returning empty response.", flush=True)
                raise ()
            else:
                print("Retrying...", flush=True)
    # if not os.path.exists(os.path.join(root_path, "wrong.json")):
    #     with open(os.path.join(root_path, "wrong.json"), "w") as f:
    #         json.dump([], f)
    # with open(os.path.join(root_path, "wrong.json"), 'r') as file:
    #     record = json.load(file)
    # record.append([true_ans, identify_env_dict, wrong])
    # with open(os.path.join(root_path, "wrong.json"), "w") as f:
    #     json.dump(record, f)
    print("entity_alignment:", flush=True)
    print(identify_env_dict, flush=True)
    print("*" * 50, flush=True)
    return identify_env_dict, wrong

def entity_alignment_cn(identify, truth, root_path, medkg):
    attempts = 0
    max_retries = 3
    #返回：identify_env_dict[物体序号] = 对应对象字典 /// wrong：错误列表
    for i in range(len(identify)):
        if "物体序号" not in identify[i].keys():  #物体序号
            identify[i].update({"物体序号": i})  #物体序号
    data = {"list": str(identify), "list_truth": str(truth)}

    # ans = medkg.lym_response(entity_alignment_chinese_system, entity_alignment_chinese, data, use_system=False)
    ans = medkg.generate_response(entity_alignment_chinese_system, entity_alignment_chinese, data,
                                  use_system=False)
    # print(ans)
    while attempts < max_retries:
        try:
            true_ans = ans.split("</think>")[1] if "</think>" in ans else ans
            # ans = ans.split("\n")
            # ans[-1] = ans[-1].replace("\n", "")
            # ans[-1] = ans[-1].replace("\"", "")
            # print(ans[-1])
            # ret_identify = re.match(r".*\[(.*)].*", ans[-1])
            # identify_list_str = ret_identify.group(1)
            # wrong = identify_list_str.split(",")
            wrong_str = true_ans.split("错误实体列表")[1]  #错误实体列表

            wrong = extract_data(wrong_str)

            identify_env_dict = {}
            ret = re.match(r".*?对齐结果(.*)错误实体列表.*?", true_ans,
                           flags=re.S | re.M)  #r".*?对齐结果(.*)错误实体列表.*?"
            if ret is not None:
                strr = ret.group(1)
                # strr = strr.replace("object number", "object-number")
                # strr = strr.replace(" ", "")
                # strr = strr.replace("object-number", "object number")
                strr = strr.replace("[", "")
                strr = strr.replace("]", "")
                sentences = strr.split("\n")
                sentences = [i for i in sentences if len(i) > 0]
            else:
                print(true_ans, flush=True)
                raise Exception("正则匹配错误")
            for sentence in sentences:
                if "{" not in sentence and "}" not in sentence:
                    continue
                identify_object = extract_data("[" + sentence.split("<=>")[0] + "]")[0]
                scene_object = extract_data("[" + sentence.split("<=>")[1] + "]")[0]
                if "物体序号" in identify_object.keys():  #物体序号
                    identify_env_dict[str(identify_object["物体序号"])] = scene_object  #物体序号
            if len(identify_env_dict) >= 0:
                break
            else:
                print("*" * 50, flush=True)
                print(strr, flush=True)
                print("*" * 50, flush=True)
                raise Exception("结果错误", flush=True)
        except Exception as e:
            attempts += 1
            print(f"\nError during generation (attempt {attempts}/{max_retries}): {e}", flush=True)
            print("ans:", flush=True)
            print(ans, flush=True)
            print("****************************************************", flush=True)
            if attempts >= max_retries:
                print("Maximum retry attempts reached. Returning empty response.", flush=True)
                raise ()
            else:
                print("Retrying...", flush=True)
    # if not os.path.exists(os.path.join(root_path, "wrong.json")):
    #     with open(os.path.join(root_path, "wrong.json"), "w") as f:
    #         json.dump([], f)
    # with open(os.path.join(root_path, "wrong.json"), 'r') as file:
    #     record = json.load(file)
    # record.append([true_ans, identify_env_dict, wrong])
    # with open(os.path.join(root_path, "wrong.json"), "w") as f:
    #     json.dump(record, f)
    print("entity_alignment:", flush=True)
    print(identify_env_dict, flush=True)
    print("*" * 50, flush=True)
    return identify_env_dict, wrong


def KG_json(pictures, object_list, root_path, medkg):
    attempts = 0
    max_retries = 3
    while attempts < max_retries:
        try:
            prompt_user = KG_user.render({"list": str(object_list)})
            ans = medkg.generate_picture_response(KG_system, prompt_user, pictures)
            relations = extract_data(ans)
            if relations is not None:
                break
        except Exception as e:
            attempts += 1
            print(f"\nError during generation (attempt {attempts}/{max_retries}): {e}")
            if attempts >= max_retries:
                print("\nMaximum retry attempts reached. Returning empty response.")
                raise ()
            else:
                print("\nRetrying...")
    print("KG_json:", flush=True)
    print(relations, flush=True)
    print("*" * 50, flush=True)
    # if not os.path.exists(os.path.join(root_path, "KG.json")):
    #     with open(os.path.join(root_path, "KG.json"), "w") as f:
    #         json.dump([], f)
    # with open(os.path.join(root_path, "KG.json"), 'r') as file:
    #     record = json.load(file)
    # record.append([ans, relations])
    # with open(os.path.join(root_path, "KG.json"), "w") as f:
    #     json.dump(record, f)
    return relations


def matching_object(i, identify_env, scene, env):
    if env:
        env_id = identify_env['ID']
        # env_describe = identify_env_dict[i]['属性']
    else:
        env_id = None

    if "name" in i.keys():  #名称
        name = i["name"]  #名称
    else:
        name = None
    if "attributes" in i.keys():  #"属性"
        if "color" in i["attributes"].keys():  #"颜色"#"属性"
            color = i["attributes"]["color"]  #"属性"#"颜色"
            other = {k: v for k, v in i["attributes"].items() if k != "color"}  #"属性"#"颜色"
        else:
            color = None
            other = i["attributes"]  #"属性"
    else:
        color = None
        other = None

    return {
        "env_id": env_id,
        "env_name": scene["instances"][env_id]["prefab"] if env_id is not None else env_id,
        "name": name,
        "color": color,
        "other": other
    }


def parse_KG(relation):
    if 'head entity' in relation.keys() and 'tail entity' in relation.keys() and 'relationship type' in relation.keys():
        if 'ID' in relation['head entity'].keys() and 'ID' in relation['tail entity'].keys():
            output = str(relation['head entity']['ID']) + "..." + relation['relationship type'] + "..." + str(
                relation['tail entity']['ID'])
            output_list = [relation['head entity']['ID'], relation['relationship type'], relation['tail entity']['ID']]
        else:
            output = None
            output_list = []
            print(f"输出结构错误：{relation}")
    else:
        output = None
        output_list = []
        print(f"输出结构错误：{relation}")
    return output, output_list


def init_KG(pic, room, root_path, medkg_dict, scene, need_room_filiter):
    # object : id,env_id,env_name,object_name,room,color
    truth = []
    for i, object in enumerate(scene["instances"]):
        if need_room_filiter and get_room(object["position"]) == room and len(object["describe"]) > 0:
            truth.append({
                "ID": object["id"],
                "name": object["describe"]["name"],  #名称
                "attributes": {k: v for k, v in object["describe"].items() if k != "name"}  #属性
            })
        elif not need_room_filiter:
            truth.append({
                "ID": object["id"],
                "name": object["describe"]["name"].split("_")[0],  #名称
                "attributes": {k: v for k, v in object["describe"].items() if k != "name"}  #属性
            })
    result = identify(pic, root_path, medkg_dict["identify"])
    identify_env_dict, wrong = entity_alignment_en(result, truth, root_path, medkg_dict["entity_alignment"])

    objects = []
    for i, res in enumerate(result):
        if str(i) in identify_env_dict.keys():
            j = matching_object(res, identify_env_dict[str(i)], scene, True)
        else:
            j = matching_object(res, None, scene, False)
        object = {
            'ID': len(objects),
            'env id': j["env_id"],
            'env name': j["env_name"],
            'object name': j["name"],
            'room': room,
            'color': j["color"],
            'other': j["other"]
        }
        objects.append(object)
    with open(os.path.join(root_path, "object.json"), "w") as f:
        json.dump(objects, f)

    KG_json_input = [
        {
            "ID": i["ID"],
            "name": i['object name'],
            "attributes": {"color": i["color"]}
        }
        for i in objects
    ]
    relations = KG_json(pic, KG_json_input, root_path, medkg_dict["KG_json"])
    for i in relations:
        relation, relation_list = parse_KG(i)
        if relation is not None:
            with open(os.path.join(root_path, "KG.txt"), 'a') as file:
                file.write(f'{relation}\n')


def add_KG(pic, room, root_path, medkg_dict, scene, need_room_filiter):  #pic为[一张图]
    # object : id,env_id,env_name,object_name,room,color
    truth = []
    for i, object in enumerate(scene["instances"]):
        if need_room_filiter and get_room(object["position"]) == room and len(object["describe"]) > 0:
            truth.append({
                "ID": object["id"],
                "name": object["describe"]["name"],
                "attributes": {k: v for k, v in object["describe"].items() if k != "name"}
            })
        elif not need_room_filiter:
            truth.append({
                "ID": object["id"],
                "name": object["describe"]["name"].split("_")[0],
                "attributes": {k: v for k, v in object["describe"].items() if k != "name"}
            })
    result = identify(pic, root_path, medkg_dict["identify"])
    identify_env_dict, wrong = entity_alignment_en(result, truth, root_path, medkg_dict["entity_alignment"])

    #到这里已经有图片内的所有物体，单独从0开始编号
    objects = []
    for i, res in enumerate(result):
        if str(i) in identify_env_dict.keys():
            j = matching_object(res, identify_env_dict[str(i)], scene, True)
        else:
            j = matching_object(res, None, scene, False)
        object = {
            'ID': len(objects),
            'env id': j["env_id"],
            'env name': j["env_name"],
            'object name': j["name"],
            'room': room,
            'color': j["color"],
            'other': j["other"]
        }
        objects.append(object)
    KG_json_input = [
        {
            "ID": i["ID"],
            "name": i['object name'],
            "attributes": {"color": i["color"]}
        }
        for i in objects
    ]
    relations = KG_json(pic, KG_json_input, root_path, medkg_dict["KG_json"])
    pic_relation = []
    for i in relations:
        relation, relation_list = parse_KG(i)
        if relation is not None:
            pic_relation.append(relation_list)
    #到这里已经有图片内的所有空间关系
    #接下来求图片内物体与图谱内物体有何重复
    for _ in range(3):
        try:
            with open(os.path.join(root_path, "object.json"), 'r') as file:
                KG_objects = json.load(file)
            new = {}
            old = {}
            for i in [j for j in objects if j["env id"] is not None]:
                flag = False
                for k in KG_objects:
                    if i["env id"] == k["env id"]:
                        old[str(i["ID"])] = k["ID"]
                        flag = True
                        break
                if flag == False:
                    new[str(i["ID"])] = 0
            no_env_id_object = [
                {
                    "object number": object['ID'],
                    "name": object['object name'],
                    "attributes": {"color": object['color']}
                }
                for object in objects
                if object["env id"] is None
            ]
            KG_objects_input = [
                {
                    "ID": object['ID'],
                    "name": object['object name'],
                    "attributes": {"color": object['color']}
                }
                for object in KG_objects
            ]
            no_env_id_old_dict, no_env_id_new_object = entity_alignment_en(no_env_id_object, KG_objects_input, root_path,
                                                                        medkg_dict["entity_alignment"])
            for k, v in no_env_id_old_dict.items():
                if "ID" in v.keys():
                    old[k] = v["ID"]
            for i in no_env_id_new_object:
                if "object number" in i.keys():
                    new[str(i["object number"])] = 0

            #现在new和old分别保存了新老实体
            for i in objects:
                if str(i["ID"]) in new.keys():
                    new[str(i["ID"])] = len(KG_objects)
                    i["ID"] = len(KG_objects)
                    KG_objects.append(i)
            with open(os.path.join(root_path, "object.json"), "w") as f:
                json.dump(KG_objects, f)
            NewOld = new
            NewOld.update(old)
            for i in pic_relation:
                if str(i[0]) in new.keys() and str(i[2]) in new.keys():
                    with open(os.path.join(root_path, "KG.txt"), 'a') as file:
                        file.write(f'{NewOld[str(i[0])]}...{str(i[1])}...{NewOld[str(i[2])]}\n')
                elif str(i[0]) in old.keys() or str(i[2]) in old.keys():
                    write_str = f'{NewOld[str(i[0])]}...{str(i[1])}...{NewOld[str(i[2])]}\n'
                    flag = True
                    with open(os.path.join(root_path, "KG.txt"), 'r') as file:
                        for line in file:
                            if line == write_str:
                                flag = False
                                break
                    if flag:
                        with open(os.path.join(root_path, "KG.txt"), 'a') as file:
                            file.write(write_str)
            break
        except Exception as e:
            print(no_env_id_object, "\n", KG_objects_input, "\n", no_env_id_old_dict, "\n", no_env_id_new_object)
            print(e)
            time.sleep(10)
            continue


if __name__ == "__main__":

    #要求：
    #
    #scene文件路径：json/scene.json
    #结果路径：KG/KG_test_3
    #图片路径：KG/KG_test_3/image/

    with open("json/scene.json", 'r', encoding='GBK') as file:
        scene = json.load(file)
    room = "First Floor Bedroom1"
    medkg_gpt = MedKG("openai/gpt-4o")
    medkg_deepseek = MedKG("deepseek/DeepSeek-R1-Distill-Qwen-32B")
    medkg_dict = {
        "identify": medkg_gpt,
        "entity_alignment": medkg_deepseek,
        "KG_json": medkg_gpt
    }
    init_KG(["KG/KG_test_3/image/human1.jpg"], "First Floor Bedroom1", "KG/KG_test_3", medkg_dict, scene, True)
    for i in range(2, 6):
        add_KG([f"KG/KG_test_3/image/human{i}.jpg"], "First Floor Bedroom1", "KG/KG_test_3", medkg_dict, scene, True)
