import asyncio
import json
import websockets
from zhipuai import ZhipuAI

# ===== 在这里填入你的信息 =====
BOT_QQ = ""        # 填写你的机器人QQ号，比如 "123456789"
API_KEY = ""      # 填写你的智谱AI API Key
# =============================

# 初始化智谱AI客户端
client = ZhipuAI(api_key=API_KEY)

async def handle_message(websocket):
    """处理收到的消息（由websockets库调用）"""
    async for message in websocket:
        try:
            data = json.loads(message)
            # 只处理群聊消息
            if data.get("post_type") == "message" and data.get("message_type") == "group":
                await process_group_message(websocket, data)
        except Exception as e:
            print(f"处理消息时出错: {e}")

async def process_group_message(websocket, data):
    """处理群消息的核心逻辑"""
    sender_id = str(data.get("sender", {}).get("user_id"))
    # 忽略机器人自己发的消息，防止死循环
    if sender_id == BOT_QQ:
        return

    group_id = data.get("group_id")
    raw_message = data.get("raw_message", "")
    print(f"收到群 {group_id} 消息: {raw_message}")

    # --- 触发条件：如果有人 @ 了机器人 ---
    if f"[CQ:at,qq={BOT_QQ}]" in raw_message:
        # 调用AI大脑获取回复
        reply = await get_ai_reply(raw_message)
        await send_group_message(websocket, group_id, reply)

async def get_ai_reply(prompt):
    """调用智谱AI的免费模型获取回复"""
    try:
        response = client.chat.completions.create(
            model="glm-4-flash",  # 使用永久免费的模型
            messages=[
                {"role": "system", "content": "你是一个有趣的聊天机器人，擅长与人类进行自然对话。"}, #立机器人的人设，可自由修改
                {"role": "user", "content": prompt}
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用智谱API失败: {e}")
        return "抱歉，我遇到了一点小问题。"

async def send_group_message(websocket, group_id, message):
    """发送群消息"""
    send_msg = {
        "action": "send_group_msg",
        "params": {
            "group_id": group_id,
            "message": message
        }
    }
    await websocket.send(json.dumps(send_msg))

async def main():
    """启动WebSocket服务，监听8765端口"""
    async with websockets.serve(handle_message, "0.0.0.0", 8765):
        print("机器人已启动，等待消息...")
        await asyncio.Future()  # 保持服务运行

if __name__ == "__main__":
    asyncio.run(main())