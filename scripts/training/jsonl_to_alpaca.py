
import os
from decouple import config as decouple_config
import shutil
import json
import random



def recreate_sample_folder(folder_path=""):
    if not folder_path:
        json_training_set_path = decouple_config("SFT_JSON_TRAINING_SET_PATH")
        sample_folder_path = json_training_set_path
    else:
        sample_folder_path = folder_path
    print(f"sample文件夹路径:{sample_folder_path}")
    if os.path.exists(sample_folder_path):
        print(f"sample文件夹已存在，删除sample文件夹")
        shutil.rmtree(sample_folder_path, ignore_errors=True)
    os.makedirs(sample_folder_path, exist_ok=True)
    print("sample文件夹已创建")


def get_list_from_jsonl(jsonl_path):
    print(f"jsonl文件路径: {jsonl_path}")
    alpaca_list = []
    error_lines = 0
    with open(jsonl_path, encoding="utf-8") as fp:
        for line in fp:
            print(f"正在处理：{line}")
            # try:
            new_line = line.replace("\C", "\\\C")
            line_json = json.loads(new_line)
            # except Exception as e:
            #     print(e)
            #     print("出现异常，跳过该条")
            #     error_lines += 1
            #     continue
            if type(line_json) == list:
                instruction = line_json[0]["prompt"]
                output_str = line_json[0]["response"][0][0]
            else:
                instruction = line_json["prompt"]
                output_str = line_json["response"][0]
            if instruction and output_str:
                alpaca_list.append({
                    "instruction": instruction,
                    "input": "",
                    "output": output_str
                })
            else:
                print("instruction或output_str为空，跳过处理")
                print(f"instruction={instruction}, output_str={output_str}")
        print(f"处理完毕 一共有{error_lines}条异常")
    return alpaca_list

def generate_all():
    recreate_sample_folder()
    jsonl_folder_path = decouple_config("SFT_JSONL_TRAINING_SET_PATH")
    json_path = decouple_config("SFT_JSON_TRAINING_SET_PATH")
    alpaca_list = []
    for filename in os.listdir(jsonl_folder_path):
        if filename.endswith(".jsonl"):
            print(f"正在处理{filename}")
            jsonl_path = os.path.join(jsonl_folder_path, filename)
            single_list = get_list_from_jsonl(jsonl_path)
            alpaca_list.extend(single_list)
        else:
            print(f"{filename}不是jsonl文件，跳过处理该文件")
    print("jsonl文件处理完毕")
    training_set_size = int(len(alpaca_list) * 0.9)
    print(f"样本数量一共：{len(alpaca_list)}")
    print(f"训练集数量={training_set_size}, 测试集数量={len(alpaca_list) - training_set_size}")

    # 随机抽取90%的元素作为训练集
    training_set = random.sample(alpaca_list, training_set_size)

    # 剩下的10%作为验证集
    validating_set = [element for element in alpaca_list if element not in training_set]

    training_set_path = os.path.join(json_path, "training_set.json")
    validating_set_path = os.path.join(json_path, "validating_set.json")

    with open(training_set_path, encoding="utf-8", mode="w") as fp:
        json.dump(training_set, fp, ensure_ascii=False)
    
    with open(validating_set_path, encoding="utf-8", mode="w") as fp:
        json.dump(validating_set, fp, ensure_ascii=False)


if __name__ == "__main__":
    generate_all()