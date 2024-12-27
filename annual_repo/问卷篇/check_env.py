def check_environment():
    """检查Python环境和必要的库"""
    import sys
    print(f"Python版本: {sys.version}")
    
    try:
        import pandas as pd
        print(f"pandas版本: {pd.__version__}")
    except ImportError:
        print("pandas未安装")
    
    try:
        import matplotlib as mpl
        print(f"matplotlib版本: {mpl.__version__}")
    except ImportError:
        print("matplotlib未安装")
    
    try:
        import seaborn as sns
        print(f"seaborn版本: {sns.__version__}")
    except ImportError:
        print("seaborn未安装")
    
    try:
        import numpy as np
        print(f"numpy版本: {np.__version__}")
    except ImportError:
        print("numpy未安装")

if __name__ == "__main__":
    check_environment() 