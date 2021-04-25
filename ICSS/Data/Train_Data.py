import copy
import csv
import json
import numpy
from Data.knowledge_entity_extraction import knowledge_entity
from py2neo import Graph


class Train_Data:
    # flag:用于定义是第几万条数据
    # user_word_table:用户名词和动词词表
    def __init__(self):
        self.graph = Graph("http://localhost:7474", username="neo4j", password="liao123")
        # 读取之前已导好的neo4j_user csv文件中的内容当问句词表
        with open("D:/作业/选题/ICSS/SQLConnect/neo4j_user.csv", "r", encoding='utf8') as f:
            reader = csv.reader(f)
            result = list(reader)
            result.pop(0)
            # len(size.user_word_table)返回的值刚好为词表长度
            self.user_word_table = result
            self.u_word_table = []
            for i in self.user_word_table:
                self.u_word_table.append(i[0])
            self.len_u = len(self.u_word_table)
        # 读取之前已导好的neo4j_customer.csv文件中的内容当答句词表
        with open("D:/作业/选题/ICSS/SQLConnect/neo4j_customer.csv", "r", encoding='utf8') as f2:
            reader = csv.reader(f2)
            result = list(reader)
            result.pop(0)
            self.customer_word_table = result
            self.c_word_table = []
            for i in self.customer_word_table:
                self.c_word_table.append(i[0])
            self.len_c = len(self.c_word_table)
        self.ke = knowledge_entity()

    # 经过数据库查找，不存在有客户询问客服无回答的情况,故客户问题和客服答案可以一一对应
    # 返回句子中的词对应的特征向量和查找到的词
    def train_data(self, flag):
        # data:经过查找的问句原始词数据,其中包括词id,词名，行号和第几条句子
        data = self.ke.return_flag_question_data(flag)
        # 关系的数据
        data2 = self.ke.return_flag_relation_data(flag)
        len_data2 = len(data2)
        # size = (40000, self.len_u + self.len_c)
        # eigenvector = numpy.zeros(size)
        # 答句的数据
        answer = self.ke.return_answer_data(flag)
        len_answer = len(answer)
        size = self.len_c + self.len_u
        eigenvector = []
        eigenvector_answer = []
        new_line = numpy.zeros(size, dtype=numpy.int)
        line = 0
        # 定位词的label和sequence位置
        location = [((flag - 1) * 1000) + 1, 0]
        # 关系词
        k = 0
        # 答句
        l = 0
        flag2 = 0
        flag3 = False
        flag4 = 0
        flag5 = False
        for i in data:
            # 如果进行下一轮对话，则line+1
            # 如果换数据，则label+1且sequence归零且line+1
            if i['label'] > location[0]:
                # 特征向量后添加新的一行
                new_line_copy = copy.copy(new_line)
                eigenvector.append(new_line_copy)
                # 重置new_line
                new_line = numpy.zeros(size, dtype=numpy.int)
                print(line, location[0], location[1])
                line += 1
                flag2 = k
                flag3 = False
                flag5 = True
                last_Sequence = i['Sequence']
                last_label = i['label']
            # 如果多个问句，则sequence+2 且line+1并把上一行内容复制到该行
            elif i['Sequence'] > location[1]:
                # 特征向量后添加新的一行，但不需要重置new_line
                new_line_copy = copy.copy(new_line)
                eigenvector.append(new_line_copy)
                print(line, location[0], location[1])
                line += 1
                flag2 = k
                flag3 = False
                flag5 = True
                last_Sequence = i['Sequence']
                last_label = i['label']
            if flag5:
                l = flag4
                new_line_answer = numpy.zeros(250, dtype=numpy.int)
                while answer[l]['label'] > location[0] or answer[l]['Sequence'] > location[1] + 1:
                    l -= 1
                while answer[l]['label'] < location[0] or answer[l]['Sequence'] < location[1] + 1:
                    l += 1
                if answer[l]['label'] == location[0] and answer[l]['Sequence'] == location[1] + 1:
                    word_location = 0
                    while l < len_answer:
                        if answer[l]['label'] == location[0] and answer[l]['Sequence'] == location[1] + 1:
                            m = self.c_word_table.index(answer[l]['name'])
                            new_line_answer[word_location] = m + 1
                            word_location += 1
                            l += 1
                        else:
                            eigenvector_answer.append(new_line_answer)
                            print(location[0], location[1] + 1)
                            flag4 = l
                            flag5 = False
                            break
                location[0] = i['label']
                location[1] = i['Sequence']
            # 查找词在词表中的位置，并在对应位置+1
            j = self.u_word_table.index(i['name'])
            new_line[j] += 1
            k = flag2
            # 查找对应句子的关系词
            while k < len_data2:
                while data2[k]['label'] < i['label'] or \
                        (data2[k]['Sequence'] < i['Sequence'] and data2[k]['label'] == i['label']):
                    # 换行
                    if data2[k]['Sequence'] > last_Sequence:
                        # 特征向量后添加新的一行，但不需要重置new_line
                        new_line_copy = copy.copy(new_line)
                        eigenvector.append(new_line_copy)
                        print(line, location[0], location[1])
                        line += 1
                        flag2 = k
                        flag3 = False
                        flag5 = True
                    # 换数据
                    if data2[k]['label'] > last_label:
                        # 特征向量后添加新的一行
                        new_line_copy = copy.copy(new_line)
                        eigenvector.append(new_line_copy)
                        # 重置new_line
                        new_line = numpy.zeros(size, dtype=numpy.int)
                        print(line, location[0], location[1])
                        line += 1
                        flag2 = k
                        flag3 = False
                        flag5 = True
                    if flag5:
                        l = flag4
                        new_line_answer = numpy.zeros(250, dtype=numpy.int)
                        while answer[l]['label'] > location[0] or answer[l]['Sequence'] > location[1] + 1:
                            l -= 1
                        while answer[l]['label'] < location[0] or answer[l]['Sequence'] < location[1] + 1:
                            l += 1
                        if answer[l]['label'] == location[0] and answer[l]['Sequence'] == location[1] + 1:
                            word_location = 0
                            while l < len_answer:
                                if answer[l]['label'] == location[0] and answer[l]['Sequence'] == location[1] + 1:
                                    m = self.c_word_table.index(answer[l]['name'])
                                    new_line_answer[word_location] = m + 1
                                    word_location += 1
                                    l += 1
                                else:
                                    eigenvector_answer.append(new_line_answer)
                                    print(location[0], location[1] + 1)
                                    flag4 = l
                                    flag5 = False
                                    break
                        location[0] = data2[k]['label']
                        location[1] = data2[k]['Sequence']
                    last_Sequence = data2[k]['Sequence']
                    last_label = data2[k]['label']
                    a_words = self.cql_match(str(0), data2[k]['name'])
                    location[0] = data2[k]['label']
                    location[1] = data2[k]['Sequence']
                    # Neo4j中查询出的词在对应位置+1
                    for l in a_words:
                        new_line[self.len_u + l[1]] += 1
                    k += 1
                    if k >= len_data2:
                        break
                if k >= len_data2:
                    break
                elif data2[k]['label'] == i['label'] and data2[k]['Sequence'] == i['Sequence']:
                    a_words = self.cql_match(i['name'], data2[k]['name'])
                    # 表示句子中有关系词
                    flag3 = True
                    # Neo4j中查询出的词在对应位置+1
                    for l in a_words:
                        new_line[self.len_u + l[1]] += 1
                    k += 1
                elif data2[k]['label'] > i['label'] or data2[k]['Sequence'] > i['Sequence']:
                    break
            if not flag3:
                a_words = self.cql_match(i['name'], str(0))
                for l in a_words:
                    new_line[self.len_u + l[1]] += 1
        return eigenvector, eigenvector_answer

    def cql_match(self, name, relationship):
        cql = "match ({name:'" + name + "'})-[name:`" + relationship + "`]->(p) where exists (p.a_id) return p"
        result = self.graph.run(cql).data()
        words = []
        for i in result:
            nodesStr = json.dumps(i['p'], ensure_ascii=False)
            nodes = json.loads(nodesStr)
            words.append([str(nodes['name']), int(nodes['a_id'])])
        return words

    def return_len_u(self):
        return self.len_c + self.len_u

    def return_len_c(self):
        return self.len_c


def main():
    td = Train_Data()
    for i in range(8, 90):
        u, c = td.train_data(i)
        numpy.savetxt(str(i) + "_u.txt", u, fmt="%d")
        numpy.savetxt(str(i) + "_c.txt", c, fmt="%d")
        print(i)


if __name__ == "__main__":
    main()
