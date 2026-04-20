import time
import re
from PIL import Image
import pytesseract  # 用于图片文字提取
import requests  # 用于DOI文献检索
from datetime import datetime, timedelta

class HermesResearchAssistant:
    def __init__(self):
        self.documents = []  # 存储添加的文献
        self.timers = {}     # 存储实验计时任务 {实验名称: (启动时间, 时长, 提醒节点)}
        self.current_timer_id = 0  # 计时任务ID
    
    # 1. 文献添加功能
    def add_document(self, input_content, doc_info=None):
        """
        添加文献，支持全文粘贴、图片上传、DOI检索三种方式
        :param input_content: 文献全文/图片路径/DOI号/标题关键词
        :param doc_info: 文献信息（标题、作者、来源），可选
        :return: 文献添加结果及初步解析
        """
        document = {}
        # 方式1：图片上传（提取文字）
        if input_content.endswith(('.png', '.jpg', '.jpeg', '.pdf')):
            try:
                if input_content.endswith('.pdf'):
                    # 简化处理：假设PDF已转换为图片，此处模拟提取文字
                    text = "模拟PDF图片文字提取：实验目的为验证XX方法的有效性，实验步骤如下..."
                else:
                    # 图片文字提取
                    img = Image.open(input_content)
                    text = pytesseract.image_to_string(img, lang='eng+chi_sim')
                document['content'] = text
                document['type'] = self._judge_doc_type(text)
                document['img_source'] = input_content
            except Exception as e:
                return f"文献添加失败：图片处理异常，错误信息：{str(e)}"
        # 方式2：DOI检索
        elif re.match(r'^10\.\d{4,9}/[-._;()/:A-Z0-9]+$', input_content, re.IGNORECASE):
            try:
                # 模拟DOI检索（实际需对接文献数据库API）
                response = requests.get(f"https://api.crossref.org/works/{input_content}")
                if response.status_code == 200:
                    data = response.json()
                    document['title'] = data['message']['title'][0]
                    document['authors'] = [auth['family'] + ' ' + auth['given'] for auth in data['message']['author']]
                    document['content'] = "模拟文献全文：基于上述标题，本文提出了XX创新方法，通过XX实验验证..."
                    document['type'] = self._judge_doc_type(document['content'])
                else:
                    return "DOI检索失败，未找到对应文献"
            except Exception as e:
                return f"DOI检索异常：{str(e)}"
        # 方式3：全文粘贴/标题关键词
        else:
            document['content'] = input_content
            document['type'] = self._judge_doc_type(input_content)
        # 补充文献信息
        if doc_info:
            document.update(doc_info)
        else:
            document['title'] = "未命名文献" if 'title' not in document else document['title']
        # 生成摘要和核心结论（模拟）
        document['abstract'] = self._generate_abstract(document['content'])
        document['core_conclusion'] = self._generate_core_conclusion(document['content'])
        # 加入文献列表
        self.documents.append(document)
        return f"文献添加成功！文献类型：{document['type']}\n摘要：{document['abstract']}"
    
    # 辅助：判断文献类型
    def _judge_doc_type(self, content):
        if any(keyword in content for keyword in ['实验', '实验设计', '实验数据', '实验结论']):
            return "实验类"
        elif any(keyword in content for keyword in ['综述', '总结', '研究进展']):
            return "综述类"
        else:
            return "理论类"
    
    # 辅助：生成文献摘要（模拟）
    def _generate_abstract(self, content):
        if len(content) <= 100:
            return content
        return content[:100] + "..."
    
    # 辅助：生成核心结论（模拟）
    def _generate_core_conclusion(self, content):
        return "模拟核心结论：基于文献内容，得出XX结论，提出XX创新点，为相关研究提供XX参考"
    
    # 2. 文献创新点提取（针对实验类文献）
    def extract_innovation(self, doc_index=0):
        """提取指定文献的创新点，默认提取最新添加的文献"""
        if not self.documents:
            return "暂无添加的文献，请先添加文献"
        doc = self.documents[doc_index]
        if doc['type'] != "实验类":
            return "当前文献非实验类，无实验创新点可提取"
        # 模拟创新点提取（实际需结合NLP解析）
        content = doc['content']
        innovations = []
        if "创新方法" in content:
            innovations.append({"类型": "实验方法创新", "详情": "提出XX创新实验方法，解决传统方法XX不足，优势在于XX", "位置": "文献第1章节"})
        if "新参数" in content:
            innovations.append({"类型": "技术创新", "详情": "优化实验参数XX，提升实验重复性和准确性，应用价值在于XX", "位置": "文献实验步骤部分"})
        if not innovations:
            return "未提取到明确创新点，可能为常规实验研究"
        # 格式化输出
        result = "文献创新点提取结果：\n"
        for i, innov in enumerate(innovations, 1):
            result += f"{i}. 类型：{innov['类型']}\n   详情：{innov['详情']}\n   对应位置：{innov['位置']}\n"
        return result
    
    # 3. 实验路线制定（针对实验类文献）
    def make_experiment_route(self, doc_index=0, current_conditions=None):
        """制定实验路线，结合文献内容和现有实验条件"""
        if not self.documents:
            return "暂无添加的文献，请先添加实验类文献"
        doc = self.documents[doc_index]
        if doc['type'] != "实验类":
            return "当前文献非实验类，无法制定实验路线"
        # 模拟实验路线制定（实际需解析文献实验步骤）
        route = f"基于文献《{doc['title']}》制定实验路线：\n"
        route += "一、实验核心目标：验证XX假设，达成XX实验效果（贴合文献核心需求）\n"
        route += "二、实验步骤：\n"
        route += "1. 样品制备：按照文献标准，准备XX样品，控制样品质量XX，注意事项：避免样品污染\n"
        route += "2. 实验装置调试：启动XX仪器，校准参数XX，确保仪器正常运行\n"
        route += "3. 实验操作：按顺序执行XX操作，控制温度XX℃、湿度XX%，每步停留XX分钟\n"
        route += "4. 数据采集：记录实验过程中的XX数据，重复实验3次，确保数据可靠性\n"
        route += "5. 实验收尾：关闭仪器，整理样品，处理实验废弃物\n"
        route += "三、误差控制：避免XX误差（如仪器误差、操作误差），可通过XX方法校准\n"
        # 结合现有条件调整
        if current_conditions:
            route += f"\n四、路线调整建议（结合现有条件）：\n{current_conditions}"
        return route
    
    # 4. 文献图片解释（针对含图片的文献）
    def explain_document_image(self, doc_index=0):
        """解释指定文献的图片内容"""
        if not self.documents:
            return "暂无添加的文献，请先添加文献"
        doc = self.documents[doc_index]
        if 'img_source' not in doc:
            return "当前文献无图片，无法进行图片解释"
        # 模拟图片解释（实际需结合图片识别和文献上下文）
        return f"文献图片解释：\n图片来源：{doc['img_source']}\n图片类型：实验装置图\n核心内容：展示了XX实验的装置结构，包括XX部件（标注1）、XX部件（标注2），该装置用于XX实验步骤，与文献中XX实验结论相关，关键参数标注为XX"
    
    # 5. 科研器材操作指导
    def equipment_guide(self, equipment_name):
        """提供指定器材的操作指导"""
        equipment_guide_dict = {
            "离心机": "【离心机操作指导】\n1. 操作步骤：\n   ① 检查离心机电源，确认仪器正常；\n   ② 将样品放入离心管，平衡重量（误差不超过0.1g）；\n   ③ 将离心管放入转子，拧紧盖子；\n   ④ 设置参数（转速XX rpm、时间XX分钟），启动仪器；\n   ⑤ 实验结束后，待转子停止转动再取出样品。\n2. 注意事项：禁止超速运行，禁止开盖运行，定期校准转子。\n3. 常见问题：转速不准→校准仪器；样品泄漏→检查离心管密封性。",
            "PCR仪": "【PCR仪操作指导】\n1. 操作步骤：\n   ① 开机预热，等待仪器温度稳定至95℃；\n   ② 配制PCR反应体系，按比例加入模板、引物、酶等试剂，混匀后离心；\n   ③ 将反应管放入PCR仪样品槽，设置程序（预变性95℃5min，变性95℃30s，退火XX℃30s，延伸72℃1min，循环35次，终延伸72℃10min）；\n   ④ 启动程序，等待反应完成。\n2. 注意事项：试剂需冰浴保存，反应管盖紧防止蒸发，实验后清洁样品槽。\n3. 常见问题：无扩增产物→检查引物特异性、酶活性；条带模糊→调整退火温度。",
            "电子天平": "【电子天平操作指导】\n1. 操作步骤：\n   ① 开机校准，等待天平显示稳定；\n   ② 放置称量纸，归零；\n   ③ 缓慢加入样品，待读数稳定后记录数据；\n   ④ 称量完成，取出样品，清理称量盘。\n2. 注意事项：保持天平水平，避免震动和气流干扰，定期校准。\n3. 常见问题：读数漂移→检查环境是否稳定；无法归零→清洁称量盘、重新校准。"
        }
        # 若查询的器材不在预设字典中，返回通用指导
        if equipment_name not in equipment_guide_dict:
            return f"【{equipment_name}操作指导】\n1. 操作步骤：\n   ① 检查仪器外观及电源，确认无异常；\n   ② 按照仪器说明书，完成开机校准；\n   ③ 进行样品制备/仪器调试，按标准步骤操作；\n   ④ 实验结束，关闭仪器，做好维护。\n2. 注意事项：严格遵循仪器说明书，避免违规操作，定期维护保养。\n3. 常见问题：可参考仪器说明书或联系技术人员排查。"
        return equipment_guide_dict[equipment_name]
    
    # 6. 实验计时功能
    def start_timer(self, experiment_name, duration_min):
        """启动实验计时，duration_min为计时时长（分钟）"""
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=duration_min)
        self.current_timer_id += 1
        timer_id = self.current_timer_id
        self.timers[timer_id] = {
            "experiment_name": experiment_name,
            "start_time": start_time,
            "duration": duration_min,
            "end_time": end_time,
            "is_running": True
        }
        # 模拟提醒（实际需结合多线程/定时任务）
        print(f"计时启动！实验：{experiment_name}，时长：{duration_min}分钟，启动时间：{start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        return f"计时启动成功！计时ID：{timer_id}，实验：{experiment_name}，预计结束时间：{end_time.strftime('%Y-%m-%d %H:%M:%S')}"
    
    def check_timer(self, timer_id=None):
        """查询计时状态，默认查询所有计时"""
        if not self.timers:
            return "暂无正在进行的计时任务"
        result = "当前计时任务状态：\n"
        for tid, timer in self.timers.items():
            if timer_id is not None and tid != timer_id:
                continue
            elapsed = (datetime.now() - timer['start_time']).total_seconds() / 60
            remaining = max(0, timer['duration'] - elapsed)
            status = "运行中" if timer['is_running'] else "已结束"
            result += f"计时ID：{tid}，实验：{timer['experiment_name']}，状态：{status}，已运行：{round(elapsed, 1)}分钟，剩余：{round(remaining, 1)}分钟\n"
        return result
    
    # 7. 通用操作解答
    def answer_question(self, question):
        """解答使用者各类疑问"""
        # 模拟疑问匹配（实际需结合NLP语义理解）
        if any(keyword in question for keyword in ['文献添加失败', '添加文献报错']):
            return "文献添加失败解决方案：\n1. 若为图片上传：检查图片清晰度，确保为PNG/JPG/PDF格式；\n2. 若为DOI检索：确认DOI号格式正确，检查网络连接；\n3. 若为全文粘贴：确保粘贴内容完整，无特殊字符干扰。"
        elif any(keyword in question for keyword in ['实验路线调整', '修改实验步骤']):
            return "实验路线调整建议：\n1. 明确调整需求（如缩短周期、替换器材）；\n2. 结合文献核心实验原理，保留关键步骤；\n3. 调整后需补充误差控制方案，确保实验重复性。"
        elif any(keyword in question for keyword in ['计时错误', '计时不准']):
            return "计时错误解决方案：\n1. 检查计时启动时的时长设置是否正确；\n2. 确认系统时间无误；\n3. 若需重新计时，可停止当前计时，重新启动。"
        else:
            return f"已收到您的疑问：{question}\n解答：结合科研规范，建议您先确认相关操作步骤（如文献添加、器材操作），若仍有疑问，可补充具体细节，将为您提供更精准的解决方案。"

# 测试代码（可直接运行）
if __name__ == "__main__":
    hermes = HermesResearchAssistant()
    # 测试文献添加（全文粘贴）
    print(hermes.add_document("实验目的：验证新型催化剂的催化效率，实验步骤：1. 制备催化剂样品；2. 搭建反应装置；3. 进行催化反应，记录数据；4. 分析实验结果。", {"title": "新型催化剂催化效率实验研究", "authors": "张三", "source": "XX期刊"}))
    # 测试创新点提取
    print(hermes.extract_innovation())
    # 测试实验路线制定
    print(hermes.make_experiment_route(current_conditions="现有器材无XX仪器，可替换为XX仪器，调整反应时间至XX分钟"))
    # 测试器材操作指导
    print(hermes.equipment_guide("离心机"))
    # 测试计时功能
    print(hermes.start_timer("催化反应计时", 30))
    print(hermes.check_timer())
    # 测试疑问解答
    print(hermes.answer_question("文献添加失败怎么办？"))
