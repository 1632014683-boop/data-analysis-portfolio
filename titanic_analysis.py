"""
泰坦尼克号乘客数据分析
数据来源：Kaggle Titanic Dataset
"""
import pandas as pd
import matplotlib.pyplot as plt

# 1. 加载数据（从本地文件）
df = pd.read_csv("train.csv")

# 2. 数据概览
print("数据集形状:", df.shape)
print("\n前5行数据:")
print(df.head())

# 3. 数据清洗
print("\n缺失值统计:")
print(df.isnull().sum())
df['Age'].fillna(df['Age'].median(), inplace=True)
df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)

# 4. 基本分析
print("\n存活率统计:")
print(df['Survived'].value_counts(normalize=True))

print("\n按性别分析存活率:")
print(df.groupby('Sex')['Survived'].mean())

print("\n按舱位分析存活率:")
print(df.groupby('Pclass')['Survived'].mean())

# 5. 可视化
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

df['Survived'].value_counts().plot(kind='bar', ax=axes[0], title='存活分布')
df.groupby('Sex')['Survived'].mean().plot(kind='bar', ax=axes[1], title='性别 vs 存活率')
df.groupby('Pclass')['Survived'].mean().plot(kind='bar', ax=axes[2], title='舱位 vs 存活率')

plt.tight_layout()
plt.savefig('titanic_analysis.png')
print("\n图表已保存为 titanic_analysis.png")
