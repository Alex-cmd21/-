# 单词听写
import json
import random
import daily_manage
from datetime import datetime 

def is_all_chinese(s):
    return all('\u4e00' <= ch <= '\u9fff' for ch in s) and len(s) > 1


FILENAME = "项目实例\英语单词听写\\vocabulary_test.json"
DAILY_FILE = "项目实例\英语单词听写\daily_record.txt"
JSON_DAILY = "项目实例\英语单词听写\json_daily.json"

def load_json():
    with open(JSON_DAILY,"r",encoding="utf-8") as f:
        daily = json.load(f)
        return daily

def load_words():
    with open(FILENAME,"r",encoding="utf-8") as f:
        return json.load(f) #获取列表，内部列表按序号排序对应单元

     
def show_and_save_result(unit,right,wronglist):
    now = datetime.now()
    time_str = now.strftime("%Y-%m-%d %H:%M")
    counts = len(wronglist) + right
    rightrate = right / counts
    print(f"日期：{time_str}\n您这次听写第{unit}单元，总共听写了{counts}个单词，正确率为{rightrate:.0%}")
    print("以下单词可能您还要进一步强化")
    i = 1
    for chinese,english in wronglist.items():
        print(f"{i}.{chinese}:{english}\n")
        i += 1
        
    #保存日志
    with open(DAILY_FILE , "a" ,encoding="utf-8") as f:
        f.write("\n\n")  # 两个空行易于阅读
        f.write(f"第{unit}单元听写\n时间:{time_str}\n总共听写了{counts}个单词，正确率为{rightrate:.0%}\n下面是您错的单词\n")
        i = 1
        for id,content in wronglist.items():
            f.write(f"{i}.{id}:{content}\n")
            i += 1 
        f.write("\n\n")  
    print("日志已经更新保存")
    
    #保存json格式文件
    daily = load_json() #daily为列表格式
    with open(JSON_DAILY,"w",encoding="utf-8") as f:
        lst = [unit,time_str,counts,len(wronglist),len(wronglist) / counts,wronglist]
        daily.append(lst)        
        json.dump(daily, f, ensure_ascii=False, indent=4)
        print("json格式已经保存")


def choose_word_pool(words_pool):
    for num,words in enumerate(words_pool,start=1):
        words = list(words.keys())
        if len(words) > 10:
            print(f"第{num}单元:{words[0]},{words[1]},.....,{words[-1]}")
        else:
            print(f"第{num}单元:{",".join(words)}")
    while True:
        choice = int(input("请选择您想报听写的单元:"))
        if 0 < choice <= len(words_pool):
            print("单词池已经准备就绪！")
            return words_pool[choice - 1],choice
        else:
            print("请在单元范围内输入")


def start_word_listen(words_pool):
    print("听写开始！")
    right = 0 
    wronglist = {}
    while words_pool:
        word_key = random.choice(list(words_pool.keys()))
        word_mean = words_pool[word_key]
        del words_pool[word_key]
        chance = 3
        while True:            
            my_answer = input(f"{word_key}:")        
            if is_all_chinese(my_answer):
                if my_answer in word_mean:
                    print(f"您的答案是正确的，它的全部意思是{word_key}:{word_mean}")
                    right = right + 1
                    break
                elif my_answer == "不知道":
                    print(f"这个单词似乎没记住呢，它的意思是{word_key}:{word_mean}")
                    wronglist[word_key] = word_mean
                    break
                else:
                    chance -= 1
                    if chance == 0:
                        print(f"这个单词似乎没记住呢，它的意思是{word_key}:{word_mean}")
                        wronglist[word_key] = word_mean
                        break
                    print(f"您的答有误，您还有{chance}次机会")
            else:
                print("请输入正确的格式")
    print("--------------------------------------------------------------------------")
    print("听写已经全部结束！以下是您的听写数据，数据已经写入日志")
    return right,wronglist 


def save_word(words_pool):
    with open(FILENAME,"w",encoding="utf-8") as f:
        json.dump(words_pool, f, ensure_ascii=False, indent=4)


def main():
    print("""
             1.选择单元报单词
             2.新增单词本(也可补充旧单词本)
             3.查看艾斯浩宾曲线记忆时间
             4.进行随机听写
             5.设置单词日程安排提醒
             6.查看往期听写记录
             """)
    
    choice = input("请输入您要进行的操作：")
    
    if choice == '1':
        words_pool = load_words()
        words_list,unit = choose_word_pool(words_pool)
        right,wronglist =start_word_listen(words_list)
        show_and_save_result(unit,right,wronglist)
    else:
        print("目前功能正在开发。。。。")
if __name__ == "__main__":
    main()
    