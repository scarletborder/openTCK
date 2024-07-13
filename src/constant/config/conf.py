import toml

# 读取 TOML 文件
Cfg = toml.load("./config.toml")

# # 访问 TOML 文件中的数据
# player_name = config["player_info"]["player_name"]
# host_ip = config["address"]["host_ip"]
# port = config["address"]["port"]
