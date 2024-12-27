import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import squarify

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

def plot_contribution_methods():
    """绘制第26题：您对开源项目的主要贡献方式"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 贡献方式标签映射
    method_labels = {
        1: '代码贡献',
        2: '文档相关贡献',
        3: '开源布道',
        4: '开源社区运营',
        5: '基于开源的\n商业化项目',
        6: '协助社区\n活动举办',
        7: '其他'
    }
    
    # 统计数据
    method_data = pd.DataFrame()
    for col in [c for c in df.columns if c.startswith('Q26|') and not c.endswith('open')]:
        option = int(col.split('|')[1])
        if option in method_labels:
            method_data[method_labels[option]] = pd.to_numeric(df[col], errors='coerce')
    
    # 计算百分比并按降序排序
    method_pcts = method_data.sum() / len(df) * 100
    method_pcts = method_pcts.sort_values(ascending=True)
    
    # 改用水平条形图
    plt.figure(figsize=(12, 6), facecolor='white')
    bars = plt.barh(range(len(method_pcts)), 
                   method_pcts.values,
                   color=COLOR_PALETTE[0])
    
    plt.yticks(range(len(method_pcts)), method_pcts.index)
    plt.xlabel('比例 (%)')
    
    # 添加数值标签
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2.,
                f'{width:.1f}%',
                ha='left', va='center')
    
    plt.title('您对开源项目的主要贡献方式', pad=15, fontsize=14)
    plt.tight_layout()
    save_plot('26_contribution_methods.png')

def plot_project_types():
    """绘制第27题：您为哪些类型的开源项目做过贡献"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 项目类型标签映射 - 删除括号中的举例
    type_labels = {
        1: '库/中间件',
        2: '通用的框架/基础设施',
        3: '完整的应用软件',
        4: '资源整合类项目、\n文档类项目',
        5: '开源社区运营\n工具项目',
        6: '其他'
    }
    
    # 统计数据
    type_data = pd.DataFrame()
    for col in [c for c in df.columns if c.startswith('Q27|') and not c.endswith('open')]:
        option = int(col.split('|')[1])
        if option in type_labels:
            type_data[type_labels[option]] = pd.to_numeric(df[col], errors='coerce')
    
    # 计算百分比并按降序排序
    type_pcts = type_data.sum() / len(df) * 100
    type_pcts = type_pcts.sort_values(ascending=True)
    
    # 改用水平条形图
    plt.figure(figsize=(12, 6), facecolor='white')
    bars = plt.barh(range(len(type_pcts)), 
                   type_pcts.values,
                   color=COLOR_PALETTE[0])
    
    plt.yticks(range(len(type_pcts)), type_pcts.index)
    plt.xlabel('比例 (%)')
    
    # 添加数值标签
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2.,
                f'{width:.1f}%',
                ha='left', va='center')
    
    plt.title('您为哪些类型的开源项目做过贡献', pad=15, fontsize=14)
    plt.tight_layout()
    save_plot('27_project_types.png')

def plot_programming_languages():
    """绘制第28题：在开源项目贡献中您最常用的开发语言是"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 编程语言标签映射
    language_labels = {
        1: '汇编语言', 2: 'Bash/Shell/PowerShell', 3: 'C/C++', 4: 'C#',
        18: 'Python', 12: 'Java', 13: 'JavaScript', 5: 'Clojure',
        6: 'Dart', 7: 'Elixir', 8: 'Erlang', 9: 'F#', 10: 'Go',
        11: 'HTML/CSS', 14: 'MATLAB', 15: 'Objective-C', 16: 'PHP',
        17: 'Perl', 19: 'R', 20: 'Ruby', 21: 'Rust', 22: 'Scala',
        23: 'SQL', 24: 'Swift', 25: 'TypeScript', 26: 'VBA',
        27: 'WebAssembly', 28: '其他'
    }
    
    # 统计数据
    language_data = pd.DataFrame()
    for col in [c for c in df.columns if c.startswith('Q28|') and not c.endswith('open')]:
        option = int(col.split('|')[1])
        if option in language_labels:
            language_data[language_labels[option]] = pd.to_numeric(df[col], errors='coerce')
    
    # 计算百分比并排序
    language_pcts = language_data.sum() / len(df) * 100
    language_pcts = language_pcts.sort_values(ascending=True)
    
    # 只显示使用比例大于1%的语言
    language_pcts = language_pcts[language_pcts > 1]
    
    # 创建水平条形图，使用渐变色
    plt.figure(figsize=(12, 8), facecolor='white')
    
    # 创建渐变色
    colors = plt.cm.Blues(np.linspace(0.3, 0.9, len(language_pcts)))
    
    bars = plt.barh(range(len(language_pcts)), 
                   language_pcts.values,
                   color=colors)
    
    plt.yticks(range(len(language_pcts)), language_pcts.index)
    plt.xlabel('比例 (%)')
    
    # 添加数值标签
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2.,
                f'{width:.1f}%',
                ha='left', va='center')
    
    plt.title('在开源项目贡献中最常用的开发语言（使用率>1%）', pad=15, fontsize=14)
    plt.tight_layout()
    save_plot('28_programming_languages.png')

def plot_incentive_types():
    """绘制第29题：请评价以下激励方式对您开源贡献的影响程度"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 激励方式标签映射
    incentive_labels = {
        3: '物质激励\n(现金、奖品等)',
        4: '荣誉激励\n(社区荣誉)',
        5: '授权激励\n(获得更多的社区决策权)',
        6: '社交激励\n(在社区中认识到朋友)',
        7: '职业激励\n(获得更好的晋升机会)'
    }
    
    # 创建热力图数据
    scores = []
    for option in sorted(incentive_labels.keys()):
        col = f'Q29|{option}'
        score_dist = pd.to_numeric(df[col], errors='coerce').value_counts(normalize=True) * 100
        scores.append([score_dist.get(i, 0) for i in range(1, 6)])
    
    # 改用分组条形图
    plt.figure(figsize=(12, 6), facecolor='white')
    
    x = np.arange(len(incentive_labels))
    width = 0.15
    
    for i in range(5):
        score_data = [scores[j][i] for j in range(len(scores))]
        plt.bar(x + i*width, score_data, width, 
               label=f'{i+1}分',
               color=COLOR_PALETTE[0],
               alpha=0.2 + i*0.2)
    
    plt.ylabel('比例 (%)')
    plt.xlabel('激励方式')
    plt.title('不同激励方式的影响程度分布', pad=15, fontsize=14)
    
    plt.xticks(x + width*2, [incentive_labels[k] for k in sorted(incentive_labels.keys())],
               rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    save_plot('29_incentive_types.png')

def plot_financial_returns():
    """绘制第30题：您参与开源的财务回报来源"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 回报来源标签映射
    return_labels = {
        1: '没有财务回报',
        2: '薪酬/工资',
        3: '悬赏/奖励',
        4: '广告收入',
        5: '捐赠',
        6: '专利或知识产权收益',
        7: '服务收入\n(基于开源项目由个人或\n公司提供的商业服务)',
        8: '其他'
    }
    
    # 统计数据
    return_data = pd.DataFrame()
    for col in [c for c in df.columns if c.startswith('Q30|') and not c.endswith('open')]:
        option = int(col.split('|')[1])
        if option in return_labels:
            return_data[return_labels[option]] = pd.to_numeric(df[col], errors='coerce')
    
    # 计算百分比
    return_pcts = return_data.sum() / len(df) * 100
    return_pcts = return_pcts.sort_values(ascending=True)
    
    # 使用简单的水平条形图
    plt.figure(figsize=(12, 6), facecolor='white')
    bars = plt.barh(range(len(return_pcts)), 
                   return_pcts.values,
                   color=COLOR_PALETTE[0])
    
    plt.yticks(range(len(return_pcts)), return_pcts.index)
    plt.xlabel('比例 (%)')
    
    # 添加数值标签
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2.,
                f'{width:.1f}%',
                ha='left', va='center')
    
    plt.title('您参与开源的财务回报来源', pad=15, fontsize=14)
    plt.tight_layout()
    save_plot('30_financial_returns.png')

def main():
    """主函数：执行所有绘图函数"""
    plot_contribution_methods()         # Q26
    plot_project_types()               # Q27
    plot_programming_languages()        # Q28
    plot_incentive_types()             # Q29
    plot_financial_returns()            # Q30
    print("\n所有图表已生成完成，请查看 output 目录")

if __name__ == "__main__":
    main() 