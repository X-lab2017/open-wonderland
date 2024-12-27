import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# 创建输出目录
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

# 设置中文字体和样式
plt.style.use('seaborn-v0_8-white')
sns.set_style("white")
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 使用 tab20c 配色方案
COLOR_PALETTE = plt.cm.tab20c(np.linspace(0, 1, 20))

def save_plot(filename):
    """保存图表到指定目录"""
    plt.savefig(output_dir / filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

def plot_age_distribution():
    """绘制年龄分布（Q2）- 使用柱状图"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 年龄标签映射（保持原始顺序）
    age_labels = {
        1: '20岁以下',
        2: '21-25岁',
        3: '26-30岁',
        4: '31-35岁',
        5: '36-50岁',
        6: '50岁以上'
    }
    
    # 按原始顺序统计数据
    age_data = pd.Series(index=age_labels.keys(), dtype=float)
    for idx in age_labels:
        count = len(df[df['Q2'] == idx])
        age_data[idx] = (count / len(df)) * 100
    
    # 创建柱状图
    plt.figure(figsize=(12, 6), facecolor='white')
    bars = plt.bar(range(len(age_data)), 
                  age_data.values,
                  color=COLOR_PALETTE[0],
                  alpha=0.8)
    
    # 设置x轴标签
    plt.xticks(range(len(age_data)), 
               [age_labels[i] for i in age_data.index],
               rotation=45)
    
    # 添加数值标签
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom')
    
    plt.ylabel('比例 (%)')
    plt.title('Q2 年龄分布', pad=15, fontsize=14)
    plt.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()
    save_plot('02_age_distribution.png')

def plot_gender_distribution():
    """绘制性别分布（Q3）- 使用饼图"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 性别标签映射（保持原始顺序）
    gender_labels = {
        1: '男',
        2: '女',
        3: '其他'
    }
    
    # 按原始顺序统计数据
    gender_data = pd.Series(index=gender_labels.keys(), dtype=float)
    for idx in gender_labels:
        count = len(df[df['Q3'] == idx])
        gender_data[idx] = (count / len(df)) * 100
    
    # 创建饼图
    plt.figure(figsize=(10, 8), facecolor='white')
    plt.pie(gender_data.values,
           labels=[gender_labels[i] for i in gender_data.index],
           autopct='%1.1f%%',
           colors=COLOR_PALETTE[:len(gender_data)],
           startangle=90)
    
    plt.title('Q3 性别分布', pad=15, fontsize=14)
    save_plot('03_gender_distribution.png')

def plot_education_distribution():
    """绘制学历分布（Q4）- 使用柱状图"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 学历标签映射（保持原始顺序）
    edu_labels = {
        1: '小学及以下',
        2: '初中',
        3: '高中/中专/技校',
        4: '大学专科',
        5: '大学本科',
        6: '硕士研究生',
        7: '博士研究生及以上'
    }
    
    # 按原始顺序统计数据
    edu_data = pd.Series(index=edu_labels.keys(), dtype=float)
    for idx in edu_labels:
        count = len(df[df['Q4'] == idx])
        edu_data[idx] = (count / len(df)) * 100
    
    # 创建柱状图
    plt.figure(figsize=(12, 6), facecolor='white')
    bars = plt.bar(range(len(edu_data)), 
                  edu_data.values,
                  color=COLOR_PALETTE[0],
                  alpha=0.8)
    
    # 设置x轴标签
    plt.xticks(range(len(edu_data)), 
               [edu_labels[i] for i in edu_data.index],
               rotation=45,
               ha='right')
    
    # 添加数值标签
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom')
    
    plt.ylabel('比例 (%)')
    plt.title('Q4 学历分布', pad=15, fontsize=14)
    plt.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()
    save_plot('04_education_distribution.png')

def plot_region_distribution():
    """绘制地区分布（Q5）- 使用分组条形图"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 提取省份和城市信息
    provinces = df['Q5|1|open'].str.extract(r'(.*?)[省市自治区]')[0]
    cities = df['Q5|2|open']
    
    # 统计数据
    province_counts = provinces.value_counts()
    province_pcts = (province_counts / len(df)) * 100
    
    # 创建分组条形图
    plt.figure(figsize=(15, 8), facecolor='white')
    
    # 绘制省份分布
    ax1 = plt.subplot(121)
    bars1 = plt.barh(range(len(province_pcts[:10])), 
                    province_pcts[:10].values,
                    color=COLOR_PALETTE[0])
    plt.yticks(range(len(province_pcts[:10])), province_pcts[:10].index)
    
    # 添加标签
    for bar in bars1:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2.,
                f'{width:.1f}%',
                ha='left', va='center')
    
    plt.xlabel('比例 (%)')
    plt.title('省份分布（Top 10）')
    
    # 绘制城市分布
    ax2 = plt.subplot(122)
    city_counts = cities.value_counts()
    city_pcts = (city_counts / len(df)) * 100
    
    bars2 = plt.barh(range(len(city_pcts[:10])), 
                    city_pcts[:10].values,
                    color=COLOR_PALETTE[1])
    plt.yticks(range(len(city_pcts[:10])), city_pcts[:10].index)
    
    # 添加标签
    for bar in bars2:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2.,
                f'{width:.1f}%',
                ha='left', va='center')
    
    plt.xlabel('比例 (%)')
    plt.title('城市分布（Top 10）')
    
    plt.suptitle('Q5 地区分布', fontsize=14, y=1.02)
    plt.tight_layout()
    save_plot('05_region_distribution.png')

def main():
    """主函数：执行所有绘图函数"""
    plot_age_distribution()      # Q2
    plot_gender_distribution()   # Q3
    plot_education_distribution()# Q4
    plot_region_distribution()   # Q5
    print("\n所有图表已生成完成，请查看 output 目录")

if __name__ == "__main__":
    main() 