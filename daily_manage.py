import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams

TXTFILENAME = "项目实例\英语单词听写\daily_record.txt"
JSONFILE = "项目实例\英语单词听写\json_daily.json"

rcParams['font.sans-serif'] = ['SimHei']
rcParams['axes.unicode_minus'] = False

def show_all_daily():
    print("您全部的听写记录如下:")
    with open(TXTFILENAME,"r",encoding="utf-8") as f:
        content = f.read()
        print(content)
    
def data_analysis():
    print("我们将为您展示近几次的听写数据")
    
    survey_df = pd.read_json(JSONFILE)
    sns.lineplot(survey_df,x=1,y=4)
    plt.title("近几次的正确率")
    plt.show()
    return survey_df

if __name__ == "__main__":
    data_analysis()