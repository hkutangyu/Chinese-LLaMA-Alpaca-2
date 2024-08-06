import os
import json
from decouple import config as decouple_config


dst_folder = "/mnt/sq_datasets/jsonl_all/"
dst_path = os.path.join(dst_folder, "doubao.jsonl")
jsonl_folder_path = decouple_config("SFT_JSONL_TRAINING_SET_PATH")


def get_list_from_jsonl(jsonl_path):
    print(f"jsonl文件路径: {jsonl_path}")
    dst_list = []
    error_lines = 0
    with open(jsonl_path, encoding="utf-8") as fp:
        for line in fp:
            print(f"正在处理：{line}")
            new_line = line.replace("\C", "\\\C")
            line_json = json.loads(new_line)
            
            if type(line_json) == list:
                instruction = line_json[0]["prompt"]
                output_str = line_json[0]["response"][0][0]
            else:
                instruction = line_json["prompt"]
                output_str = line_json["response"][0]
            if instruction and output_str:
                dst_list.append({
                    "messages": [
                      {"role": "user", "content": instruction},
                      {"role": "assistant", "content": output_str}
                    ]
                })
            else:
                print("instruction或output_str为空，跳过处理")
                print(f"instruction={instruction}, output_str={output_str}")
        print(f"处理完毕 一共有{error_lines}条异常")
    return dst_list

if __name__ == "__main__":
    dst_list = []
    print(f"jsonl训练集文件夹：{jsonl_folder_path}")
    for filename in os.listdir(jsonl_folder_path):
        if filename.endswith(".jsonl"):
            print(f"正在处理{filename}")
            jsonl_path = os.path.join(jsonl_folder_path, filename)
            single_list = get_list_from_jsonl(jsonl_path)
            dst_list.extend(single_list)
        else:
            print(f"{filename}不是jsonl文件，跳过处理该文件")
    print("jsonl文件处理完毕")
    # print(dst_list)
    with open(dst_path, mode="w", encoding="utf-8") as fp:
        for line in dst_list:
            fp.write(json.dumps(line, ensure_ascii=False))
            fp.write("\n")
    print(f"结果文件已保存到{dst_path}")