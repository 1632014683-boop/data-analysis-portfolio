"""
泰坦尼克号数据分析 - 网页展示
运行方式：streamlit run app.py
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="泰坦尼克号数据分析", layout="wide")

st.title("🚢 泰坦尼克号乘客数据分析")
st.markdown("大一数据分析项目 | 数据来源：Kaggle")

# 加载数据
df = pd.read_csv("train.csv")

# 数据概览
st.header("📊 数据概览")
col1, col2 = st.columns(2)
col1.metric("总乘客数", df.shape[0])
col2.metric("存活率", f"{df['Survived'].mean():.1%}")

st.subheader("前5行数据")
st.dataframe(df.head())

# 存活分析
st.header("🔍 核心发现")

col1, col2, col3 = st.columns(3)

# 性别分析
fig1, ax1 = plt.subplots()
df.groupby('Sex')['Survived'].mean().plot(kind='bar', ax=ax1, color=['blue', 'pink'])
ax1.set_title('性别 vs 存活率')
ax1.set_ylabel('存活率')
col1.pyplot(fig1)
col1.write(f"女性存活率: **{df[df['Sex']=='female']['Survived'].mean():.1%}**")
col1.write(f"男性存活率: **{df[df['Sex']=='male']['Survived'].mean():.1%}**")

# 舱位分析
fig2, ax2 = plt.subplots()
df.groupby('Pclass')['Survived'].mean().plot(kind='bar', ax=ax2, color=['gold', 'silver', '#cd7f32'])
ax2.set_title('舱位 vs 存活率')
ax2.set_ylabel('存活率')
col2.pyplot(fig2)
col2.write(f"头等舱: **{df[df['Pclass']==1]['Survived'].mean():.1%}**")
col2.write(f"三等舱: **{df[df['Pclass']==3]['Survived'].mean():.1%}**")

# 年龄分布
fig3, ax3 = plt.subplots()
df['Age'].hist(bins=30, ax=ax3, edgecolor='black')
ax3.set_title('年龄分布')
ax3.set_xlabel('年龄')
col3.pyplot(fig3)

# 结论
st.header("📝 结论")
st.info("""
1. **性别**：女性存活率远高于男性（约 3.8 倍）
2. **舱位**：头等舱存活率最高，三等舱最低
3. **年龄**：儿童存活率较高
""")

st.caption("项目代码: https://github.com/1632014683-boop/data-analysis-portfolio")