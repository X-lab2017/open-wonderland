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

def plot_commercialization_attitude():
    """绘制第21题：您是否认可将开源项目用于商业化？"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 获取数据
    scores = pd.to_numeric(df['Q21|1'], errors='coerce').dropna()
    
    # 创建提琴图
    plt.figure(figsize=(12, 6), facecolor='white')
    parts = plt.violinplot(scores, 
                          vert=False,
                          showmeans=True,
                          showmedians=True)
    
    # 设置提琴图颜色
    parts['bodies'][0].set_facecolor(COLOR_PALETTE[0])
    parts['bodies'][0].set_alpha(0.8)
    parts['cmeans'].set_color('black')
    parts['cmedians'].set_color('darkred')
    
    # 添加统计信息
    mean_score = scores.mean()
    median_score = scores.median()
    stats_text = f'平均分：{mean_score:.1f}\n中位数：{median_score:.1f}'
    
    plt.text(plt.xlim()[1], 0.5, 
            stats_text,
            verticalalignment='center',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
    
    # 添加分布信息
    counts = scores.value_counts().sort_index()
    pcts = counts / len(scores) * 100
    dist_text = '\n'.join([f'评分 {score}: {pct:.1f}%' for score, pct in pcts.items()])
    
    plt.text(plt.xlim()[0], 0.5,
            dist_text,
            verticalalignment='center',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
    
    plt.yticks([])
    plt.xlabel('认可程度')
    plt.title('您是否认可将开源项目用于商业化？', pad=15, fontsize=14)
    plt.tight_layout()
    save_plot('21_commercialization_attitude.png')

def plot_opensource_activities():
    """绘制第22题：您参加过什么开源实践活动？"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 活动标签映射 - 添加换行
    activity_labels = {
        1: 'Google编程之夏\n(GSoC)',
        2: '开源之夏\n(OSPP)',
        3: '开源编程夏令营\n(GLCC)',
        4: '飞桨黑客马拉松\n(PaddlePaddle Hackathon)',
        5: '开放原子大赛',
        6: '摩尔马开源\n人才培养计划',
        7: '未参加过相关实践',
        8: '其他'
    }
    
    # 统计数据
    activity_data = pd.DataFrame()
    for col in [c for c in df.columns if c.startswith('Q22|') and not c.endswith('open')]:
        option = int(col.split('|')[1])
        if option in activity_labels:
            activity_data[activity_labels[option]] = pd.to_numeric(df[col], errors='coerce')
    
    # 计算百分比并排序
    activity_pcts = activity_data.sum() / len(df) * 100
    activity_pcts = activity_pcts.sort_values(ascending=True)
    
    # 绘制水平条形图
    plt.figure(figsize=(12, 6), facecolor='white')
    bars = plt.barh(range(len(activity_pcts)), 
                   activity_pcts.values,
                   color=COLOR_PALETTE[0])
    
    plt.yticks(range(len(activity_pcts)), activity_pcts.index)
    plt.xlabel('比例 (%)')
    
    # 添加数值标签
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2.,
                f'{width:.1f}%',
                ha='left', va='center')
    
    plt.title('您参加过什么开源实践活动？', pad=15, fontsize=14)
    plt.tight_layout()
    save_plot('22_opensource_activities.png')

def plot_education_support():
    """绘制第23题：您的高校在开源教育与支持方面的��况如何？"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 支持方式标签映射 - 添加换行
    support_labels = {
        1: '开设与开源相关的课程',
        2: '组织与开源项目相关的\n讲座、社团或研讨会',
        3: '支持开源项目的基础设施和资源\n（如服务器、代码托管平台等）',
        4: '以上均无'
    }
    
    # 统计数据
    support_data = pd.DataFrame()
    for col in [c for c in df.columns if c.startswith('Q23|') and not c.endswith('open')]:
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
    
    plt.title('您的高校在开源教育与支持方面的情况如何？', pad=15, fontsize=14)
    plt.tight_layout()
    save_plot('23_education_support.png')

def plot_weekly_hours():
    """绘制第24题：您每周参与开源的时长���约是"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 时长标签映射
    hours_labels = {
        1: '1小时以内',
        2: '1-5小时',
        3: '5-10小时',
        4: '10-20小时',
        5: '20-35小时',
        6: '35小时以上'
    }
    
    # 统计数据
    hours_counts = df['Q24'].value_counts()
    hours_pcts = hours_counts / len(df) * 100
    
    # 确保所有选项都有数据
    for option in hours_labels:
        if option not in hours_pcts.index:
            hours_pcts[option] = 0
    
    # 按选项顺序排序
    hours_pcts = hours_pcts.reindex(sorted(hours_labels.keys()))
    hours_pcts.index = [hours_labels[i] for i in hours_pcts.index]
    
    # 绘制环形图
    plt.figure(figsize=(10, 8), facecolor='white')
    
    # 使用单一颜色的不同透明度
    base_color = COLOR_PALETTE[0]  # 使用主题色
    colors = []
    alphas = [0.2, 0.35, 0.5, 0.65, 0.8, 1.0]  # 递增的透明度
    for alpha in alphas:
        color = list(base_color)
        color[3] = alpha
        colors.append(color)
    
    # 绘制环形图
    plt.pie(hours_pcts.values, 
           labels=hours_pcts.index,
           autopct='%1.1f%%',
           colors=colors,
           pctdistance=0.85,  # 百分比标签的位置
           wedgeprops=dict(width=0.5))  # 设置环形图的宽度
    
    plt.title('您每周参与开源的时长', pad=15, fontsize=14)
    plt.tight_layout()
    save_plot('24_weekly_hours.png')

def plot_contribution_platforms():
    """绘制第25题：您通过哪些平台对开源项目做贡献？"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 平台标签映射
    platform_labels = {
        1: 'GitHub',
        2: 'GitLab',
        3: 'Gitee',
        7: 'Gitea',
        6: 'AtomGit',
        5: 'GitCode',
        4: '其他'
    }
    
    # 统计数据
    platform_data = pd.DataFrame()
    for col in [c for c in df.columns if c.startswith('Q25|') and not c.endswith('open')]:
        option = int(col.split('|')[1])
        if option in platform_labels:
            platform_data[platform_labels[option]] = pd.to_numeric(df[col], errors='coerce')
    
    # 计算百分比并排序
    platform_pcts = platform_data.sum() / len(df) * 100
    platform_pcts = platform_pcts.sort_values(ascending=True)
    
    # 绘制水平条形图
    plt.figure(figsize=(12, 6), facecolor='white')
    bars = plt.barh(range(len(platform_pcts)), 
                   platform_pcts.values,
                   color=COLOR_PALETTE[0])
    
    plt.yticks(range(len(platform_pcts)), platform_pcts.index)
    plt.xlabel('比例 (%)')
    
    # 添加数值标签
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2.,
                f'{width:.1f}%',
                ha='left', va='center')
    
    plt.title('您通过哪些平台对开源项目做贡献？', pad=15, fontsize=14)
    plt.tight_layout()
    save_plot('25_contribution_platforms.png')

def main():
    """主函数：执行所有绘图函数"""
    plot_commercialization_attitude()  # Q21
    plot_opensource_activities()       # Q22
    plot_education_support()           # Q23
    plot_weekly_hours()               # Q24
    plot_contribution_platforms()      # Q25
    print("\n所有图表已生成完成，请查看 output 目录")

if __name__ == "__main__":
    main() 