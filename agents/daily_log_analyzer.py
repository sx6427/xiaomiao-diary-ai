import os
import json
from openai import OpenAI

client = OpenAI(
    base_url="https://api.xiaomimimo.com/v1",
    api_key=os.environ.get("MIMO_API_KEY")
)

def analyze_daily_log(observation_text: str) -> dict:
    """
    分析家长输入的自由文本，提取结构化育儿事件。
    返回：{'type', 'summary', 'keywords', 'mood'}
    """
    system_prompt = """
    你是一个专业的育儿观察助手。根据家长提供的日常记录，提取以下信息并以JSON返回：
    {
        "type": "事件类别，如：饮食、睡眠、语言、运动、健康、社交",
        "summary": "用一句话概括事件，例如'宝宝第一次独立站了3秒'",
        "keywords": ["关键词1", "关键词2"],
        "mood": "宝宝当时的情绪，如开心、平静、哭闹"
    }
    只返回JSON，不要有任何额外文字。
    """

    try:
        response = client.chat.completions.create(
            model="mimo-v2.5-pro",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": observation_text}
            ],
            temperature=0.1,
            max_tokens=300
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        return {"error": str(e)}
