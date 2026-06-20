"""
电力负荷数据分析 - 结合大数据+电气工程背景
数据来源：UCI Household Electric Power Consumption
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# 1. 加载数据（从UCI数据集）
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00235/household_power_consumption.zip"
print("正在下载数据...")

df = pd.read_csv(url, sep=';', na_values=['?'],
                 nrows=100000)  # 取前10万行，防止电脑卡顿
df['datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'],
                                format='%d/%m/%Y %H:%M:%S')

# 2. 数据清洗
df.dropna(inplace=True)
df['Global_active_power'] = pd.to_numeric(df['Global_active_power'], errors='coerce')
df['Global_active_power_kw'] = df['Global_active_power']  # 数据集原始单位为千瓦

# 3. 添加时间特征
df['hour'] = df['datetime'].dt.hour
df['day_of_week'] = df['datetime'].dt.dayofweek
df['month'] = df['datetime'].dt.month

print(f"数据量: {len(df)} 条")
print(f"时间范围: {df['datetime'].min()} ~ {df['datetime'].max()}")
print(f"平均功率: {df['Global_active_power_kw'].mean():.2f} kW")
print(f"峰值功率: {df['Global_active_power_kw'].max():.2f} kW")
print()

# 4. 分析：不同时间段的用电规律
print("=" * 40)
print("【核心发现】")
print("=" * 40)

# 按小时分析
hourly_avg = df.groupby('hour')['Global_active_power_kw'].mean()
peak_hour = hourly_avg.idxmax()
valley_hour = hourly_avg.idxmin()
print(f"\n[时间] 用电高峰期: {peak_hour}:00（平均 {hourly_avg[peak_hour]:.2f} kW）")
print(f"[时间] 用电低谷期: {valley_hour}:00（平均 {hourly_avg[valley_hour]:.2f} kW）")

# 按工作日/周末分析
df['is_weekend'] = df['day_of_week'].isin([5, 6])
weekday_power = df[~df['is_weekend']]['Global_active_power_kw'].mean()
weekend_power = df[df['is_weekend']]['Global_active_power_kw'].mean()
print(f"\n[日期] 工作日平均功率: {weekday_power:.2f} kW")
print(f"[日期] 周末平均功率: {weekend_power:.2f} kW")

# 5. 可视化
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# 图1：24小时用电曲线
hours = range(24)
axes[0, 0].plot(hours, [hourly_avg.get(h, 0) for h in hours], 
                marker='o', color='#FF6B35', linewidth=2)
axes[0, 0].set_title('24小时用电负荷曲线', fontsize=14)
axes[0, 0].set_xlabel('小时')
axes[0, 0].set_ylabel('平均功率 (kW)')
axes[0, 0].grid(True, alpha=0.3)
axes[0, 0].axvline(x=peak_hour, color='red', linestyle='--', alpha=0.5, label=f'峰值 {peak_hour}:00')
axes[0, 0].legend()

# 图2：工作日 vs 周末
bars = axes[0, 1].bar(['工作日', '周末'], [weekday_power, weekend_power], 
                      color=['#004E89', '#FF6B35'], width=0.5)
axes[0, 1].set_title('工作日 vs 周末用电对比', fontsize=14)
axes[0, 1].set_ylabel('平均功率 (kW)')
for bar in bars:
    height = bar.get_height()
    axes[0, 1].text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.2f} kW', ha='center', va='bottom')

# 图3：功率分布直方图
axes[1, 0].hist(df['Global_active_power_kw'], bins=50, 
                color='#004E89', edgecolor='white', alpha=0.7)
axes[1, 0].set_title('用电功率分布', fontsize=14)
axes[1, 0].set_xlabel('功率 (kW)')
axes[1, 0].set_ylabel('频次')

# 图4：各子电路功率占比
sub_meters = ['Global_active_power_kw', 'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3']
labels = ['总功率', '厨房用电', '洗衣用电', '空调/热水']
# 取平均值
avg_values = [df['Global_active_power_kw'].mean(),
              df['Sub_metering_1'].mean() / 1000,
              df['Sub_metering_2'].mean() / 1000,
              df['Sub_metering_3'].mean() / 1000]
colors = ['#FF6B35', '#004E89', '#1B998B', '#FFD166']
axes[1, 1].pie(avg_values[1:], labels=labels[1:], autopct='%1.1f%%', 
               colors=colors[1:], startangle=90)
axes[1, 1].set_title('家庭用电构成分析', fontsize=14)

plt.suptitle('电力负荷数据分析报告', fontsize=18, fontweight='bold')
plt.tight_layout()
plt.savefig('power_analysis.png', dpi=150)
print("\n[图表] 图表已保存为 power_analysis.png")
