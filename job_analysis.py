"""
招聘数据爬取与分析 - 数据分析实习岗位市场调研
技术栈：Python + 爬虫 + 数据分析 + 可视化
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import json

matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# ========== 内置样本数据（模拟从招聘网站爬取的结果）==========
# 实际使用时替换为真实爬虫数据
sample_jobs = [
    {"title": "数据分析实习生", "company": "字节跳动", "salary": "200-250/天", "city": "北京", "skills": "Python,SQL,Excel,Tableau", "education": "本科", "experience": "在校生"},
    {"title": "数据分析实习生", "company": "阿里巴巴", "salary": "200-300/天", "city": "杭州", "skills": "SQL,Python,Excel,数据可视化", "education": "本科", "experience": "在校生"},
    {"title": "数据分析实习生", "company": "腾讯", "salary": "150-200/天", "city": "深圳", "skills": "SQL,Python,Excel,统计学", "education": "本科", "experience": "在校生"},
    {"title": "数据分析实习生", "company": "美团", "salary": "180-250/天", "city": "北京", "skills": "SQL,Python,Excel,AB测试", "education": "本科", "experience": "在校生"},
    {"title": "数据分析实习生", "company": "京东", "salary": "150-200/天", "city": "北京", "skills": "SQL,Excel,Python,数据清洗", "education": "本科", "experience": "在校生"},
    {"title": "数据分析实习生", "company": "小红书", "salary": "180-220/天", "city": "上海", "skills": "SQL,Python,Excel,业务分析", "education": "本科", "experience": "在校生"},
    {"title": "数据分析实习生", "company": "滴滴", "salary": "200-260/天", "city": "北京", "skills": "SQL,Python,Pandas,数据可视化", "education": "本科", "experience": "在校生"},
    {"title": "数据分析实习生", "company": "快手", "salary": "180-230/天", "city": "北京", "skills": "Python,SQL,Excel,统计学", "education": "本科", "experience": "在校生"},
    {"title": "数据分析实习生", "company": "网易", "salary": "150-200/天", "city": "广州", "skills": "SQL,Excel,Python,数据分析方法", "education": "本科", "experience": "在校生"},
    {"title": "数据分析实习生", "company": "百度", "salary": "200-250/天", "city": "北京", "skills": "SQL,Python,Excel,AB测试,统计学", "education": "本科", "experience": "在校生"},
    {"title": "数据分析实习生", "company": "哔哩哔哩", "salary": "150-200/天", "city": "上海", "skills": "SQL,Python,Excel,用户分析", "education": "本科", "experience": "在校生"},
    {"title": "数据分析实习生", "company": "拼多多", "salary": "200-300/天", "city": "上海", "skills": "Python,SQL,Excel,数据挖掘", "education": "本科", "experience": "在校生"},
    {"title": "数据分析实习生", "company": "华为", "salary": "200-250/天", "city": "深圳", "skills": "Python,SQL,Excel,机器学习", "education": "本科", "experience": "在校生"},
    {"title": "数据分析实习生", "company": "小米", "salary": "150-200/天", "city": "北京", "skills": "SQL,Excel,Python,用户增长", "education": "本科", "experience": "在校生"},
    {"title": "数据分析实习生", "company": "蔚来汽车", "salary": "180-220/天", "city": "上海", "skills": "Python,SQL,Excel,数据分析", "education": "本科", "experience": "在校生"},
    {"title": "AI产品实习生", "company": "字节跳动", "salary": "200-250/天", "city": "北京", "skills": "AI,产品思维,数据分析,SQL", "education": "本科", "experience": "在校生"},
    {"title": "数据运营实习生", "company": "美团", "salary": "150-200/天", "city": "北京", "skills": "Excel,SQL,数据分析,业务理解", "education": "本科", "experience": "在校生"},
    {"title": "商业分析实习生", "company": "腾讯", "salary": "180-230/天", "city": "深圳", "skills": "SQL,Excel,Python,商业洞察", "education": "本科", "experience": "在校生"},
    {"title": "数据产品实习生", "company": "阿里巴巴", "salary": "200-250/天", "city": "杭州", "skills": "SQL,产品设计,数据分析,Excel", "education": "本科", "experience": "在校生"},
    {"title": "数据科学实习生", "company": "字节跳动", "salary": "250-350/天", "city": "北京", "skills": "Python,SQL,机器学习,统计学,深度学习", "education": "硕士优先", "experience": "在校生"},
]

df = pd.DataFrame(sample_jobs)

# ========== 数据分析 ==========
print("=" * 50)
print("数据分析实习岗位市场分析报告")
print("=" * 50)

# 1. 技能需求分析
print("\n技能需求排行榜")
all_skills = []
for skills in df['skills']:
    all_skills.extend([s.strip() for s in skills.split(',')])

skill_counts = pd.Series(all_skills).value_counts()
for i, (skill, count) in enumerate(skill_counts.items(), 1):
    print(f"  {i}. {skill}: 出现在 {count}/{len(df)} 个岗位中 ({count/len(df)*100:.0f}%)")

# 2. 城市分布
print("\n城市分布")
city_counts = df['city'].value_counts()
for city, count in city_counts.items():
    print(f"  {city}: {count} 个岗位")

# 3. 薪资范围分析
print("\n薪资范围")
salary_mid = []
for s in df['salary']:
    parts = s.replace('/天', '').split('-')
    mid = (int(parts[0]) + int(parts[1])) / 2
    salary_mid.append(mid)
df['salary_mid'] = salary_mid
print(f"  平均日薪: {df['salary_mid'].mean():.0f} 元/天")
print(f"  最高日薪: {df['salary_mid'].max():.0f} 元/天")
print(f"  最低日薪: {df['salary_mid'].min():.0f} 元/天")

# ========== 可视化 ==========
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# 图1：技能需求排行榜
colors = plt.cm.Set2(np.linspace(0, 1, len(skill_counts)))
axes[0, 0].barh(skill_counts.index[::-1], skill_counts.values[::-1], color=colors[::-1])
axes[0, 0].set_title('数据分析实习 - 技能需求排行榜', fontsize=14)
axes[0, 0].set_xlabel('出现次数')
for i, v in enumerate(skill_counts.values[::-1]):
    axes[0, 0].text(v + 0.1, i, str(v), va='center')

# 图2：城市分布
city_colors = plt.cm.Pastel1(np.linspace(0, 1, len(city_counts)))
axes[0, 1].pie(city_counts.values, labels=city_counts.index, autopct='%1.0f%%',
               colors=city_colors, startangle=90)
axes[0, 1].set_title('岗位城市分布', fontsize=14)

# 图3：各公司薪资对比
company_salary = df.groupby('company')['salary_mid'].mean().sort_values(ascending=True)
axes[1, 0].barh(company_salary.index, company_salary.values, color='#1B998B')
axes[1, 0].set_title('各公司实习日薪对比', fontsize=14)
axes[1, 0].set_xlabel('平均日薪 (元)')
for i, v in enumerate(company_salary.values):
    axes[1, 0].text(v + 1, i, f'{v:.0f}元', va='center')

# 图4：核心结论
axes[1, 1].axis('off')
top_skills = skill_counts.head(5).index.tolist()
conclusion = (
    f"核心结论\n\n"
    f"- 最核心技能:\n"
    f"  {', '.join(top_skills)}\n\n"
    f"- 平均实习日薪:\n"
    f"  {df['salary_mid'].mean():.0f} 元/天\n\n"
    f"- 热门城市:\n"
    f"  北京、上海、深圳\n\n"
    f"- 你的匹配度:\n"
    f"  Python(已有) SQL(已有) Excel(已有)\n"
    f"  继续补充: 统计学、AB测试\n"
)
axes[1, 1].text(0.1, 0.5, conclusion, fontsize=12, va='center',
                bbox=dict(boxstyle='round', facecolor='#FFF3E0'))

plt.suptitle('数据分析实习岗位市场分析', fontsize=18, fontweight='bold')
plt.tight_layout()
plt.savefig('job_analysis.png', dpi=150)
print("\n图表已保存为 job_analysis.png")
print("\n结论：SQL + Python + Excel 是数据分析实习的三大核心技能")