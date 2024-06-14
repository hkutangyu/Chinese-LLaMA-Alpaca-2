import os

def main():
    root_folder = "/mnt/sq_datasets/flat_txt"
    filepath_list = []
    final_content = ""
    print("读取文件列表")
    for filename in os.listdir(root_folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(root_folder, filename)
            filepath_list.append(filepath)
    print(f"一共要处理{len(filepath_list)}个文件")
    for i, filepath in enumerate(filepath_list):
        with open(filepath, mode="r", encoding="utf-8") as f:
            final_content += f.read()
            final_content += "\n"
        print(f"已处理{i+1}/{len(filepath_list)} filepath={filepath}")
    
    print("final_content生成完毕，开始写入文件")
    with open("flat_content.txt", mode="w", encoding="utf-8") as f:
        f.write(final_content)
    print("处理完毕！")

if __name__ == "__main__":
    main()