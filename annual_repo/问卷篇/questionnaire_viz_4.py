import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import textwrap

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

def get_question_options(question_num):
    """从编码对照表中读取指定题目的选项"""
    df_code = pd.read_csv('2024 中国开源参与情况问卷调查_文本编码对照表_202412111519.csv', encoding='gb18030')
    
    # 找到该题目的所有行
    question_mask = df_code.iloc[:,0].astype(str).str.contains(f'Q{question_num}')
    question_rows = df_code[question_mask]
    
    # 获取题目标题
    question_title = question_rows.iloc[0,1]
    print(f"\n处理问 Q{question_num}: {question_title}")
    
    # 获取选项映射
    options = {}
    for _, row in question_rows.iterrows():
        if pd.isna(row[0]) and pd.notna(row[1]) and pd.notna(row[2]):
            try:
                option_num = int(row[1].strip())
                option_text = row[2].strip()
                options[option_num] = option_text
                print(f"选项 {option_num}: {option_text}")
            except ValueError:
                continue
    
    return options

def adjust_plot_layout():
    """调整图表布局，为长文本留出空间"""
    plt.subplots_adjust(left=0.4)  # 为左侧文本留出更多空间

def plot_with_long_labels(pcts, title, filename, figsize=(12, 6)):
    """通用绘图函数，处理长标签"""
    fig, ax = plt.subplots(figsize=figsize, facecolor='white')
    
    # 绘制水平条形图
    bars = ax.barh(range(len(pcts)), 
                  pcts.values,
                  color=COLOR_PALETTE[0])
    
    # 设置y轴标签位置在图表外侧
    ax.set_yticks(range(len(pcts)))
    ax.set_yticklabels([])  # 清除默认标签
    
    # 在左侧添加长文本标签
    for i, label in enumerate(pcts.index):
        ax.text(-0.2, i, 
                label, 
                ha='right', 
                va='center',
                transform=ax.get_yaxis_transform())
    
    # 添加数值标签
    for bar in bars:
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2.,
                f'{width:.1f}%',
                ha='left', va='center')
    
    ax.set_xlabel('比例 (%)')
    ax.set_title(title, pad=15, fontsize=14)
    
    # 调整布局
    plt.subplots_adjust(left=0.4)  # 为左侧文本留出空间
    plt.tight_layout()
    save_plot(filename)

def plot_opensource_tools():
    """绘制第16题：下面哪三个因素更能促使您对项目做贡献"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 严格按照问卷选项设置
    tool_labels = {
        1: '对项目领域感兴趣',
        2: '维护程序的问题/可拓展性',
        3: '社区形式的开放、氛围和谐',
        4: '提升技术能力',
        5: '开源理念的认同感',
        6: '有经济上的回报',
        7: '能够获得职业发展机会',
        8: '获得更高的社会认可',
        9: '暂时没有贡献意愿',
        10: '其他'
    }
    
    # 获取数据并处理
    tool_data = pd.DataFrame()
    for col in [c for c in df.columns if c.startswith('Q16|') and not c.endswith('open')]:
        option = int(col.split('|')[1])
        if option in tool_labels:
            tool_data[tool_labels[option]] = pd.to_numeric(df[col], errors='coerce')
    
    # 计算百分比
    tool_pcts = tool_data.sum() / len(df) * 100
    tool_pcts = tool_pcts.sort_values(ascending=True)
    
    # 绘制条形图
    plt.figure(figsize=(12, 6), facecolor='white')
    bars = plt.barh(range(len(tool_pcts)), tool_pcts.values, color=COLOR_PALETTE[0])
    
    plt.yticks(range(len(tool_pcts)), tool_pcts.index)
    plt.xlabel('选择比例 (%)')
    
    # 添加数值标签
    for i, bar in enumerate(bars):
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2, 
                f'{width:.1f}%', 
                ha='left', va='center', fontsize=10)
    
    plt.title('下面哪三个因素更能促使您对项目做贡献', pad=15, fontsize=14)
    plt.grid(True, axis='x', alpha=0.3)
    plt.tight_layout()
    save_plot('16_opensource_tools.png')

def plot_opensource_fields():
    """绘制第17题：您与开源社区的沟通方式（可多选）"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 简化选项文本，去除括号中的示例
    field_labels = {
        1: '国际化通讯工具',
        2: '国内通讯工具',
        3: '异步沟通工具',
        5: '其他'
    }
    
    # 获取数据并处理
    field_data = pd.DataFrame()
    for col in [c for c in df.columns if c.startswith('Q17|') and not c.endswith('open')]:
        option = int(col.split('|')[1])
        if option in field_labels:
            field_data[field_labels[option]] = pd.to_numeric(df[col], errors='coerce')
    
    # 计算百分比
    field_pcts = field_data.sum() / len(df) * 100
    field_pcts = field_pcts.sort_values(ascending=True)
    
    # 绘制条形图
    plt.figure(figsize=(12, 6), facecolor='white')
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
    
    plt.title('您与开源社区的沟通方式（可多选）', pad=15, fontsize=14)
    plt.tight_layout()
    save_plot('17_opensource_fields.png')

def plot_opensource_languages():
    """绘制第18题：您最主要使用或访问哪些社区/平台？（可选三项）"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 简化选项文本，去除括号中的示例
    language_labels = {
        3: '海外代码托管平台',
        4: '国内代码托管平台',
        5: '海外技术论坛',
        6: '国内技术论坛',
        9: '其他'
    }
    
    # 获取数据并处理
    language_data = pd.DataFrame()
    for col in [c for c in df.columns if c.startswith('Q18|') and not c.endswith('open')]:
        option = int(col.split('|')[1])
        if option in language_labels:
            language_data[language_labels[option]] = pd.to_numeric(df[col], errors='coerce')
    
    # 计算百分比
    language_pcts = language_data.sum() / len(df) * 100
    language_pcts = language_pcts.sort_values(ascending=True)
    
    # 绘制条形图
    plt.figure(figsize=(12, 6), facecolor='white')
    bars = plt.barh(range(len(language_pcts)), 
                   language_pcts.values,
                   color=COLOR_PALETTE[0])
    
    plt.yticks(range(len(language_pcts)), language_pcts.index)
    plt.xlabel('比例 (%)')
    
    # 添加数值标签
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2.,
                f'{width:.1f}%',
                ha='left', va='center')
    
    plt.title('您最主要使用或访问哪些技术社区/平台？（可选三项）', pad=15, fontsize=14)
    plt.tight_layout()
    save_plot('18_opensource_languages.png')

def plot_opensource_platforms():
    """绘制第19题：您所在企业开源软件使用情况（可多选）"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 简化选项文本并添加换行
    platform_labels = {
        7: '使用社区版本',
        4: '购买使用商业版本的\n开源软件',
        5: '使用开源软件但没有相应的\n使用要求与管理规范',
        6: '对开源软件和开源制品库的使用\n有相应的使用要求与管理规范',
        3: '不使用开源软件'
    }
    
    # 获取数据并处理
    platform_data = pd.DataFrame()
    for col in [c for c in df.columns if c.startswith('Q19|') and not c.endswith('open')]:
        option = int(col.split('|')[1])
        if option in platform_labels:
            platform_data[platform_labels[option]] = pd.to_numeric(df[col], errors='coerce')
    
    # 计算百分比
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
    
    plt.title('您所在企业开源软件使用情况（可多选）', pad=15, fontsize=14)
    plt.tight_layout()
    save_plot('19_opensource_platforms.png')

def plot_opensource_satisfaction():
    """绘制第20题：您多大程度上认为自己是开源社区的一份子？"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 获取数据
    satisfaction_data = pd.to_numeric(df['Q20|1'], errors='coerce').dropna()
    
    # 修改提琴图样式
    plt.figure(figsize=(12, 6), facecolor='white')
    parts = plt.violinplot(satisfaction_data, 
                          vert=False,
                          showmeans=True,
                          showmedians=True)
    
    # 设置提琴图颜色
    parts['bodies'][0].set_facecolor(COLOR_PALETTE[0])
    parts['bodies'][0].set_alpha(0.8)
    parts['cmeans'].set_color('black')
    parts['cmedians'].set_color('darkred')
    
    # 计算统计量
    mean_score = satisfaction_data.mean()
    median_score = satisfaction_data.median()
    q1 = satisfaction_data.quantile(0.25)
    q3 = satisfaction_data.quantile(0.75)
    
    stats_text = (f'平均分：{mean_score:.1f}\n'
                 f'中位数：{median_score:.1f}\n'
                 f'25分位数：{q1:.1f}\n'
                 f'75分位数：{q3:.1f}')
    
    plt.text(plt.xlim()[1], 0.5, 
            stats_text,
            verticalalignment='center',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
    
    # 添加分布信息
    counts = satisfaction_data.value_counts().sort_index()
    pcts = counts / len(satisfaction_data) * 100
    dist_text = '\n'.join([f'评分 {score}: {pct:.1f}%' for score, pct in pcts.items()])
    
    plt.text(plt.xlim()[0], 0.5,
            dist_text,
            verticalalignment='center',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
    
    plt.yticks([])
    plt.xlabel('评分')
    plt.title('您多大程度上认为自己是开源社区的一份子？', pad=15, fontsize=14)
    plt.tight_layout()
    save_plot('20_opensource_satisfaction.png')

def plot_role_satisfaction():
    """绘制第20.5题：开源社区角色与归属感的关系分析"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 角色标签映射
    role_labels = {
        2: '使用者',
        4: '参与者',
        1: '贡献者',
        3: '维护者',
        5: '生态运营',
        8: '其他'
    }
    
    # 准备数据
    results = []
    for role_id in sorted(role_labels.keys()):
        role_col = f'Q8|{role_id}'
        if role_col in df.columns:
            # 选择该角色的用户
            role_df = df[df[role_col] == 1]
            # 计算该角色下各评分的占比
            scores = pd.to_numeric(role_df['Q20|1'], errors='coerce').value_counts().sort_index()
            total = len(role_df)
            percentages = (scores / total * 100).round(1)
            
            # 填充缺失的评分为0
            all_scores = range(1, 6)  # 1-5分
            for score in all_scores:
                if score not in percentages.index:
                    percentages[score] = 0
            percentages = percentages.sort_index()
            
            results.append({
                'role': role_labels[role_id],
                'percentages': percentages,
                'mean': pd.to_numeric(role_df['Q20|1'], errors='coerce').mean()
            })
    
    # 创建图表
    plt.figure(figsize=(12, 6), facecolor='white')
    
    # 设置颜色映射 - 使用与问卷风格一致的蓝色系
    base_color = COLOR_PALETTE[0]  # 获取基础蓝色
    colors = []
    for alpha in [0.2, 0.4, 0.6, 0.8, 1.0]:  # 使用不同的透明度创建渐变效果
        color = list(base_color)
        color[3] = alpha  # 修改alpha通道
        colors.append(color)
    
    y_positions = range(len(results))
    bar_height = 0.8
    
    # 绘制堆叠的水平条形图
    left = np.zeros(len(results))
    for score in range(1, 6):
        widths = [r['percentages'][score] for r in results]
        plt.barh(y_positions, widths, left=left, height=bar_height,
                color=colors[score-1], label=f'{score}分')
        
        # 在每个部分添加百分比标签（当百分比大于5%时）
        for i, width in enumerate(widths):
            if width > 5:  # 只显示大于5%的标签
                plt.text(left[i] + width/2, y_positions[i], f'{width:.1f}%',
                        ha='center', va='center')
        left += widths
    
    # 在右侧添加平均分
    for i, result in enumerate(results):
        plt.text(100, i, f'平均: {result["mean"]:.1f}分',
                ha='left', va='center', fontsize=10)
    
    # 设置图表样式
    plt.yticks(y_positions, [r['role'] for r in results])
    plt.xlabel('比例 (%)')
    plt.title('不同社区角色的开源社区归属感分布', pad=15, fontsize=14)
    
    # 添加图例
    plt.legend(title='归属感评分', bbox_to_anchor=(1.15, 1), loc='upper left')
    
    plt.grid(True, axis='x', alpha=0.3)
    plt.tight_layout()
    save_plot('20_5_role_satisfaction.png')

def main():
    """主函数：执行所有绘图函数"""
    plot_opensource_tools()        # Q16
    plot_opensource_fields()       # Q17
    plot_opensource_languages()    # Q18
    plot_opensource_platforms()    # Q19
    plot_opensource_satisfaction() # Q20
    plot_role_satisfaction()       # Q20.5
    print("\n所有图表已生成完成，请查看 output 目录")

if __name__ == "__main__":
    main()