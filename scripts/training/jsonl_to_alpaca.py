import os
from decouple import config as decouple_config
import json
import random
import shutil
import pypandoc

def recreate_sample_folder(folder_path=""):
    if not folder_path:
        training_set_path = decouple_config("TRAINING_SET_PATH")
        sample_folder_path = os.path.dirname(training_set_path)
    else:
        sample_folder_path = folder_path
    print(f"sample文件夹路径:{sample_folder_path}")
    if os.path.exists(sample_folder_path):
        print(f"sample文件夹已存在，删除sample文件夹")
        shutil.rmtree(sample_folder_path, ignore_errors=True)
    os.makedirs(sample_folder_path, exist_ok=True)
    print("sample文件夹已创建")

def generate_longhu():
    recreate_sample_folder()
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
                    "instruction": instruction.replace("请把以下内容进行改写，", "请改写下面的内容：").replace("\n", "").replace("改写后内容如下:", ""),
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
        json.dump(training_set, fp, ensure_ascii=False)
    
    with open(validating_set_path, encoding="utf-8", mode="w") as fp:
        json.dump(validating_set, fp, ensure_ascii=False)

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

def generate_pt_txt():
    od_jsonl_path = decouple_config("OD_JSONL_PATH")
    print(f"od jsonl文件路径: {od_jsonl_path}")
    pt_txt_list = []
    with open(od_jsonl_path, encoding="utf-8") as fp:
        for index, line in enumerate(fp):
            print(f"正在处理第{index}行")
            line_json = json.loads(line)
            tmp_instruction = line_json[0]["prompt"]
            output_str = line_json[0]["response"][0][0]
            if tmp_instruction and output_str:
                pt_txt_list.append(output_str)
            else:
                print("instruction或output_str为空，跳过处理")
                print(f"instruction={tmp_instruction}, output_str={output_str}")

    print(f"样本数量一共：{len(pt_txt_list)}")
    # 重新创建文件夹
    pt_samples_path = decouple_config("PT_SAMPLES_PATH")
    recreate_sample_folder(folder_path=pt_samples_path)
    # 遍历列表，生成一批txt
    for index, pt_txt in enumerate(pt_txt_list):
        txt_path = os.path.join(pt_samples_path, f"{index}.txt")
        with open(txt_path, mode="w", encoding="utf-8") as fp:
            fp.write(pt_txt)
        print(f"{txt_path}生成完毕")
    
def docx_filter():
    dir_path = decouple_config("DATASET_DIR")
    flat_doc_path = decouple_config("FLAT_DOC_PATH")
    move_list = []
    for home, dirs, files in os.walk(dir_path):
        for filename in files:
            filepath = os.path.join(home, filename)
            if not os.path.isdir(filepath) and '.docx' in filename:
                move_list.append(filepath)
    move_list_len = len(move_list)
    print(f"一共有{move_list_len}个文件满足要求")
    for i, filepath in enumerate(move_list):
        dst_path = os.path.join(flat_doc_path, os.path.basename(filepath))
        if os.path.exists(dst_path):
            print(f"{dst_path}已存在")
            continue
        shutil.copy(filepath, dst_path)
        print(f"{i+1}/{move_list_len} 处理完毕")

def docx_to_txt():
    flat_doc_path = decouple_config("FLAT_DOC_PATH")
    for home, dirs, files in os.walk(flat_doc_path):
        for filename in files:
            filepath = os.path.join(home, filename)
            if not os.path.isdir(filepath) and '.docx' in filename:
                docxfilename = '/mnt/sq_datasets/flat_documents/刘积龙：2019年乡人大主席述责述纪述廉述法报告.docx'
    # output = pypandoc.convert_file(docxFilename, 'plain', outputfile="/mnt/sq_datasets/flat_txt/刘积龙：2019年乡人大主席述责述纪述廉述法报告.txt")

def main():
    # generate_od_news()
    # generate_longhu()
    # generate_pt_txt()
    docx_filter()

if __name__ == "__main__":
    main()