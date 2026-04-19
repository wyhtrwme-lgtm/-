# AI指令机器 - 简易版
import requests

# 你的API配置（可换成你自己的接口）
API_URL = "https://api.example.com/chat"
API_KEY = "your_api_key_here"

def ai_command(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "general",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(API_URL, json=headers, data=data)
        result = response.json()
        return result.get("content", "没有返回内容")
    except Exception as e:
        return f"出错了: {str(e)}"

if __name__ == "__main__":
    print("=== AI指令机器已启动 ===")
    print("输入 'exit' 退出\n")
    
    while True:
        user_input = input("请输入指令：")
        if user_input.lower() == "exit":
            print("退出成功")
            break
        
        reply = ai_command(user_input)
        print("\nAI回复：", reply)
        print("-" * 40)
