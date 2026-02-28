import subprocess
import os
import json
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
images = ['103.jpg', '105.jpg', '106.jpg', '129.jpg', '130.jpg', '146.jpg', '209.jpg', '210.jpg', '233.jpg', '24.jpg', '312.jpg', '316.jpg', '332.jpg', '370.jpg', '379.jpg', '384.jpg', '414.jpg', '49.jpg', '58.jpg', '63.jpg', '64.jpg', '97.jpg']
result = {}
for image in images:
    print(image,flush=True)
    path = os.path.join("/mnt/disk1/wanght/liym/work/recognize-anything/KG_image/", image)
    model_path1 = "/mnt/disk1/wanght/liym/work/recognize-anything/pretrain/ram_plus_swin_large_14m.pth"
    model_path2 = "/mnt/disk1/wanght/liym/work/recognize-anything/pretrain/tag2text_swin_14m.pth"
    proc = subprocess.Popen(
        # f"python inference_ram_plus.py --image {path} --pretrained {model_path1}",
        f"python inference_tag2text.py  --image {path} --pretrained {model_path2}",
        stdin=None, # 标准输入 键盘
        stdout=subprocess.PIPE, # -1 标准输出（演示器、终端) 保存到管道中以便进行操作
        stderr=subprocess.PIPE,
        shell=True)
    outinfo, errinfo = proc.communicate()
    print(outinfo.decode('utf-8'),flush=True)
    result[image] = outinfo.decode('utf-8')

with open("/mnt/disk1/wanght/liym/work/recognize-anything/ram_plus_swin_large_14m.json","w") as f:
    json.dump(result,f)