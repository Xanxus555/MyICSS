import csv
from Data.knowledge_entity_extraction import knowledge_entity
import pandas as pd

ke = knowledge_entity()
word_list = ke.return_word_list()
word_dict_list = ke.return_word_dict_list()
relationship = ke.return_relation_word_list()
a_word_list = ke.return_a_word_list()
customer_list = ke.return_customer_word_list()
with open("neo4j_user.csv", "w", newline='', encoding='utf8') as csvfile:
    writer = csv.writer(csvfile)
    # 写入列名
    writer.writerow(['name', 'LABEL', 'q_id'])
    t = 0
    for i in word_dict_list:
        writer.writerow([i['name'], i['part'][1:], t])
        t += 1
    writer.writerow(['0', 'NULL', t])
    print('问句实体导成csv文件成功')
with open("neo4j_customer.csv", "w", newline='', encoding='utf8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['name', 'LABEL', 'a_id'])
    t = 0
    for i in customer_list:
        writer.writerow([i['name'], i['part'][1:], t])
        t += 1
    print('答句实体导成csv文件成功')
with open("neo4j_user_to_customer.csv", "w", newline='', encoding='utf8') as csvfile:
    num = 0
    writer = csv.writer(csvfile)
    writer.writerow(['START_NAME', 'END_NAME', 'TYPE'])
    # 用于记录a_word_list的位置
    flag = 0
    # 用于记录relation的位置
    flag2 = 0
    # 用于记录是否有属性插入
    flag3 = False
    last_Sequence = 0
    last_label = 0
    j = 0
    k = 0
    # 循环问句词
    for i in range(len(word_list)):
        if i != 0:
            last_Sequence = word_list[i-1]['Sequence']
            last_label = word_list[i-1]['label']
        this_Sequence = word_list[i]['Sequence']
        this_label = word_list[i]['label']
        if this_Sequence - last_Sequence >= 2:
            flag2 = k
            flag3 = False
        if this_label - last_label >= 1:
            flag = j
            flag2 = k
            flag3 = False
        j = flag
        # 循环答句词
        while j < len(a_word_list):
            flag3 = False
            if word_list[i]['label'] == a_word_list[j]['label'] and word_list[i]['Sequence'] + 1 == \
                    a_word_list[j]['Sequence']:
                k = flag2
                # 循环关系词
                while k < len(relationship):
                    if word_list[i]['label'] == relationship[k]['label'] and word_list[i]['Sequence'] == \
                            relationship[k]['Sequence']:
                        writer.writerow([word_list[i]['name'], a_word_list[j]['name'], relationship[k]['name']])
                        num += 1
                        flag3 = True
                    elif relationship[k]['label'] > word_list[i]['label'] or (relationship[k]['Sequence'] > \
                        word_list[i]['Sequence'] and relationship[k]['label'] == word_list[i]['label']):
                        break
                    k += 1
                # 如果没有链接属性，则直接插入一个空值
                if not flag3:
                    writer.writerow([word_list[i]['name'], a_word_list[j]['name'], '0'])
                    num += 1
            # 换数据
            if word_list[i]['label'] < a_word_list[j]['label'] or (this_Sequence+1 < a_word_list[j]['Sequence'] and this_label == a_word_list[j]['label']):
                break
            j += 1
    # 用于记录relation的位置
    flag = 0
    # 用于记录word_list的位置
    flag2 = 0
    # 用于记录是否有属性插入
    flag3 = False
    last_Sequence = 0
    last_label = 1
    j = 0
    k = 0
    # 循环答句词
    for i in range(len(a_word_list)):
        if i != 0:
            last_Sequence = a_word_list[i-1]['Sequence']
            last_label = a_word_list[i-1]['label']
        this_Sequence = a_word_list[i]['Sequence']
        this_label = a_word_list[i]['label']
        if this_Sequence - last_Sequence >= 2:
            flag2 = k
            flag3 = False
        if this_label - last_label == 1:
            flag = j
            flag2 = k
            flag3 = False
        j = flag
        # 循环关系词
        while j < len(relationship):
            if a_word_list[i]['label'] == relationship[j]['label'] and a_word_list[i]['Sequence'] - 1 == \
                    relationship[j]['Sequence']:
                k = flag2
                # 循环问句词
                while k < len(word_list):
                    if relationship[j]['label'] == word_list[k]['label'] and relationship[j]['Sequence'] == \
                            word_list[k]['Sequence']:
                        # 有问句词
                        writer.writerow([word_list[k]['name'], a_word_list[i]['name'], relationship[j]['name']])
                        num += 1
                        flag3 = True
                    elif word_list[k]['label'] > relationship[j]['label'] or (word_list[k]['Sequence'] > \
                        relationship[j]['Sequence'] and word_list[k]['label'] == relationship[j]['label']):
                        break
                    k += 1
                # 如果没有链接属性，则直接插入一个空值
                if not flag3:
                    writer.writerow(['0', a_word_list[i]['name'], relationship[j]['name']])
                    num += 1
            # 换数据
            if this_label < relationship[j]['label'] or (this_Sequence < relationship[j]['Sequence'] and this_label == relationship[j]['label']):
                break
            j += 1
    print(num)
    print('关系导成CSV成功')
print('开始整理关系CSV')
frame = pd.read_csv('neo4j_user_to_customer.csv')
data = frame.drop_duplicates(subset=None, keep='first')
data.to_csv('neo4j_user_to_customer_after.csv', encoding='utf8', index=False)
print('去除关系CSV重复列完成')
