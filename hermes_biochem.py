import random
import datetime

# 赫尔墨斯指令 - 生化&AI科研专用版
class HermesCommand_BioChem:
    def __init__(self):
        self.name = "赫尔墨斯指令｜生化科研版"
        self.date = datetime.date.today().strftime("%Y-%m-%d")
        self.version = "V1.0"

    # 随机生成生化科研任务
    def generate_task(self):
        tasks = [
            "查阅5篇与小分子药物设计相关的文献，整理核心方法",
            "使用RDKit处理10个分子结构，计算分子量、LogP、氢键供体受体",
            "搭建简单机器学习模型，预测分子水溶性或生物活性",
            "学习GNN图神经网络基础，理解分子结构图表示方法",
            "整理实验数据，使用Python绘制折线图/柱状图进行可视化",
            "学习蛋白结构基础，尝试查看PDB文件并分析结合位点",
            "练习SMILES表达式书写，尝试转换分子结构格式",
            "学习AI辅助逆合成思路，记录3种常见反应路径",
            "整理实验室安全规范，熟悉试剂存放与应急处理",
            "学习数据标准化、归一化处理，为AI模型训练做准备",
            "尝试用公开数据集训练一个简单的分子分类模型",
            "复盘本周实验/学习内容，优化下周科研计划",
            "了解ADMET性质预测，整理影响药物活性的关键因素",
            "学习光谱数据（红外/紫外/核磁）基础处理方法",
            "了解AlphaFold基本原理，尝试查看蛋白折叠结果"
        ]
        return random.choice(tasks)

    # 生成对应建议 + 详细做法
    def generate_suggestion(self, task):
        base_suggest = [
            "先明确目标，再拆分小步骤，避免盲目操作",
            "数据处理前先清洗异常值，保证模型可靠性",
            "文献阅读优先看摘要、图表与结论，提高效率",
            "代码边写边注释，方便后续复盘与复用",
            "实验记录完整保存，便于复现与数据分析",
            "遇到结构问题优先用可视化工具辅助理解",
            "模型效果不佳时，优先检查特征是否合理",
            "保持每日学习节奏，长期积累远胜于突击"
        ]

        # 根据任务类型给专业建议
        if "RDKit" in task or "分子" in task:
            method = "先安装RDKit库 → 读取SMILES → 计算描述符 → 保存CSV → 绘图分析"
        elif "机器学习" in task or "模型" in task:
            method = "数据集加载 → 特征提取 → 划分训练集测试集 → 训练 → 评估指标"
        elif "文献" in task:
            method = "使用知网、Sci-Hub、PubMed检索 → 按年份/期刊筛选 → 做思维导图整理"
        elif "GNN" in task or "图神经网络" in task:
            method = "先学图结构基础 → 理解节点与边 → 学习PyTorch Geometric基础用法"
        elif "蛋白" in task or "PDB" in task:
            method = "下载PDB结构 → 使用PyMOL或可视化工具打开 → 观察活性中心与相互作用"
        elif "数据" in task or "可视化" in task:
            method = "Pandas读数据 → 去除空值 → Matplotlib绘图 → 标注清晰标题与图例"
        else:
            method = "按计划稳步执行，遇到问题及时记录并查找解决方案"

        select_suggest = random.choice(base_suggest)
        return f"【操作步骤】\n{method}\n\n【小建议】\n{select_suggest}"

    # 生化AI方向指导
    def get_aim_guide(self):
        guides = [
            "方向：AI计算化学 → 分子性质预测、反应路径模拟",
            "方向：AI药物发现 → 小分子筛选、ADMET预测、分子生成",
            "方向：生物信息学 → 蛋白序列分析、AlphaFold结构预测",
            "方向：智能材料 → AI辅助催化剂设计、高分子性能预测",
            "方向：光谱AI → 红外/质谱/核磁数据自动分类识别"
        ]
        return random.choice(guides)

    # 启动界面
    def start(self):
        print(f"\n================================")
        print(f"    {self.name} {self.version}")
        print(f"    日期：{self.date}")
        print(f"    方向：生物 + 化学 + AI")
        print(f"================================")

        # 任务
        task = self.generate_task()
        print(f"\n📌 今日科研任务：")
        print(f"   {task}")

        # 建议
        print(f"\n💡 执行做法：")
        suggest = self.generate_suggestion(task)
        print(suggest)

        # 方向
        print(f"\n🧬 推荐研究方向：")
        print(f"   {self.get_aim_guide()}")

        print(f"\n=================================")
        print("指令：rerun = 换任务 | exit = 退出")
        print(f"=================================\n")

        # 交互
        while True:
            cmd = input("请输入指令：").strip().lower()
            if cmd == "exit":
                print("\n✅ 赫尔墨斯指令已关闭，继续加油！")
                break
            elif cmd == "rerun":
                print("\n🔄 正在生成新任务...\n")
                self.start()
                break
            else:
                print("\n⚠️  指令错误，请输入 rerun 或 exit\n")

# 运行
if __name__ == "__main__":
    hermes = HermesCommand_BioChem()
    hermes.start()
