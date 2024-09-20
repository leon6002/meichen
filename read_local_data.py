import json
def read_json():
    files = ['stiffness_variables.json', 'main_variables.json', 'cdc_variables.json', 'main_warnings.json', 'ui_control.json', 'test.json']
    merged_data = {}
    for filename in files:
        with open('new_'+filename, 'r', encoding='utf-8') as f:
            file_data = json.load(f)
            merged_data.update(file_data)
    return merged_data


def save_merged():
    data = read_json()
    with open('merged_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("新的JSON文件已保存")

if __name__ == "__main__":
    save_merged()