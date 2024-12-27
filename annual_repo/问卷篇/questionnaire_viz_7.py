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

def plot_community_users():
    """绘制第31题：您所在社区活跃用户最多有多少？"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 用户数量标签映射
    user_labels = {
        1: '50人以内',
        2: '50-200人',
        3: '200-500人',
        4: '500人以上'
    }
    
    # 统计数据 - 只统计有效回答
    valid_responses = df['Q31'].dropna()  # 删��缺失值
    valid_responses = valid_responses[valid_responses.isin(user_labels.keys())]  # 只保留有效选项
    
    user_counts = valid_responses.value_counts()
    user_pcts = user_counts / len(valid_responses) * 100  # 使用有效回答数量计算百分比
    
    # 确保所有选项都有数据并按顺序排列
    user_pcts = user_pcts.reindex(sorted(user_labels.keys()), fill_value=0)
    user_pcts.index = [user_labels[i] for i in user_pcts.index]
    
    # 绘制纵向柱状图
    plt.figure(figsize=(10, 6), facecolor='white')
    bars = plt.bar(range(len(user_pcts)), 
                  user_pcts.values,
                  color=COLOR_PALETTE[0],
                  width=0.6)
    
    plt.xticks(range(len(user_pcts)), user_pcts.index)
    plt.ylabel('比例 (%)')
    
    # 添加数值标签
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom')
    
    plt.title('您所在社区活跃用户最多有多少？', pad=15, fontsize=14)
    plt.tight_layout()
    save_plot('31_community_users.png')

def plot_community_developers():
    """绘制第32题：您所在社区活跃开发者最多有多少？"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 开发者数量标签映射
    dev_labels = {
        1: '5人以内',
        2: '5-20人',
        3: '20-50人',
        4: '50人以上'
    }
    
    # 统计数据
    dev_counts = df['Q32'].value_counts()
    dev_pcts = dev_counts / len(df) * 100
    
    # 确保所有选项都有数据
    for option in dev_labels:
        if option not in dev_pcts.index:
            dev_pcts[option] = 0
    
    # 按选项顺序排序
    dev_pcts = dev_pcts.reindex(sorted(dev_labels.keys()))
    dev_pcts.index = [dev_labels[i] for i in dev_pcts.index]
    
    # 绘制环形图
    plt.figure(figsize=(10, 8), facecolor='white')
    
    # 使用单一颜色的不同透明度
    base_color = COLOR_PALETTE[0]
    colors = []
    alphas = [0.3, 0.5, 0.7, 0.9]
    for alpha in alphas:
        color = list(base_color)
        color[3] = alpha
        colors.append(color)
    
    plt.pie(dev_pcts.values, 
           labels=dev_pcts.index,
           autopct='%1.1f%%',
           colors=colors,
           pctdistance=0.85,
           wedgeprops=dict(width=0.5))
    
    plt.title('您所在社区活跃开发者最多有多少？', pad=15, fontsize=14)
    plt.tight_layout()
    save_plot('32_community_developers.png')

def plot_community_management():
    """绘制第33题：您所在的社区和项目管理情况"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 管理情况标签映射
    management_labels = {
        10: '有清晰的治理结构',
        3: '有专人负责社区的日常运营',
        4: '有明确的社区规范和准则',
        6: '有持续更新的文档和资源，\n以帮助新成员融入',
        7: '定期举行线上/线下相关活动',
        8: '借助自动化工具来帮助运营',
        9: '借助数据可视化工具来帮助运营'
    }
    
    # 统计数据
    management_data = pd.DataFrame()
    for col in [c for c in df.columns if c.startswith('Q33|') and not c.endswith('open')]:
        option = int(col.split('|')[1])
        if option in management_labels:
            management_data[management_labels[option]] = pd.to_numeric(df[col], errors='coerce')
    
    # 计算百分比并排序
    management_pcts = management_data.sum() / len(df) * 100
    management_pcts = management_pcts.sort_values(ascending=True)
    
    # 绘制水平条形图
    plt.figure(figsize=(12, 6), facecolor='white')
    bars = plt.barh(range(len(management_pcts)), 
                   management_pcts.values,
                   color=COLOR_PALETTE[0])
    
    plt.yticks(range(len(management_pcts)), management_pcts.index)
    plt.xlabel('比例 (%)')
    
    # 添加数值标签
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2.,
                f'{width:.1f}%',
                ha='left', va='center')
    
    plt.title('您所在的社区和项目管理情况', pad=15, fontsize=14)
    plt.tight_layout()
    save_plot('33_community_management.png')

def plot_company_support():
    """绘制第34题：您所在项目有哪些类型的商业公司支持？"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 公司支持类型标签映射
    support_labels = {
        3: '有商业公司声明采用项目',
        4: '有商业公司参与协同开发',
        5: '有商业公司给予资源或资金赞助',
        8: '没有商业公司支持',
        7: '其他'
    }
    
    # 统计数据
    support_data = pd.DataFrame()
    for col in [c for c in df.columns if c.startswith('Q34|') and not c.endswith('open')]:
        option = int(col.split('|')[1])
        if option in support_labels:
            support_data[support_labels[option]] = pd.to_numeric(df[col], errors='coerce')
    
    # 计算百分比并排序
    support_pcts = support_data.sum() / len(df) * 100
    support_pcts = support_pcts.sort_values(ascending=True)
    
    # 绘制水平条形图
    plt.figure(figsize=(12, 6), facecolor='white')
    bars = plt.barh(range(len(support_pcts)), 
                   support_pcts.values,
                   color=COLOR_PALETTE[0])
    
    plt.yticks(range(len(support_pcts)), support_pcts.index)
    plt.xlabel('比例 (%)')
    
    # 添加数值标签
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2.,
                f'{width:.1f}%',
                ha='left', va='center')
    
    plt.title('您所在项目有哪些类型的商业公司支持？', pad=15, fontsize=14)
    plt.tight_layout()
    save_plot('34_company_support.png')

def plot_community_qualities():
    """绘制第35题：您认为影响一个开源社区健康持续发展的最重要的特质有哪些"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 特质标签映射
    quality_labels = {
        3: '快速的社区响应速度',
        4: '有持续涌入的新贡献者',
        5: '新贡献者能够被转化为\n长期贡献者',
        6: '好的社区维护者',
        7: '良好的社区文化和氛围',
        8: '资金支持',
        9: '项目被广泛使用',
        10: '项目的技术先进性',
        11: '其他'
    }
    
    # 统计数据
    quality_data = pd.DataFrame()
    for col in [c for c in df.columns if c.startswith('Q35|') and not c.endswith('open')]:
        option = int(col.split('|')[1])
        if option in quality_labels:
            quality_data[quality_labels[option]] = pd.to_numeric(df[col], errors='coerce')
    
    # 计算百分比并排序
    quality_pcts = quality_data.sum() / len(df) * 100
    
    # 过滤掉0值并按百分比降序排序
    quality_pcts = quality_pcts[quality_pcts > 0].sort_values(ascending=True)
    
    # 绘制水平条形图
    plt.figure(figsize=(12, 6), facecolor='white')
    bars = plt.barh(range(len(quality_pcts)), 
                   quality_pcts.values,
                   color=COLOR_PALETTE[0])
    
    plt.yticks(range(len(quality_pcts)), quality_pcts.index)
    plt.xlabel('比例 (%)')
    
    # 添加数值标签
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2.,
                f'{width:.1f}%',
                ha='left', va='center')
    
    plt.title('您认为影响一个开源社区健康持续发展的最重要的特质有哪些', pad=15, fontsize=14)
    plt.tight_layout()
    save_plot('35_community_qualities.png')

def main():
    """主函数：执行所有绘图函数"""
    plot_community_users()          # Q31
    plot_community_developers()     # Q32
    plot_community_management()     # Q33
    plot_company_support()         # Q34
    plot_community_qualities()      # Q35
    print("\n所有图表已生成完成，请查看 output 目录")

if __name__ == "__main__":
    main() 