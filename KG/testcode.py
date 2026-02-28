# coding=utf-8
import re
import json
import os
import re

room_id = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
            11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
            21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
            201, 202, 203, 204, 205, 206, 207, 208, 209, 210,
            211, 212, 213, 214, 215, 216, 217, 218, 219, 220,
            221, 222, 223, 224, 225, 226, 227, 228, 229, 230,
            301, 302, 303, 304, 305, 306, 307, 308, 309, 310,
            311, 312, 313, 314, 315, 316, 317, 318, 319, 320,
            321, 322, 323, 324, 325, 326, 327, 328, 329, 330,
            401, 402, 403, 404, 405, 406, 407, 408, 409, 410,
            411, 412, 413, 414, 415, 416, 417, 418, 419, 420,
            421, 422, 423, 424, 425, 426, 427, 428, 429, 430]
# with open("KG/KG_result/gpt_4o.json", 'r') as file:
#     json_content = json.load(file)
# result = {}
# for key,value in json_content.items():
#     for string in value:
#         if "[" in string and "]" in string:
#             object_str = string
#             break
#     object_str = object_str.replace("\n","")
#     ret = re.match(r".*\[(.*)].*", object_str)
#     result[key] = [i.replace(" ","") for i in ret.group(1).split(",")]
# print(result,flush=True)
# print(len(result),flush=True)

# with open("KG/KG_result/truth.json", 'r') as file:
#     json_content = json.load(file)
# result = {}
# for key in sorted(json_content):
#     result[key] = json_content[key]
# with open("KG/KG_result/truth.json", 'w') as file:
#     json.dump(result, file)

####################################################################################
# result = {
#     "49.png":["wardrobe" , "television" , "remote control", "plant","dresser"],
# }
# for key in result.keys():
#     result[key] = result[key].split(".")
# with open(path.join("KG/test_result","example.json"), "w") as f:
#     json.dump(result, f)
#################################################################################
# from itertools import product
# a = [1,2,3,4]
# b= ["a","s","d"]
# for p,q in product(a,b):
#     print(p,q)

# with open("KG/KG_test_2/KG_identify.json", 'r') as file:
#     result = json.load(file)
# s = result[-1]
# print(s)
# ret_identify = re.match(".*\[(.*)\].*", s)
# identify_list_str = ret_identify.group(0)
################################################################################
# with open("json/scene.json", 'r') as file:
#     scene = json.load(file)
# name =set()
# for i in scene["instances"]:
#     if i["prefab"] in name:
#         print(i["prefab"])
#     else:
#         name.add(i["prefab"])
################################################################################
# ans = '''
# </think>
# 思考过程：
# 实体0分析：识别结果中的"床"与真实实体列表中的id39的"床"颜色均为灰色，名称相同，属性无冲突，判定匹配。
# 实体1分析：识别结果中的"床头柜"颜色为灰色，而真实列表中的"床头桌"颜色均为蓝色，颜色冲突且名称略有不同，无法匹配。
# 实体2分析：识别结果中的"台灯"颜色为橙色，与真实实体id44的"床头灯"颜色一致，尽管名称存在差异，但可能为同一物体的不同描述，判定匹配。
# 实体3分析：识别结果中的"书"与真实实体id63的"书"颜色均为绿色，名称和属性完全匹配。
# 实体4分析：识别结果中的"装饰画"颜色为黑色边框，与真实列表中的"墙上画"（绿色）颜色冲突，且"画框"类实体无颜色属性，无法建立对应关系。
#
# 对齐结果:
# {"物体序号":0,"名称": "床","属性": {"颜色": "灰色", "材质": "织物"}} - {"id":39,"名称":"床","属性": {"color": "灰色"}}
# {"物体序号":2,"名称": "台灯","属性": {"颜色": "橙色", "形状": "圆筒状", "位置": "床头柜上"}} - {"id":44,"名称":"床头灯","属性": {"color": "橙色"}}
# {"物体序号":3,"名称": "书","属性": {"颜色": "绿色", "位置": "床头柜上"}} - {"id":63,"名称":"书","属性": {"color": "绿色"}}
#
# 错误实体列表:
# [
#     {
#         "物体序号":1,
#         "名称": "床头柜",
#         "属性": {"颜色": "灰色", "材质": "木质"}
#     },
#     {
#         "物体序号":4,
#         "名称": "装饰画",
#         "属性": {"颜色": "黑色边框", "位置": "床左侧墙面"}
#     }
# ]
# '''
# from dynamic_KG import extract_data
#
# true_ans = ans.split("</think>")[1]
# wrong_str = true_ans.split("错误实体列表")[1]
# wrong = extract_data(wrong_str)
#
# identify_env_dict = {}
# ret = re.match(r".*?对齐结果(.*)错误实体列表.*?", true_ans, flags=re.S | re.M)
# if ret is not None:
#     strr = ret.group(1)
#     strr = strr.replace(" ", "")
#     strr = strr.replace("[", "")
#     strr = strr.replace("]", "")
#     sentences = strr.split("\n")
#     sentences = [i for i in sentences if len(i) > 0]
# else:
#     print(true_ans)
#     raise ()
# for sentence in sentences:
#     print(sentence)
#     if "{" not in sentence and "}" not in sentence:
#         continue
#     identify_object = extract_data("[" + sentence.split("-")[0] + "]")[0]
#     scene_object = extract_data("[" + sentence.split("-")[1] + "]")[0]
#     if "物体序号" in identify_object.keys():
#         identify_env_dict[identify_object["物体序号"]] = scene_object
# print(identify_env_dict)
#
# raise ()
#######################################################################################################
# from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
# import torch
#
# model_id = "/mnt/disk1/hf_models/DeepSeek-R1-Distill-Qwen-14B/"
# tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=False, trust_remote_code=True)
# model = AutoModelForCausalLM.from_pretrained(
#     model_id, device_map="auto", torch_dtype=torch.bfloat16, trust_remote_code=True
# )
# messages = [
#     {'role': 'system', 'content': '你是一个智能助手。'},
#     {'role': 'user', 'content': '请用一段话总结一下李世民一生的功绩。'}
# ]
# text = tokenizer.apply_chat_template(
#     messages,
#     tokenize=False,
#     add_generation_prompt=True
# )
# model_inputs = tokenizer([text], return_tensors="pt").to("cuda")
#
# model.generation_config = GenerationConfig.from_pretrained(model_id)
#
# generated_ids = model.generate(
#     model_inputs.input_ids,
#     max_new_tokens=10240,
#     pad_token_id=tokenizer.eos_token_id,
#     attention_mask=model_inputs['attention_mask']
# )
# generated_ids = [
#     output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
# ]
#
# response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
# print(response)
# import os
# os.environ["CUDA_VISIBLE_DEVICES"] = "1"
# from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
# import torch
#
# model_id = "/mnt/disk1/hf_models/DeepSeek-V2-Lite-Chat/"
# tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=False, trust_remote_code=True)
# model = AutoModelForCausalLM.from_pretrained(
#     model_id, device_map="auto", torch_dtype=torch.bfloat16, trust_remote_code=True
# )
# messages = ['请用一段话总结一下李世民一生的功绩。']
# inputs = tokenizer(messages, return_tensors="pt").to("cuda")
# outputs = model.generate(inputs["input_ids"],
#                          max_new_tokens=10240,
#                          pad_token_id=tokenizer.eos_token_id,
#                          attention_mask=inputs['attention_mask'])
# response = tokenizer.decode(outputs[0], skip_special_tokens=True)
# print(response)
# import os
# os.environ["CUDA_VISIBLE_DEVICES"] = "1"
# from identify import MedKG
# from liquid import Template
# medkg_deepseek = MedKG("deepseek/DeepSeek-R1-Distill-Qwen-32B")
# res = medkg_deepseek.generate_response("你是一名历史专家", Template('请用一段话总结一下李世民一生的功绩。{{list}}'), {"list":"分点回答"}, use_system=False)
# print(res)
# openai_api = "sk-LkzfPGogAtwqV3Fwox5MBx9S6iD1nbnGfu5aawxUTQYOzWMQ"
# openai_url = 'https://pro.xiaoai.plus/v1'
# from openai import OpenAI
# client = OpenAI(api_key=openai_api, base_url=openai_url)
# messages = [{"role": "user", "content": '请用一段话总结一下李世民一生的功绩。'}]
# ans = client.chat.completions.create(model="deepseek-v3", messages=messages)
# # print(ans)
# ans = ans.choices[0].message.content
##################################################################################################
# from dynamic_KG import extract_data
# ans = '''
# ### Thinking Process:
#
# 1. **Entity 0 Analysis**: The "kitchen counter" in the recognition result does not match any object in the real entity list, so it is judged as a wrong recognition.
# 2. **Entity 1 Analysis**: The "bowl" in the recognition result matches the "Bowl" in the real entity list in terms of name, and it is judged to match.
# 3. **Entity 2 Analysis**: The "tomato" in the recognition result matches the "Tomato" in the real entity list in terms of name, and it is judged to match.
# 4. **Entity 3 Analysis**: The "potato" in the recognition result matches the "Potato" in the real entity list in terms of name, and it is judged to match.
# 5. **Entity 4 Analysis**: The "egg" in the recognition result matches the "Egg" in the real entity list in terms of name, and it is judged to match.
# 6. **Entity 5 Analysis**: The "cabbage" in the recognition result does not match any object in the real entity list, so it is judged as a wrong recognition.
# 7. **Entity 6 Analysis**: The "frying pan" in the recognition result matches the "Pan" in the real entity list in terms of name, and it is judged to match.
# 8. **Entity 7 Analysis**: The "ladle" in the recognition result matches the "Ladle" in the real entity list in terms of name, and it is judged to match.
# 9. **Entity 8 Analysis**: The "chair 1" in the recognition result does not match any object in the real entity list, so it is judged as a wrong recognition.
# 10. **Entity 9 Analysis**: The "chair 2" in the recognition result does not match any object in the real entity list, so it is judged as a wrong recognition.
#
# ### Alignment Results:
# ```
# {"object number": 1, "name": "bowl", "attributes": {"color": "grey", "shape": "rectangular"}} <=> {"ID": 36, "name": "Bowl", "attributes": {}}
# {"object number": 2, "name": "tomato", "attributes": {"color": "red"}} <=> {"ID": 25, "name": "Tomato", "attributes": {}}
# {"object number": 3, "name": "potato", "attributes": {"color": "brown"}} <=> {"ID": 0, "name": "Potato", "attributes": {}}
# {"object number": 4, "name": "egg", "attributes": {"color": "white"}} <=> {"ID": 4, "name": "Egg", "attributes": {}}
# {"object number": 6, "name": "frying pan", "attributes": {"color": "black"}} <=> {"ID": 24, "name": "Pan", "attributes": {}}
# {"object number": 7, "name": "ladle", "attributes": {"color": "yellow and blue"}} <=> {"ID": 1, "name": "Ladle", "attributes": {}}
# ```
#
# ### List of Error Entities:
# ```
# [
#     {
#         "object number": 0,
#         "name": "kitchen counter",
#         "attributes": {"color": "white"}
#     },
#     {
#         "object number": 5,
#         "name": "cabbage",
#         "attributes": {"color": "green"}
#     },
#     {
#         "object number": 8,
#         "name": "chair 1",
#         "attributes": {"color": "yellow"}
#     },
#     {
#         "object number": 9,
#         "name": "chair 2",
#         "attributes": {"color": "yellow"}
#     }
# ]
# ```
#
# This output ensures that the alignment results and the list of error entities are consistent with the input data in terms of names, attributes, and IDs.
# '''
# true_ans = ans.split("</think>")[1] if "</think>" in ans else ans
# # ans = ans.split("\n")
# # ans[-1] = ans[-1].replace("\n", "")
# # ans[-1] = ans[-1].replace("\"", "")
# # print(ans[-1])
# # ret_identify = re.match(r".*\[(.*)].*", ans[-1])
# # identify_list_str = ret_identify.group(1)
# # wrong = identify_list_str.split(",")
# true_ans = true_ans.replace("Alignment Results", "Alignment results")
# true_ans = true_ans.replace("List of Error Entities", "List of error entities")
# wrong_str = true_ans.split("List of error entities")[1]#错误实体列表
# wrong = extract_data(wrong_str)
#
# identify_env_dict = {}
# ret = re.match(r".*?Alignment results(.*)List of error entities.*?", true_ans, flags=re.S | re.M)#r".*?对齐结果(.*)错误实体列表.*?"
# if ret is not None:
#     strr = ret.group(1)
#     strr = strr.replace("[", "")
#     strr = strr.replace("]", "")
#     sentences = strr.split("\n")
#     sentences = [i for i in sentences if len(i) > 0]
# else:
#     print(true_ans)
#     raise ()
# for sentence in sentences:
#     print(sentence)
#     if "{" not in sentence and "}" not in sentence:
#         continue
#     identify_object = extract_data("[" + sentence.split("<=>")[0] + "]")[0]
#     scene_object = extract_data("[" + sentence.split("<=>")[1] + "]")[0]
#     # print(identify_object,scene_object)
#     if "object number" in identify_object.keys():#物体序号
#         identify_env_dict[str(identify_object["object number"])] = scene_object#物体序号
# print(identify_env_dict)
