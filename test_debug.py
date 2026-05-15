import json
import os
import pandas as pd

# 1. 模拟一个“坏掉的”大模型输出 (故意少了一个逗号)
mock_result = '{"sentiment": "positive" "trend": "rising"}' 
GAME_NAME = "测试游戏"

# --- 你的保存逻辑开始 ---
raw_final_string = str(mock_result)
os.makedirs("outputs/audit", exist_ok=True)
os.makedirs("outputs/reports", exist_ok=True)

# 强制保存原始输出
with open("outputs/raw_output.txt", "w", encoding="utf-8") as f:
    f.write(raw_final_string)

try:
    # 模拟解析
    parsed_result = json.loads(raw_final_string)
    print("✅ 解析成功（说明数据没坏）")
except Exception as e:
    print(f"❌ 捕获到预期错误: {e}")
    
    # 验证 Badcase 写入逻辑
    badcase_path = "outputs/audit/badcase.json"
    current_badcases = []
    if os.path.exists(badcase_path):
        try:
            with open(badcase_path, "r", encoding="utf-8") as f:
                current_badcases = json.load(f)
        except:
            current_badcases = []

    current_badcases.append({
        "error": str(e),
        "game": GAME_NAME,
        "time": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
        "raw_output": raw_final_string
    })

    with open(badcase_path, "w", encoding="utf-8") as f:
        json.dump(current_badcases, f, ensure_ascii=False, indent=2)
    print("⚠️ Badcase 记录成功！请去 outputs/audit/ 检查。")
# --- 你的保存逻辑结束 ---