# openTCK

[TOC]



## 这是什么

TCK是风靡于合肥一中的拍手游戏，开发者将其电子化方便联机

## 安装和配置

由于菜单还没有得到完善，开发版需要用户手动去执行python脚本。在这之前你还需要安装所有的依赖

### 下载

进入dev分支[scarletborder/openTCK at dev (github.com)](https://github.com/scarletborder/openTCK/tree/dev)下载源代码，解压到文件夹中。

![image-20240713175422337](./assets/image-20240713175422337.png)

### 安装依赖

在目录`opentck-dev`下执行`pip install -r requirements.txt`安装所有依赖的包

### 配置文件

在`.\src\constant\config\config.toml`是唯一的配置文件，你可以在其中设置用户名和将要开放或者连接的主机和端口号。

```toml
[player_info]
# Username which will be displayed in lobby
player_name = "Anonymous"

[address]
# For host mode, the IP and port which will be boardcastd.
# For client mode, the IP and port which will be connected to.
host_ip = "127.0.0.1"
port = 47989

```



### 服务端

在目录`opentck-dev`下执行`python .\test\3-gamelink_host.py`即可开启服务端。

### 客户端

在目录`opentck-dev`下执行`python .\test\4-gamelink_client.py`开启客户端。

#### 客户端退出

目前退出功能还没有完善，客户端在退出时，需要先输入菜单命令`exit`离开大厅，再手动退出python进程。

## 如何去玩

打开软件后，如果配置正确成功开启服务端或者连接后，你的界面中会弹出一个大厅列表，这个列表列举出了所有大厅内的玩家。

### 菜单命令

在任何时候你可以输入`!聊天信息`进行聊天，输入`help`查看菜单命令帮助。

### 战斗使用技能

当服务端输入`start`菜单命令后，游戏会开始，每个玩家的终端里都会提示可以输入技能，此时你可以按照`{技能名拼音|技能ID} [一系列参数]`使用技能，使用技能后你无法再次使用技能，直到所有玩家使用技能后进行结算的下一回合之后，你才可以再一次使用技能。

你可以使用菜单命令`query {技能名拼音|技能ID}`查询技能描述，使用菜单命令`skills`查询所有技能的名字，拼音，ID。

## 目前的缺点

### 游戏胜利判定

目前还没有制作游戏胜利判定，死亡的玩家可以每回合使用sleep技能(id为0)跳过回合

### 反作弊

作为一款PVP游戏，本软件目前没有任何反作弊功能也没有任何验证功能，请谨慎提供你的IP地址和选择联机伙伴。