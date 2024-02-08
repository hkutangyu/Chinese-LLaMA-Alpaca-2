import os
from decouple import config as decouple_config
import json
import random

def generate_longhu():
    jsonl_path = decouple_config("JSONL_PATH")
    print(f"jsonl文件路径: {jsonl_path}")
    alpaca_list = []
    with open(jsonl_path, encoding="utf-8") as fp:
        for line in fp:
            print(f"正在处理：{line}")
            line_json = json.loads(line)
            instruction = line_json[0]["prompt"]
            output_str = line_json[0]["response"][0][0]
            if instruction and output_str:
                alpaca_list.append({
                    "instruction": instruction,
                    "input": "",
                    "output": output_str
                })
            else:
                print("instruction或output_str为空，跳过处理")
                print(f"instruction={instruction}, output_str={output_str}")
            print("处理完毕")

    training_set_size = int(len(alpaca_list) * 0.9)

    print(f"样本数量一共：{len(alpaca_list)}")
    print(f"训练集数量={training_set_size}, 测试集数量={len(alpaca_list) - training_set_size}")

    # 随机抽取90%的元素作为训练集
    training_set = random.sample(alpaca_list, training_set_size)

    # 剩下的10%作为验证集
    validating_set = [element for element in alpaca_list if element not in training_set]

    training_set_path = decouple_config("TRAINING_SET_PATH")
    validating_set_path = decouple_config("VALIDATING_SET_PATH")

    with open(training_set_path, encoding="utf-8", mode="w") as fp:
        json.dump(training_set, fp)
    
    with open(validating_set_path, encoding="utf-8", mode="w") as fp:
        json.dump(validating_set, fp)

def generate_od_news():
    od_jsonl_path = decouple_config("OD_JSONL_PATH")
    print(f"od jsonl文件路径: {od_jsonl_path}")
    alpaca_list = []
    with open(od_jsonl_path, encoding="utf-8") as fp:
        for index, line in enumerate(fp):
            print(f"正在处理第{index}行")
            line_json = json.loads(line)
            tmp_instruction = line_json[0]["prompt"]
            output_str = line_json[0]["response"][0][0]
            if tmp_instruction and output_str:
                instruction = tmp_instruction.replace("\n生成文章如下:", "")
                alpaca_list.append({
                    "instruction": instruction,
                    "input": "",
                    "output": output_str
                })
            else:
                print("instruction或output_str为空，跳过处理")
                print(f"instruction={tmp_instruction}, output_str={output_str}")
    news_jsonl_path = decouple_config("NEWS_JSONL_PATH")
    print(f"news jsonl文件路径: {news_jsonl_path}")
    with open(news_jsonl_path, encoding="utf-8") as fp:
        for index, line in enumerate(fp):
            print(f"正在处理第{index}行")
            line_json = json.loads(line)
            tmp_instruction = line_json[0]["prompt"]
            output_str = line_json[0]["response"][0][0]
            if tmp_instruction and output_str:
                instruction = tmp_instruction.replace("\n生成文章如下:", "").replace("文章", "新闻文章")
                print(instruction)
                alpaca_list.append({
                    "instruction": instruction,
                    "input": "",
                    "output": output_str
                })
            else:
                print("instruction或output_str为空，跳过处理")
                print(f"instruction={tmp_instruction}, output_str={output_str}")
    
    training_set_size = int(len(alpaca_list) * 0.9)

    print(f"样本数量一共：{len(alpaca_list)}")
    print(f"训练集数量={training_set_size}, 测试集数量={len(alpaca_list) - training_set_size}")

    # 随机抽取90%的元素作为训练集
    training_set = random.sample(alpaca_list, training_set_size)

    # 剩下的10%作为验证集
    validating_set = [element for element in alpaca_list if element not in training_set]

    training_set_path = decouple_config("TRAINING_SET_PATH")
    validating_set_path = decouple_config("VALIDATING_SET_PATH")

    with open(training_set_path, encoding="utf-8", mode="w") as fp:
        json.dump(training_set, fp, ensure_ascii=False)
    
    with open(validating_set_path, encoding="utf-8", mode="w") as fp:
        json.dump(validating_set, fp, ensure_ascii=False)

def main():
    generate_od_news()

if __name__ == "__main__":
    main()