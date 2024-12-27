import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
from wordcloud import WordCloud
import jieba

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

def plot_evaluation_criteria():
    """绘制第36题：您认为在您心中哪些指标用于评价开源项目"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 评价指标标签映射
    criteria_labels = {
        1: '开发者是否具有权威性',
        2: '项目是否具有影响力、\n是否受大众欢迎',
        3: '是否有大公司背书',
        4: '项目以及社区的活跃程度',
        5: '是否有持续的更新和维护',
        6: '其他'
    }
    
    # 统计数据
    criteria_data = pd.DataFrame()
    for col in [c for c in df.columns if c.startswith('Q36|') and not c.endswith('open')]:
        option = int(col.split('|')[1])
        if option in criteria_labels:
            criteria_data[criteria_labels[option]] = pd.to_numeric(df[col], errors='coerce')
    
    # 计算百分比并排序
    criteria_pcts = criteria_data.sum() / len(df) * 100
    criteria_pcts = criteria_pcts.sort_values(ascending=True)
    
    # 绘制水平条形图
    plt.figure(figsize=(12, 6), facecolor='white')
    bars = plt.barh(range(len(criteria_pcts)), 
                   criteria_pcts.values,
                   color=COLOR_PALETTE[0])
    
    plt.yticks(range(len(criteria_pcts)), criteria_pcts.index)
    plt.xlabel('比例 (%)')
    
    # 添加数值标签
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2.,
                f'{width:.1f}%',
                ha='left', va='center')
    
    plt.title('您认为哪些指标用于评价开源项目', pad=15, fontsize=14)
    plt.tight_layout()
    save_plot('36_evaluation_criteria.png')

def plot_ai_models():
    """绘制第37题：您使用的大模型产品主要是哪些？"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # AI模型标签映射
    model_labels = {
        15: 'LLaMA (Meta)',
        16: 'Claude (Anthropic)',
        17: 'GPT系列 (如GPT-3、GPT-4)',
        10: 'OpenLLaMA',
        11: 'RoBERTa',
        12: 'BERT',
        13: 'BLOOM',
        14: 'GPT系列开源实现\n(如GPT-3、GPT-4开源实现)',
        5: '百度千帆大模型',
        6: '讯飞星火',
        7: '阿里模型服务矩阵',
        3: '通义千问',
        8: '腾讯混元大模型',
        9: '科大讯飞星火大模型',
        4: '智谱清言 (Zhipu AI)',
        1: 'ChatGLM系列\n(如ChatGLM-6B、ChatGLM2-6B)',
        2: 'MOSS',
        18: 'AI代码生成工具\n(如: Cursor, Devin, Copilot等)',
        19: '没使用过大模型',
        20: '其他'
    }
    
    # 统计数据
    model_data = pd.DataFrame()
    for col in [c for c in df.columns if c.startswith('Q37|') and not c.endswith('open')]:
        option = int(col.split('|')[1])
        if option in model_labels:
            model_data[model_labels[option]] = pd.to_numeric(df[col], errors='coerce')
    
    # 计算百分比并排序
    model_pcts = model_data.sum() / len(df) * 100
    model_pcts = model_pcts.sort_values(ascending=True)
    
    # 绘制水平条形图
    plt.figure(figsize=(12, 8), facecolor='white')
    bars = plt.barh(range(len(model_pcts)), 
                   model_pcts.values,
                   color=COLOR_PALETTE[0])
    
    plt.yticks(range(len(model_pcts)), model_pcts.index)
    plt.xlabel('比例 (%)')
    
    # 添加数值标签
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2.,
                f'{width:.1f}%',
                ha='left', va='center')
    
    plt.title('您使用的大模型产品主要是哪些？', pad=15, fontsize=14)
    plt.tight_layout()
    save_plot('37_ai_models.png')

def plot_ai_impact():
    """绘制第38题：您认为人工智能对开源项目/社区的最重要影响是什么？"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 影响标签映射
    impact_labels = {
        1: '推动跨学科合作，\n拓展新兴领域的开源项目',
        2: '提升代码生成和审查的效率',
        3: '加快开发者学习和创新的速度',
        4: '自动化常见开发任务，\n减少重复性劳动',
        5: '帮助社区成员进行技术问题的解答与指导',
        6: '通过智能管理系统优化\n项目的资源分配和调度',
        7: '产生更多低质量或重复性项目',
        8: '加剧对AI模型的依赖，\n降低开发者自主编程能力',
        9: '其他'
    }
    
    # 统计数据
    valid_responses = df['Q38'].dropna()
    valid_responses = valid_responses[valid_responses.isin(impact_labels.keys())]
    
    impact_counts = valid_responses.value_counts()
    impact_pcts = impact_counts / len(valid_responses) * 100
    
    # 过滤掉0值并按百分比降序排序
    impact_pcts = impact_pcts[impact_pcts > 0].sort_values(ascending=True)
    
    # 转换标签
    impact_pcts.index = [impact_labels[i] for i in impact_pcts.index]
    
    # 绘制水平条形图
    plt.figure(figsize=(12, 8), facecolor='white')
    bars = plt.barh(range(len(impact_pcts)), 
                   impact_pcts.values,
                   color=COLOR_PALETTE[0])
    
    plt.yticks(range(len(impact_pcts)), impact_pcts.index)
    plt.xlabel('比例 (%)')
    
    # 添加数值标签
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2.,
                f'{width:.1f}%',
                ha='left', va='center')
    
    plt.title('您认为人工智能对开源项目/社区的最重要影响是什么？', pad=15, fontsize=14)
    plt.tight_layout()
    save_plot('38_ai_impact.png')

def plot_llm_challenges():
    """绘制第39题：您认为开源大模型在发展过程中最需要解决的技术挑战有哪些"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 挑战标签映射
    challenge_labels = {
        1: '降低模型的训练与使用成本',
        2: '提高模型的透明度与可解释性',
        3: '消除模型中的数据偏见和伦理问题',
        4: '改进大模型在实际应用中的\n可控性与安全性',
        5: '提供更多可复用的开源模型和工具包',
        6: '增强大模型在开源社区的\n可访问性和共享机制',
        7: '其他'
    }
    
    # 统计数据
    challenge_data = pd.DataFrame()
    for col in [c for c in df.columns if c.startswith('Q39|') and not c.endswith('open')]:
        option = int(col.split('|')[1])
        if option in challenge_labels:
            challenge_data[challenge_labels[option]] = pd.to_numeric(df[col], errors='coerce')
    
    # 计算百分比并排序
    challenge_pcts = challenge_data.sum() / len(df) * 100
    challenge_pcts = challenge_pcts.sort_values(ascending=True)
    
    # 绘制水平条形图
    plt.figure(figsize=(12, 6), facecolor='white')
    bars = plt.barh(range(len(challenge_pcts)), 
                   challenge_pcts.values,
                   color=COLOR_PALETTE[0])
    
    plt.yticks(range(len(challenge_pcts)), challenge_pcts.index)
    plt.xlabel('比例 (%)')
    
    # 添加数值标签
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2.,
                f'{width:.1f}%',
                ha='left', va='center')
    
    plt.title('您认为开源大模型在发展过程中最需要解决的技术挑战有哪些', pad=15, fontsize=14)
    plt.tight_layout()
    save_plot('39_llm_challenges.png')

def plot_keywords_cloud():
    """绘制第40题：您认为2024年的开源关键词（词云图）"""
    df = pd.read_csv('2024 中国开源参与情况问卷调查_数据详情表_编码数据_202412111519.csv', encoding='gb18030')
    
    # 获取所有关键词并合并
    keywords = df['Q40'].dropna().astype(str).str.cat(sep=' ')
    
    # 使用jieba分词
    words = jieba.cut(keywords)
    word_space_split = ' '.join(words)
    
    # 创建词云
    wordcloud = WordCloud(
        font_path='simhei.ttf',  # 使用黑体
        width=1200,
        height=800,
        background_color='white',
        max_words=100,
        colormap='Blues'  # 使用蓝色系配色
    ).generate(word_space_split)
    
    # 绘制词云图
    plt.figure(figsize=(15, 10), facecolor='white')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('2024年开源关键词', pad=20, fontsize=16)
    plt.tight_layout()
    save_plot('40_keywords_cloud.png')

def main():
    """主函数：执行所有绘图函数"""
    plot_evaluation_criteria()      # Q36
    plot_ai_models()               # Q37
    plot_ai_impact()               # Q38
    plot_llm_challenges()          # Q39
    plot_keywords_cloud()          # Q40
    print("\n所有图表已生成完成，请查看 output 目录")

if __name__ == "__main__":
    main() 