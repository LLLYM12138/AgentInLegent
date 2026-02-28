# coding=utf-8
import json
import os
from openai import OpenAI
from zhipuai import ZhipuAI
from KG.prompt import *
import base64
import os.path as path
import re
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
import torch
import time

openai_api = "sk-LkzfPGogAtwqV3Fwox5MBx9S6iD1nbnGfu5aawxUTQYOzWMQ"
openai_url = 'https://pro.xiaoai.plus/v1'
zhiyuan_api = "4b7cda8ce47a13c743b60fe927eec2c1.YQrmvP2LunUK0vAm"
hunyuan_api = "sk-ophi66xizyPVctxN13wtI4yyCuzNQ2ImOWGKbxNZLqvqwcar"
baidu_api = "bce-v3/ALTAK-UozfCdiPiCO5Ol7J5Qybs/2a37de584399565781f02cd1d5578e73c9652a93"


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


class MedKG:
    def __init__(self, llm_name=""):
        self.llm_name = llm_name
        self.templates = {
            "general_system": general_system,
            "general": general,
        }
        self.load_llm_model(llm_name)
        self.model = llm_name.split("/")[1]

    def load_llm_model(self, llm_name):
        model_loaders = {
            "openai": self._load_openai_model,
            "zhiyuan": self._load_zhiyuan_model,
            "hunyuan": self._load_hunyuan_model,
            "baidu": self._load_baidu_model,
            "deepseek": self._load_deepseek_model,
            "aliyuncs": self._load_aliyuncs_model,
        }
        self.llm_type = llm_name.split("/")[0]
        if self.llm_type in model_loaders:
            model_loaders[self.llm_type]()
        else:
            raise ValueError(f"Unsupported model type: {self.llm_type}")

    # def _load_qwen_model(self, model_path):
    # def _load_baichuan_model(self, model_path):

    def _load_openai_model(self):
        self.client = OpenAI(api_key=openai_api, base_url=openai_url)

    def _load_zhiyuan_model(self):
        self.client = ZhipuAI(api_key=zhiyuan_api)

    def _load_hunyuan_model(self):
        self.client = OpenAI(
            api_key=hunyuan_api,  # 混元 APIKey
            base_url="https://api.hunyuan.cloud.tencent.com/v1",  # 混元 endpoint
        )

    def _load_baidu_model(self):
        self.client = OpenAI(
            api_key=baidu_api,
            # 千帆ModelBuilder平台bearer token
            base_url="https://qianfan.baidubce.com/v2",  # 千帆ModelBuilder平台域名
            default_headers={"appid": "app-Mu***q6"}  # 千帆ModelBuilder平台应用ID，非必传
        )

    def _load_deepseek_model(self):
        # self.model_id = "/mnt/disk1/hf_models/DeepSeek-R1-Distill-Qwen-14B/"
        # self.tokenizer = AutoTokenizer.from_pretrained(self.model_id, use_fast=False, trust_remote_code=True)
        # self.pre_model = AutoModelForCausalLM.from_pretrained(
        #     self.model_id, device_map="auto", torch_dtype=torch.bfloat16, trust_remote_code=True
        # )
        model_id = "/mnt/disk1/hf_models/DeepSeek-V2-Lite-Chat/"
        self.tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=False, trust_remote_code=True)
        self.pre_model = AutoModelForCausalLM.from_pretrained(
            model_id, device_map="auto", torch_dtype=torch.bfloat16, trust_remote_code=True
        )
    def _load_aliyuncs_model(self):
        self.client = OpenAI(
            api_key="sk-25459c274f3d4055ba90384d692944cd",
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
    def generate(self, messages, max_new_tokens=512, max_retries=6):
        attempts = 0
        while attempts < max_retries:
            try:
                if "openai" in self.llm_name.lower():
                    ans = self.client.chat.completions.create(model=self.model, messages=messages)
                    # print(ans)
                    ans = ans.choices[0].message.content
                elif "zhiyuan" in self.llm_name.lower():
                    # print(messages)
                    response = self.client.chat.completions.create(
                        model=self.model,  #glm-4-plus/glm-4-flash
                        messages=messages
                    )
                    ans = response.choices[0].message.content
                elif "hunyuan" in self.llm_name.lower():
                    # print(messages)
                    response = self.client.chat.completions.create(
                        model="hunyuan-lite",
                        messages=messages
                    )
                    ans = response.choices[0].message.content
                elif "baidu" in self.llm_name.lower():
                    response = self.client.chat.completions.create(
                        model="ernie-speed-128k",  # 预置服务请查看支持的模型列表
                        messages=messages
                    )
                    ans = response.choices[0].message.content
                elif "aliyuncs" in self.llm_name.lower():
                    response = self.client.chat.completions.create(
                        model=self.model,  # 预置服务请查看支持的模型列表
                        messages=messages
                    )
                    ans = response.choices[0].message.content
                elif "deepseek" in self.llm_name.lower():
                    if "content" in messages[0].keys():
                        messages = messages[0]["content"]
                    else:
                        messages = str(messages)
                    inputs = self.tokenizer(messages, return_tensors="pt").to("cuda")
                    outputs = self.pre_model.generate(inputs["input_ids"],
                                             max_new_tokens=10240,
                                             pad_token_id=self.tokenizer.eos_token_id,
                                             attention_mask=inputs['attention_mask'])
                    ans = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
                else:
                    raise ValueError("Unsupported model type")
                # print(ans)
                return ans
            except Exception as e:
                attempts += 1
                print(f"Error during generation (attempt {attempts}/{max_retries}): {e}")
                if attempts == 5:
                    time.sleep(20)
                    print("sleep 20s")
                if attempts >= max_retries:
                    print("Maximum retry attempts reached. Returning empty response.")
                    return {}
                else:
                    print("Retrying...")

    def generate_picture_response(self, system, user_prompt, pic_path):
        # prompt = user_prompt.render(data)
        base64_images = []
        if isinstance(pic_path, list):
            for file in pic_path:
                base64_image = encode_image(file)
                base64_images.append(base64_image)
        else:
            base64_image = encode_image(pic_path)
            base64_images.append(base64_image)
        content = [
            {"type": "text", "text": user_prompt}
        ]
        if self.llm_type == "openai":
            content.extend([
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                }
                for base64_image in base64_images
            ])
        elif self.llm_type == "zhiyuan":
            content.extend([
                {
                    "type": "image_url",
                    "image_url": {"url": base64_image},
                }
                for base64_image in base64_images
            ])
        else:
            content.extend([
                {
                    "type": "image_url",
                    "image_url": {"url": base64_image},
                }
                for base64_image in base64_images
            ])
        messages = [
            {
                "role": "system",
                "content": [
                    {"type": "text",
                     "text": system}
                ]
            },
            {
                "role": "user",
                "content": content
            }
        ]
        return self.generate(messages=messages)

    def lym_response(self, system, user, data, use_system=True):
        prompt = user.render(data)
        if use_system:
            messages = [{"role": "system", "content": system}, {"role": "user", "content": prompt}]
        else:
            messages = [{"role": "user", "content": system + prompt}]
        print("查询大模型的prompt如下：")
        print(system + prompt)
        print("请输入大模型回复：")
        ans = ""
        while True:
            input_str = input()
            if input_str == "LYMEND":
                print("输入结束")
                break
            else:
                ans = ans + input_str + "\n"

        return ans

    def generate_response(self, system, user, data, use_system=True):
        prompt = user.render(data)
        if use_system:
            messages = [{"role": "system", "content": system}, {"role": "user", "content": prompt}]
        else:
            messages = [{"role": "user", "content": system + prompt}]

        return self.generate(messages=messages)

    def generate_picture_mutilturn_response(self, history_content, user_prompt, data):
        prompt = user_prompt.render(data)
        messages = history_content
        messages.append(
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}]
            }
        )
        return self.generate(messages=messages)


def test_all_picture(model_name):
    medkg = MedKG(model_name)
    pictures = os.listdir("KG/KG_image")
    result = {}
    for pic in pictures:
        if "jpg" not in pic:
            continue
        pic_path = path.join("KG/KG_image", pic)
        ans = medkg.generate_picture_response(chinese_identify_system, chinese_identify_user, pic_path)
        result[pic] = ans.split(".")
        # print(pic, ans)
    with open(path.join("KG/KG_result", model_name.split("/")[1] + "2.json"), "w") as f:
        json.dump(result, f)


#测试图片：
if __name__ == "__main__":
    # test_all_picture("zhiyuan/glm-4v-plus")
    # test_all_picture("openai/gpt-4-vision-preview")
    # medkg = MedKG("openai/gpt-4o")
    # ans = medkg.generate_response(general_system, general, "KG/test_image/02.jpg")
    # print(ans)
    ####################################################################################
    root_path = "KG/KG_test_2"
    # lym = ["红色面条盒","书","沙发","画","壁炉","红酒杯","一瓶红酒","酱油","寿司","小木桌","盆栽1","盆栽2","筷子"]
    # with open(os.path.join(root_path,"KG_truth.json"), "w") as f:
    #     json.dump(lym, f)
    # raise()
    ## 识别实体
    # medkg = MedKG("openai/gpt-4o")
    # pictures = [
    #     os.path.join(root_path, image)
    #     for image in ["01.png", "02.png", "03.png"]
    # ]
    # ans = medkg.generate_picture_response(chinese_identify_system, chinese_identify_user, pictures)
    # result = ans.split("\n")
    # print(result)
    # with open(os.path.join(root_path, "KG_identify.json"), "w") as f:
    #     json.dump(result, f)

    # # 实体匹配
    # with open(os.path.join(root_path, "KG_identify.json"), 'r') as file:
    #     result = json.load(file)
    # result[-1] = result[-1].replace("\n","")
    # ret_identify = re.match(r".*\[(.*)].*", result[-1])
    # identify_list_str = ret_identify.group(1)
    # result = identify_list_str.split(",")
    # # result = ["沙发", "茶几", "电视柜", "奖杯", "遥控器", "电视",
    # #           "画", "落地灯", "小盆栽", "书", "纸杯", "玻璃杯"]
    # with open(os.path.join(root_path, "KG_truth.json"), 'r') as file:
    #     truth = json.load(file)
    # medkg = MedKG("openai/gpt-4-0613")
    # data = {"list": str(result), "list_truth": str(truth)}
    # ans = medkg.generate_response(entity_alignment_chinese_system, entity_alignment_chinese, data, use_system=False)
    # print(ans)
    # with open(os.path.join(root_path, "KG_alignment_gpt-4-0613.json"), "w") as f:
    #     json.dump(ans, f)

    # with open("KG/KG_test_2/KG_alignment_gpt-4-0613.json", 'r') as file:
    #     test1 = json.load(file)
    # with open("KG/KG_test_2/KG_alignment_o1-preview.json", 'r') as file:
    #     test2 = json.load(file)
    # with open("KG/KG_test_1/KG_alignment_gpt-4-0613.json", 'r') as file:
    #     test1 = json.load(file)
    # with open("KG/KG_test_1/KG_alignment_o1-preview.json", 'r') as file:
    #     test2 = json.load(file)
    # print(test1)
    # print(test2)

    ##图谱生成1
    # medkg = MedKG("openai/gpt-4o")
    # with open(os.path.join(root_path,"KG_identify.json"), 'r') as file:
    #     result = json.load(file)
    # with open(os.path.join(root_path,"KG_alignment_o1-preview.json"), 'r') as file:
    #     wrong = json.load(file)
    # sentence = wrong.split("\n")[-1]
    # ret = re.match(r".*\[(.*)].*", sentence)
    # data = {"wrong": "["+ret.group(1)+"]"}
    #
    # base64_images = []
    # for file in pictures:
    #     base64_image = encode_image(file)
    #     base64_images.append(base64_image)
    # content = [{"type": "text", "text": chinese_identify_user}]+[
    #         {
    #             "type": "image_url",
    #             "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
    #         }
    #         for base64_image in base64_images
    #     ]
    # history_content = [
    #     {
    #         "role": "system",
    #         "content": [{"type": "text","text": chinese_identify_system}]
    #     },
    #     {
    #         "role": "user",
    #         "content": content
    #     },
    #     {
    #         "role": "assistant",
    #         "content": [{"type": "text","text": result}]
    #     },
    # ]
    #
    # ans = medkg.generate_picture_mutilturn_response(history_content, KG_history_chinese_user, data)
    # print(ans)
    # with open(os.path.join(root_path,"KG.json"), "w") as f:
    #     json.dump(ans, f)

    # ## 图谱生成2
    medkg = MedKG("openai/gpt-4o")
    pictures = [
        os.path.join(root_path, image)
        for image in ["01.png", "02.png", "03.png"]
    ]

    with open(os.path.join(root_path, "KG_identify.json"), 'r') as file:
        identify = json.load(file)
    with open(os.path.join(root_path, "KG_alignment_o1-preview.json"), 'r') as file:
        wrong = json.load(file)
    ret_identify = re.match(r".*\[(.*)].*", identify[-1])
    identify_list_str = ret_identify.group(1)
    identify_list_str = identify_list_str.replace(" ", "")
    identify_list_str = identify_list_str.replace("\'", "")
    identify_list = identify_list_str.split(",")
    ret_alignment = re.match(r".*\[(.*)].*", wrong.split("\n")[-1])
    alignment_list_str = ret_alignment.group(1)
    alignment_list_str = alignment_list_str.replace(" ", "")
    alignment_list_str = alignment_list_str.replace("\'", "")
    alignment_list = alignment_list_str.split(",")
    object_list = list(set(identify_list) - set(alignment_list))
    #object_list = ["沙发", "茶几", "电视柜", "奖杯", "遥控器", "电视", "画", "落地灯", "小盆栽", "纸杯", "玻璃杯"]

    prompt_user = KG_chinese_user.render({"list": str(object_list)})
    ans = medkg.generate_picture_response(KG_chinese_system, prompt_user, pictures)
    print(ans)
    with open(os.path.join(root_path, "KG.json"), "w") as f:
        json.dump(ans, f)
