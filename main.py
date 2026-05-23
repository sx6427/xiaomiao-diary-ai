"""
小苗成长日记 - 主演示入口
展示全部AI Agent协作流程
"""
from agents.daily_log_analyzer import analyze_daily_log
from agents.health_monitor import check_health_status
from agents.milestone_engine import evaluate_milestone
from memory.rag_query import add_memory, query_memory

def main():
    print("=" * 50)
    print("🌱 小苗成长日记 - AI育儿助手演示")
    print("=" * 50)

    # 1. 日常记录分析
    log = "下午带宝宝在客厅玩，他突然松开扶着沙发的手，独立站了有3秒钟，然后特别开心地回头看我。"
    print(f"\n📝 原始记录：{log}")
    analysis = analyze_daily_log(log)
    print(f"✅ 分析结果：{analysis}")

    # 2. 健康监测
    health_data = {
        "age_months": 18,
        "gender": "boy",
        "height_cm": 82.5,
        "weight_kg": 11.2,
        "sleep_hours": 10.5,
        "meals_today": "早餐蛋羹+米糊，午餐碎肉粥，晚餐蔬菜面，有水果加餐"
    }
    print(f"\n🏥 健康数据：{health_data}")
    health_report = check_health_status(health_data)
    print(f"🩺 健康报告：{health_report}")

    # 3. 里程碑推理
    events = ["能独站3秒", "会叫爸爸妈妈", "可以模仿拍手", "喜欢躲猫猫"]
    print(f"\n🧠 近期技能表现：{events}")
    milestone = evaluate_milestone(18, events)
    print(f"🎯 里程碑推理：{milestone}")

    # 4. RAG记忆问答（演示存储和查询）
    print("\n💾 存储一些成长记忆...")
    add_memory("demo1", "1岁半，第一次自己用勺子吃饭，虽然洒了很多。", {"date": "2025-06-10"})
    add_memory("demo2", "昨天去公园，自己爬上了小滑梯的台阶。", {"date": "2025-06-15"})

    question = "宝宝什么时候开始自己吃饭的？"
    print(f"❓ 提问：{question}")
    answers = query_memory(question)
    for i, ans in enumerate(answers, 1):
        print(f"   {i}. {ans['content']} (相关度: {ans['relevance']:.2f})")

    print("\n🎉 演示结束！")

if __name__ == "__main__":
    main()
