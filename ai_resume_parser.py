"""
AI简历解析器 - 使用大模型API自动提取简历信息
展示AI应用能力
"""

import json

def build_prompt(resume_text):
    """构建提示词模板"""
    return f"""
从以下简历文本中提取结构化信息，以JSON格式返回：
字段: 姓名(name), 教育背景(education), 技能(skills), 项目经验(projects), 工作经历(experience)

简历文本:
{resume_text}

按JSON格式返回：
{{
    "name": "",
    "education": "",
    "skills": [],
    "projects": [],
    "experience": []
}}
"""

def parse_resume_with_llm(resume_text, api_key=None):
    """
    调用大模型API解析简历
    你可以替换为任何大模型的API
    """
    prompt = build_prompt(resume_text)
    
    # 这里以调用API为例，实际使用时替换为真实API调用
    # 例如：OpenAI、Claude、文心一言等
    
    print("=" * 50)
    print("输入简历文本:")
    print("-" * 50)
    print(resume_text)
    print("-" * 50)
    print("构建的Prompt:")
    print(prompt)
    print("-" * 50)
    print("→ 只需接入真实LLM API即可运行")
    print("  支持: ChatGPT / Claude / 文心一言 / 通义千问")
    print("=" * 50)
    
    return prompt

# 示例：实战中的简历解析
if __name__ == "__main__":
    sample_resume = """
    张三
    教育背景：XX大学 大数据管理与应用 本科 大一
    技能：Python, SQL, Excel, AI Prompt
    项目：泰坦尼克号数据分析
    """
    
    prompt = parse_resume_with_llm(sample_resume)
    
    print("\n实战应用场景:")
    print("- HR批量筛选简历: 自动提取关键信息")
    print("- 简历库管理: 结构化存储")
    print("- 技能匹配: 自动对比JD要求")
