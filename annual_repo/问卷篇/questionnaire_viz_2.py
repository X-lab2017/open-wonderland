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

def check_columns():
    """检查CSV文件中的列名"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    print("\n=== CSV文件列名 ===")
    for col in df.columns:
        print(col)

def plot_field_distribution():
    """绘制Q6题 - 只展示二级行业"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 只统计二级行业数据（Q6|2|open）
    field_data = df['Q6|2|open'].value_counts()
    field_pcts = (field_data / len(df)) * 100
    field_pcts = field_pcts.sort_values(ascending=True)  # 从低到高排序
    
    # 创建水平条形图
    plt.figure(figsize=(12, 8), facecolor='white')
    bars = plt.barh(range(len(field_pcts)), 
                   field_pcts.values,
                   color=COLOR_PALETTE[0])
    
    plt.yticks(range(len(field_pcts)), field_pcts.index)
    plt.xlabel('比例 (%)')
    
    # 添加数值标签
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2.,
                f'{width:.1f}%',
                ha='left', va='center')
    
    plt.title('您目前所处行业', pad=15, fontsize=14)
    plt.grid(True, axis='x', alpha=0.3)
    plt.tight_layout()
    save_plot('06_field_distribution.png')

def plot_work_status():
    """绘制工作状态分布 - 使用条形图"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 工作状态标签映射
    work_labels = {
        1: '在校学生',
        2: '学术研究员',
        3: '数据或业务分析师',
        4: '数据科学家/机器学习专家',
        29: '开源/技术布道师/DevRel',
        5: '数据库管理员',
        6: '设计师',
        7: '后端开发者',
        8: '架构师',
        9: '桌面或企业软件开发者',
        10: '嵌入式应用开发者',
        11: '前端开发者',
        12: '全栈开发者',
        13: '游戏或图形开发者',
        14: '移动端开发者',
        15: '测试（QA）工程师',
        16: 'DevOps 技术专家',
        17: '教师',
        18: '数据工程师',
        19: '网站可靠性工程师',
        20: '技术经理',
        21: '营销或销售',
        22: '产品经理',
        23: '科研工作者',
        24: '高级主管',
        25: 'CEO/CTO',
        26: '技术布道师',
        27: '运维工程师',
        28: '其他'
    }
    
    # 统计数据
    work_data = pd.DataFrame()
    for col in [c for c in df.columns if c.startswith('Q7|') and not c.endswith('open')]:
        option = int(col.split('|')[1])
        if option in work_labels:
            work_data[work_labels[option]] = pd.to_numeric(df[col], errors='coerce')
    
    # 计算百分比并按照占比排序
    work_pcts = work_data.sum() / len(df) * 100
    work_pcts = work_pcts.sort_values(ascending=True)  # 从低到高排序
    
    # 创建水平条形图
    plt.figure(figsize=(12, 10), facecolor='white')
    bars = plt.barh(range(len(work_pcts)), 
                   work_pcts.values,
                   color=COLOR_PALETTE[0])
    
    plt.yticks(range(len(work_pcts)), work_pcts.index)
    plt.xlabel('比例 (%)')
    
    # 添加数值标签
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2.,
                f'{width:.1f}%',
                ha='left', va='center')
    
    plt.title('以下哪些最能描述您的职业身份（可多选）', pad=15, fontsize=14)
    plt.grid(True, axis='x', alpha=0.3)
    plt.tight_layout()
    save_plot('07_work_status.png')

def plot_opensource_role():
    """绘制Q8题：在开源社区中的角色"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 角色标签映射
    role_labels = {
        2: '使用者（使用过开源产品）',
        4: '参与者（与社区有所互动）',
        1: '贡献者（有为社区做过贡献）',
        3: '维护者(项目maintainer、PMC成员等）',
        5: '生态运营',
        8: '其他'
    }
    
    # 统计数据
    role_data = pd.DataFrame()
    for col in [c for c in df.columns if c.startswith('Q8|') and not c.endswith('open')]:
        option = int(col.split('|')[1])
        if option in role_labels:
            role_data[role_labels[option]] = pd.to_numeric(df[col], errors='coerce')
    
    # 计算百分比并排序
    role_pcts = role_data.sum() / len(df) * 100
    role_pcts = role_pcts.sort_values(ascending=True)
    
    # 绘制水平条形图
    plt.figure(figsize=(12, 6), facecolor='white')
    bars = plt.barh(range(len(role_pcts)), 
                   role_pcts.values,
                   color=COLOR_PALETTE[0])
    
    plt.yticks(range(len(role_pcts)), role_pcts.index)
    plt.xlabel('比例 (%)')
    
    # 添加数值标签
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2.,
                f'{width:.1f}%',
                ha='left', va='center')
    
    plt.title('在开源社区中，您认为您的角色是（可多选）', pad=15, fontsize=14)
    plt.tight_layout()
    save_plot('08_opensource_role.png')

def plot_experience():
    """绘制Q9题"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 经验标签映射（保持原始顺序）
    exp_labels = {
        1: '小于 1 年',
        2: '1-2 年',
        3: '3-5 年',
        4: '6-9 年',
        5: '10 年以上',
        6: '未接触过'
    }
    
    # 统计数据并保持原始顺序
    exp_pcts = pd.Series(index=exp_labels.keys(), dtype=float)
    for idx in exp_labels:
        count = len(df[df['Q9'] == idx])
        exp_pcts[idx] = (count / len(df)) * 100
    
    # 创建柱状图
    plt.figure(figsize=(10, 6), facecolor='white')
    bars = plt.bar(range(len(exp_pcts)), 
                  exp_pcts.values,
                  color=COLOR_PALETTE[0])
    
    plt.xticks(range(len(exp_pcts)), 
               [exp_labels[i] for i in exp_pcts.index],
               rotation=45,
               ha='right')
    
    # 添加数值标签
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom')
    
    plt.ylabel('比例 (%)')
    plt.title('您接触开源的时长', pad=15, fontsize=14)
    plt.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()
    save_plot('09_experience.png')

def plot_opensource_usage():
    """绘制Q10题"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 使用情况标签映射
    usage_labels = {
        1: '产品免费',
        2: '以二次开发为主',
        3: '社区氛围好',
        4: '维护性好',
        5: '不关注产品是否开源',
        6: '其他'
    }
    
    # 统计数据
    usage_data = pd.DataFrame()
    for col in [c for c in df.columns if c.startswith('Q10|') and not c.endswith('open')]:
        option = int(col.split('|')[1])
        if option in usage_labels:
            usage_data[usage_labels[option]] = pd.to_numeric(df[col], errors='coerce')
    
    # 计算百分比并按照占比排序
    usage_pcts = usage_data.sum() / len(df) * 100
    usage_pcts = usage_pcts.sort_values(ascending=True)  # 从低到高排序（因为是水平条形图）
    
    # 创建水平条形图
    plt.figure(figsize=(10, 6), facecolor='white')
    bars = plt.barh(range(len(usage_pcts)), 
                   usage_pcts.values,
                   color=COLOR_PALETTE[0])
    
    plt.yticks(range(len(usage_pcts)), usage_pcts.index)
    plt.xlabel('比例 (%)')
    
    # 添加数值标签
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2.,
                f'{width:.1f}%',
                ha='left', va='center')
    
    plt.title('您使用开源软件的原因（可多选）', pad=15, fontsize=14)
    plt.grid(True, axis='x', alpha=0.3)
    plt.tight_layout()
    save_plot('10_opensource_usage.png')

def main():
    """主函数：执行所有绘图函数"""
    plot_field_distribution()    # Q6
    plot_work_status()          # Q7
    plot_opensource_role()      # Q8
    plot_experience()           # Q9
    plot_opensource_usage()     # Q10
    print("\n所有图表已生成完成，请查看 output 目录")

if __name__ == "__main__":
    main()