"""
电力负荷数据分析 - Streamlit 网页展示
运行方式：streamlit run power_app.py
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="电力负荷数据分析", layout="wide")

st.title("⚡ 家庭电力负荷数据分析")
st.markdown("**大数据 + 电气工程** | 数据来源：UCI 机器学习库")

# 加载数据
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00235/household_power_consumption.zip"

with st.spinner("正在加载数据..."):
    df = pd.read_csv(url, sep=';', na_values=['?'], nrows=100000)
    df['datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
    df.dropna(inplace=True)
    df['Global_active_power_kw'] = pd.to_numeric(df['Global_active_power'], errors='coerce') / 1000
    df['hour'] = df['datetime'].dt.hour
    df['day_of_week'] = df['datetime'].dt.dayofweek
    df['month'] = df['datetime'].dt.month
    df['is_weekend'] = df['day_of_week'].isin([5, 6])

# 概览指标
st.header("📊 数据概览")
col1, col2, col3, col4 = st.columns(4)
col1.metric("数据量", f"{len(df):,} 条")
col2.metric("平均功率", f"{df['Global_active_power_kw'].mean():.2f} kW")
col3.metric("峰值功率", f"{df['Global_active_power_kw'].max():.2f} kW")
col4.metric("时间跨度", "约2个月")

# 核心发现
st.header("🔍 核心发现")

col1, col2 = st.columns(2)

# 24小时用电曲线
hourly_avg = df.groupby('hour')['Global_active_power_kw'].mean()
peak_hour = int(hourly_avg.idxmax())

fig1, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(hourly_avg.index, hourly_avg.values, marker='o', color='#FF6B35', linewidth=2)
ax1.set_title('24小时用电负荷曲线', fontsize=14)
ax1.set_xlabel('小时')
ax1.set_ylabel('平均功率 (kW)')
ax1.grid(True, alpha=0.3)
ax1.axvline(x=peak_hour, color='red', linestyle='--', alpha=0.5, label=f'峰值 {peak_hour}:00')
ax1.legend()
col1.pyplot(fig1)
col1.success(f"**用电高峰期**: {peak_hour}:00 ({hourly_avg[peak_hour]:.2f} kW)")

# 工作日 vs 周末
weekday_power = df[~df['is_weekend']]['Global_active_power_kw'].mean()
weekend_power = df[df['is_weekend']]['Global_active_power_kw'].mean()

fig2, ax2 = plt.subplots(figsize=(10, 5))
bars = ax2.bar(['工作日', '周末'], [weekday_power, weekend_power], 
               color=['#004E89', '#FF6B35'], width=0.5)
ax2.set_title('工作日 vs 周末用电对比', fontsize=14)
ax2.set_ylabel('平均功率 (kW)')
for bar in bars:
    h = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., h, f'{h:.2f} kW', ha='center', va='bottom')
col2.pyplot(fig2)
col2.warning(f"**周末比工作日多用电** {(weekend_power/weekday_power - 1)*100:.0f}%")

# 用电构成
st.header("📈 深度分析")
col1, col2 = st.columns(2)

fig3, ax3 = plt.subplots(figsize=(8, 8))
labels = ['厨房用电', '洗衣用电', '空调/热水', '其他']
sizes = [df['Sub_metering_1'].mean(),
         df['Sub_metering_2'].mean(),
         df['Sub_metering_3'].mean(),
         df['Global_active_power'].mean()*60 - df[['Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3']].mean().sum()]
colors = ['#FF6B35', '#004E89', '#1B998B', '#FFD166']
ax3.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
ax3.set_title('家庭用电构成分析', fontsize=14)
col1.pyplot(fig3)

col2.markdown("""
### 💡 结论与建议

1. **晚8点是用电高峰** — 可考虑分时电价策略
2. **周末用电量显著高于工作日** — 与居家活动时间相关
3. **空调/热水器占比最高** — 节能重点设备
4. 结合**电气工程知识**，这些规律可用于：
   - 智能电网需求侧响应
   - 家庭能耗优化建议
   - 电力负荷预测
""")

st.caption("项目代码: https://github.com/1632014683-boop/data-analysis-portfolio")