import os
import json
from openai import OpenAI

client = OpenAI(
    base_url="https://api.xiaomimimo.com/v1",
    api_key=os.environ.get("MIMO_API_KEY")
)

def evaluate_milestone(child_age_months: int, recent_events: list) -> dict:
    """
    综合近期事件列表，进行长链推理，判断当前里程碑达成情况。
    recent_events: 例如 ["会独立走几步", "会说爸爸、妈妈", "能模仿拍手"]
    """
    system_prompt = f"""
    你是一位儿童发育专家。孩子当前{child_age_months}个月大，以下是最近的技能表现：
    {json.dumps(recent_events, ensure_ascii=False)}
    
    请根据丹佛发育筛查量表（DDST）和CDC里程碑清单进行推理，输出JSON：
    {{
        "domain": "运动 / 语言 / 社交 / 认知",
        "current_milestone": "当前正处于哪个里程碑阶段，例如'独站片刻'",
        "achieved": true/false,
        "next_milestone": "下一个可期待的里程碑",
        "suggested_activities": ["推荐1-2个促进发展的亲子活动"]
    }}
    只返回JSON。
    """

    try:
        response = client.chat.completions.create(
            model="mimo-v2.5-pro",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "请分析以上信息。"}
            ],
            temperature=0.2,
            max_tokens=500
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        return {"error": str(e)}
