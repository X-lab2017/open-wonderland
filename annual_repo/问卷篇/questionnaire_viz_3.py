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

def plot_opensource_search():
    """绘制开源产品获取途径分布"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 途径标签映射
    search_labels = {
        1: '通过代码托管平台搜索',
        2: '通过搜索引擎搜索',
        3: '技术社区、技术媒体推荐',
        4: '技术交流与开源代码',
        5: '其他使用者推荐',
        6: '其他'
    }
    
    # 统计数据
    search_data = pd.DataFrame()
    for col in [c for c in df.columns if c.startswith('Q11|') and not c.endswith('open')]:
        option = int(col.split('|')[1])
        if option in search_labels:
            search_data[search_labels[option]] = pd.to_numeric(df[col], errors='coerce')
    
    # 计算百分比并排序
    search_pcts = search_data.sum() / len(df) * 100
    search_pcts = search_pcts.sort_values(ascending=True)
    
    # 创建水平条形图
    plt.figure(figsize=(12, 6), facecolor='white')
    bars = plt.barh(range(len(search_pcts)), 
                   search_pcts.values,
                   color=COLOR_PALETTE[0])
    
    plt.yticks(range(len(search_pcts)), search_pcts.index)
    plt.xlabel('比例 (%)')
    
    # 添加数值标签
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2.,
                f'{width:.1f}%',
                ha='left', va='center')
    
    plt.title('您检索开源产品的途径（可多选）', pad=15, fontsize=14)
    plt.tight_layout()
    save_plot('11_opensource_search.png')

def plot_project_selection():
    """绘制开源产品选择因素分布"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 因素标签映射
    selection_labels = {
        1: '代码规范程度高',
        2: '开发者活跃度高',
        3: '开源许可证合适',
        4: '社区回复及时',
        5: '项目文档完整',
        6: '持续的更新和维护',
        7: '其他'
    }
    
    # 统计数据
    selection_data = pd.DataFrame()
    for col in [c for c in df.columns if c.startswith('Q12|') and not c.endswith('open')]:
        option = int(col.split('|')[1])
        if option in selection_labels:
            selection_data[selection_labels[option]] = pd.to_numeric(df[col], errors='coerce')
    
    # 计算百分比并排序
    selection_pcts = selection_data.sum() / len(df) * 100
    selection_pcts = selection_pcts.sort_values(ascending=True)
    
    # 准备数据
    categories = selection_pcts.index
    values = selection_pcts.values
    
    # 创建雷达图
    angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False)
    values = np.concatenate((values, [values[0]]))
    angles = np.concatenate((angles, [angles[0]]))
    
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, values)
    ax.fill(angles, values, alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    
    plt.title('影响开源产品选择的因素分析', pad=15, fontsize=14)
    save_plot('12_project_selection.png')

def plot_tech_interest():
    """绘制感兴趣的技术方向分布"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 技术方向标签映射
    tech_labels = {
        1: '人工智能',
        2: '容器化和云计算',
        3: '开发工具',
        4: '网络和安全',
        5: '数据库和数据处理',
        8: '前端和移动开发',
        9: '操作系统',
        7: '其他'
    }
    
    # 统计数据
    tech_data = pd.DataFrame()
    for col in [c for c in df.columns if c.startswith('Q13|') and not c.endswith('open')]:
        option = int(col.split('|')[1])
        if option in tech_labels:
            tech_data[tech_labels[option]] = pd.to_numeric(df[col], errors='coerce')
    
    # 计算百分比并排序
    tech_pcts = tech_data.sum() / len(df) * 100
    tech_pcts = tech_pcts.sort_values(ascending=True)
    
    # 创建水平条形图
    plt.figure(figsize=(12, 6), facecolor='white')
    bars = plt.barh(range(len(tech_pcts)), 
                   tech_pcts.values,
                   color=COLOR_PALETTE[0])
    
    plt.yticks(range(len(tech_pcts)), tech_pcts.index)
    plt.xlabel('比例 (%)')
    
    # 添加数值标签
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2.,
                f'{width:.1f}%',
                ha='left', va='center')
    
    plt.title('感兴趣的技术方向分布', pad=15, fontsize=14)
    plt.tight_layout()
    save_plot('13_tech_interest.png')

def plot_usage_problems():
    """绘制使用开源产品遇到的问题分布"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 问题标签映射
    problem_labels = {
        1: '不稳定的版本更新',
        2: '缺少相关功能',
        3: '项目缺少文档',
        4: '项目依赖混乱',
        5: '项目运行出错',
        6: '没有问题',
        7: '其他'
    }
    
    # 统计数据
    problem_data = pd.DataFrame()
    for col in [c for c in df.columns if c.startswith('Q14|') and not c.endswith('open')]:
        option = int(col.split('|')[1])
        if option in problem_labels:
            problem_data[problem_labels[option]] = pd.to_numeric(df[col], errors='coerce')
    
    # 计算百分比并排序
    problem_pcts = problem_data.sum() / len(df) * 100
    problem_pcts = problem_pcts.sort_values(ascending=True)
    
    # 创建水平条形图
    plt.figure(figsize=(12, 6), facecolor='white')
    bars = plt.barh(range(len(problem_pcts)), 
                   problem_pcts.values,
                   color=COLOR_PALETTE[0])
    
    plt.yticks(range(len(problem_pcts)), problem_pcts.index)
    plt.xlabel('比例 (%)')
    
    # 添加数值标签
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2.,
                f'{width:.1f}%',
                ha='left', va='center')
    
    plt.title('使用开源产品遇到的问题', pad=15, fontsize=14)
    plt.tight_layout()
    save_plot('14_usage_problems.png')

def plot_license_knowledge():
    """绘制第15题：您了解哪些开源许可证"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 许可证标签映射
    license_labels = {
        1: 'Apache 许可证',
        2: 'MIT 许可证',
        3: 'BSD 许可证',
        4: 'GPL 许可证',
        5: 'Mozilla 许可证',
        6: 'LGPL 许可证',
        7: '木兰公共许可证（MulanPubL）',
        8: '木兰宽松许可证（MulanPSL）',
        9: '上述全都了解',
        10: '上述全都不了解',
        11: '其他'
    }
    
    # 统计数据
    license_data = pd.DataFrame()
    for col in [c for c in df.columns if c.startswith('Q15|') and not c.endswith('open')]:
        option = int(col.split('|')[1])
        if option in license_labels:
            license_data[license_labels[option]] = pd.to_numeric(df[col], errors='coerce')
    
    # 计算百分比并排序
    license_pcts = license_data.sum() / len(df) * 100
    
    # 过滤掉0值并按百分比降序排序
    license_pcts = license_pcts[license_pcts > 0.01].sort_values(ascending=True)
    
    # 绘制水平条形图
    plt.figure(figsize=(12, 6), facecolor='white')
    bars = plt.barh(range(len(license_pcts)), 
                   license_pcts.values,
                   color=COLOR_PALETTE[0])
    
    plt.yticks(range(len(license_pcts)), license_pcts.index)
    plt.xlabel('比例 (%)')
    
    # 添加数值标签
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2.,
                f'{width:.1f}%',
                ha='left', va='center')
    
    plt.title('您了解哪些开源许可证（可多选）', pad=15, fontsize=14)
    plt.tight_layout()
    save_plot('15_license_knowledge.png')

def main():
    """主函数：执行所有绘图函数"""
    plot_opensource_search()      # Q11
    plot_project_selection()      # Q12
    plot_tech_interest()         # Q13
    plot_usage_problems()        # Q14
    plot_license_knowledge()     # Q15
    print("\n所有图表已生成完成，请查看 output 目录")

if __name__ == "__main__":
    main()