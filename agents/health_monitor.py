import os
import json
from openai import OpenAI

client = OpenAI(
    base_url="https://api.xiaomimimo.com/v1",
    api_key=os.environ.get("MIMO_API_KEY")
)

def check_health_status(child_data: dict) -> dict:
    """
    根据输入的健康数据（身高、体重、睡眠时长、饮食情况），
    对照儿童生长标准，输出评价与预警。
    child_data 示例：
    {
        "age_months": 18,
        "gender": "boy",
        "height_cm": 82.5,
        "weight_kg": 11.2,
        "sleep_hours": 10.5,
        "meals_today": "早餐鸡蛋羹+米糊，午餐碎肉粥，晚餐蔬菜面，有加餐水果"
    }
    """
    system_prompt = """
    你是一位儿科健康顾问。基于WHO儿童生长标准（0-5岁），分析输入数据。
    返回JSON：
    {
        "height_evaluation": "正常范围 / 偏高 / 偏低",
        "weight_evaluation": "正常范围 / 偏高 / 偏低",
        "sleep_evaluation": "充足 / 不足 / 过多",
        "diet_balance": "均衡 / 偏食 / 热量不足 / 热量超标",
        "alerts": ["如果有任何偏离标准的情况，请用中文给出预警。无则返回空数组"]
    }
    只返回JSON。
    """

    try:
        response = client.chat.completions.create(
            model="mimo-v2.5-pro",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(child_data, ensure_ascii=False)}
            ],
            temperature=0.0,
            max_tokens=400
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        return {"error": str(e)}
