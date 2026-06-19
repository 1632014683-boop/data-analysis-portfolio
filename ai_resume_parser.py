"""
AI简历解析器 - 用大模型API自动提取简历信息
技术栈：Python + LLM API + JSON
"""
import json
import re

class ResumeParser:
    def __init__(self, api_key=None):
        self.api_key = api_key
    
    def extract_text_from_file(self, filepath):
        """读取简历文本文件"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    
    def parse_with_regex(self, text):
        """不用API也能用的正则解析方案"""
        result = {}
        
        lines = text.strip().split('\n')
        result['name'] = lines[0].strip() if lines else ""
        
        email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
        emails = re.findall(email_pattern, text)
        result['email'] = emails[0] if emails else ""
        
        phone_pattern = r'1[3-9]\d{9}'
        phones = re.findall(phone_pattern, text)
        result['phone'] = phones[0] if phones else ""
        
        skill_keywords = ['Python', 'SQL', 'Java', 'Excel', 'Tableau', 
                         'Spark', 'Hadoop', 'MySQL', 'Pandas', 'AI',
                         '机器学习', '数据分析', '深度学习', 'Prompt']
        found_skills = []
        for skill in skill_keywords:
            if skill.lower() in text.lower():
                found_skills.append(skill)
        result['skills'] = found_skills
        
        return result
    
    def build_prompt(self, text):
        return f"""你是一名HR助手。从以下简历文本中提取信息，严格按JSON格式返回：
{{
    "name": "姓名",
    "education": "教育背景",
    "skills": ["技能1", "技能2"],
    "experience": "工作/项目经历",
    "score": 85
}}

简历文本：
{text}
"""

if __name__ == "__main__":
    sample = """张三
    邮箱: zhangsan@email.com
    电话: 13800138000
    教育背景: XX大学 大数据管理与应用 本科 大一
    技能: Python, SQL, Excel, AI Prompt, 数据分析
    项目经验: 泰坦尼克号数据分析项目
    """
    
    parser = ResumeParser()
    result = parser.parse_with_regex(sample)
    
    print("=" * 40)
    print("AI简历解析结果")
    print("=" * 40)
    print(json.dumps(result, ensure_ascii=False, indent=2))
