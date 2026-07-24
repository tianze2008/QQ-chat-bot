# QQ-chat-bot
QQ聊天机器人(可自由修改人设)

使用方法
1.下载NapCat文件夹 qqbot.py 并将其放入无特殊字符路径下
2.运行NapCat文件夹中的launcher.bat
3.powershell中出现诸如“[NapCat] [WebUi] WebUi User Panel Url: http://127.0.0.1:6099/webui?token=.....”的命令行，在浏览器中打开此链接
4.登录QQ
5.在左侧点击网络配置 新建 Websocket客户端 名称自填 URL改为ws://localhost:8765 启用此配置
6.编辑qqbot.py文件（看注释）
  6.0下载python依赖库
  6.1填写机器人qq号
  6.2前往智谱ai官网获取api
  6.3编辑机器人人设
7.使用cd命令在终端中进入在qqbot.py所在路径，运行py文件(py qqbot.py)
大功告成！
