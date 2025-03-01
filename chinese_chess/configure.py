import os
from json import dump, load

# 检查文件是否存在，如果不存在则创建并初始化为空字典
def ensure_file_exists(filename: str) -> dict:
    if not os.path.exists(filename):
        with open(filename, 'w', encoding='utf-8') as file:
            dump({}, file, indent=4)
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            if filename == 'config.json':
                data = load(file)
            elif filename == 'statistic.json':
                data = load(file);
    except (IOError, json.JSONDecodeError):
        # 如果文件读取失败（例如，不是有效的JSON），则创建一个新的空字典
        data = {}
    # 检查并添加缺失的项
    if filename == 'config.json':
        defaults = {
            'auto_scale': True,
            'scale': 1,
            'virtual': True,
            'level': 4,
            'peace': 60,
            'algo': 0,
        }
    elif filename == 'statistic.json':
        defaults = {
            'Launch': 0,
            'Play': 0,
            'First': 0,
            'Time': 0,
            'LAN': 0,
            'LOCAL': 0,
            'COMPUTER': 0,
            'END': 0,
            'TEST': 0,
            'Win': 0,
            'Lose': 0,
            'Peace': 0,
            'Eat': 0,
            'Move': 0,
            'Revoke': 0,
            'Recovery': 0,
            'Warn': 0,
        }
    else:
        raise ValueError("Unsupported filename")
 
    for key, value in defaults.items():
        if key not in data:
            data[key] = value
 
    return data


# 加载配置文件
config_filename = 'config.json'
config = ensure_file_exists(config_filename)

# 修改配置文件的函数
def configure(**kw) -> None:
    global config
    config.update(**kw)
    with open(config_filename, 'w', encoding='utf-8') as file:
        dump(config, file, indent=4)

# 加载统计数据文件
statistic_filename = 'statistic.json'
statistic_data = ensure_file_exists(statistic_filename)

# 修改统计数据的函数
def statistic(**kw) -> None:
    global statistic_data
    for key, value in kw.items():
        if key in statistic_data:
            statistic_data[key] += value
        else:
            statistic_data[key] = value
    with open(statistic_filename, 'w', encoding='utf-8') as file:
        dump(statistic_data, file, indent=4)