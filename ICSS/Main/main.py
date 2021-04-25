import csv
import json
import numpy
import pandas
from py2neo import Graph
import sys


def sigmoid(z):
    return 1.0 / (1 + numpy.exp(-z))


class decoder:
    def __init__(self):
        self.graph = Graph("http://localhost:7474", usergame="neo4j", password="liao123")
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
        self.size = self.len_c + self.len_u
        self.vector = numpy.zeros(self.size, dtype=numpy.int)
        bp_para = pandas.read_pickle("bp6.pkl")
        self.weights = bp_para[0]
        self.biases = bp_para[1]

    def cql_match(self, name, relationship):
        cql = "match ({name:'" + name + "'})-[name:`" + relationship + "`]->(p) where exists (p.a_id) return p"
        result = self.graph.run(cql).data()
        words = []
        for i in result:
            nodesStr = json.dumps(i['p'], ensure_ascii=False)
            nodes = json.loads(nodesStr)
            words.append([str(nodes['name']), int(nodes['a_id'])])
        return words

    def word_to_vector(self, entities, relations, sentence):
        if entities is not None and relations is not None:
            for entity in entities:
                for relation in relations:
                    words = self.cql_match(entity, relation)
                    for l in words:
                        self.vector[self.len_u + l[1]] += 1
                j = self.u_word_table.index(entity)
                self.vector[j] += 1
        elif entities is None:
            for relation in relations:
                words = self.cql_match(str(0), relation)
                for l in words:
                    self.vector[self.len_u + l[1]] += 1
        elif relations is None:
            for entity in entities:
                words = self.cql_match(entity, str(0))
                for l in words:
                    self.vector[self.len_u + l[1]] += 1
            j = self.u_word_table.index(entity)
            self.vector[j] += 1

    def feedforward(self, a):
        """
        前向传输计算每个神经元的值
        :param a:输入值
        :return:经过计算后每个神经元的值
        """
        a.resize(self.size, 1)
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(numpy.dot(w, a) + b)
        a = numpy.rint(numpy.power(10, (a * numpy.math.log(9845, 10))))-1
        return a

    def decoder(self, entities, relations, sentence):
        self.word_to_vector(entities, relations, sentence)
        result = numpy.rint(self.feedforward(self.vector))
        word_result = ""
        for i in result:
            if 0 < i < 9844:
                word_result += self.c_word_table[int(i)-1]
        print(word_result)
        return word_result


if __name__ == "__main__":
    decoder = decoder()
    # entities = ["买", "有", "没有"]
    # relations = ["少", "点"]
    # sentence = ["买", "二份", "有", "没有", "少", "点", "呀"]
    print("123465")
    decoder.decoder(sys.argv[1], sys.argv[2], sys.argv[3])
    # decoder.decoder(entities, relations, sentence)