import pickle

import numpy
import numpy as np
import pandas
from cffi.backend_ctypes import xrange
from numpy import random

from Data.Train_Data import Train_Data
from TrainModel import mnist_loader


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


class BP:
    def __init__(self, sizes, biases=None, weights=None, max_output=None, similarity_degree=None):
        """
        :param size: list属性，存储神经网络的神经元个数
        """
        self.max_log = np.math.log(max_output, 10)
        # 有几层神经网络
        self.num_layers = len(sizes)
        self.sizes = sizes
        if biases is None:
            # 除去输入层，随机产生每层中 y 个神经元的 biase 值（0 - 1）
            self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        else:
            self.biases = biases
        if weights is None:
            # 随机产生每条连接线的 weight 值（0 - 1）
            self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]
        else:
            self.weights = weights
        self.max_output = max_output
        if similarity_degree is None:
            self.similarity_degree = []
        else:
            self.similarity_degree = similarity_degree

    def feedforward(self, a):
        """
        前向传输计算每个神经元的值
        :param a:输入值
        :return:经过计算后每个神经元的值
        """
        a.resize(self.sizes[0], 1)
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a) + b)
        return a

    def SGD(self, epochs, lr, test_input_data=None, test_output_data=None):
        """
        随机梯度下降

        :param epochs:迭代次数
        :param lr:学习率
        :param test_input_data:输入端测试集
        :param test_output_data:输出端测试集
        :return:
        """
        if test_input_data is not None:
            n_test = test_input_data.shape[0]
        shunxu = np.zeros(30, dtype=int)
        for i in xrange(30):
            shunxu[i] = int(i + 1)
        for epoch in xrange(epochs):
            # 搅乱数据集
            random.shuffle(shunxu)
            for i in shunxu:
                # 读取对应的数据
                input_arr = numpy.loadtxt("D:/作业/选题/ICSS/Data/" + str(i) + "_u.txt")
                output_arr = numpy.loadtxt("D:/作业/选题/ICSS/Data/" + str(i) + "_c.txt")
                i_size = input_arr.shape
                o_size = output_arr.shape
                # 如果数据行数对不上，则证明数据中存在问题
                if i_size[0] != o_size[0]:
                    continue
                # n = len(input_arr)
                # 按照小样本数量划分训练集
                # mini_batch_size = 4
                # input_mini_batches = [input_arr[k:k + mini_batch_size] for k in xrange(0, n, mini_batch_size)]
                # output_mini_batches = [output_arr[k:k + mini_batch_size] for k in xrange(0, n, mini_batch_size)]
                # for input_mini_batch, output_mini_batch in zip(input_mini_batches, output_mini_batches):
                #     根据每个小样本来更新 w 和 b，代码在下一段
                    # self.update_mini_batch(input_mini_batch, np.log10(output_mini_batch + 1) / self.max_log, lr)
                self.update_mini_batch(input_arr, np.log10(output_arr + 1) / self.max_log, lr)
                print(i)
                with open("bp6.pkl", "wb") as file:
                    similarity_degree = self.evaluate(test_input_data, test_output_data)
                    self.similarity_degree.append(similarity_degree)
                    para = (self.weights, self.biases, similarity_degree)
                    pickle.dump(para, file)
                    print(similarity_degree)
            if test_input_data is not None:
                print("Epoch {0}: {1} / {2}".format(epoch, self.evaluate(test_input_data, test_output_data), n_test))
            else:
                print("Epoch {0} complete".format(epoch))
        # for j in xrange(epochs):
        #     # 搅乱训练集，让其排序顺序发生变化
        #     random.shuffle(training_data)
        #     # 按照小样本数量划分训练集
        #     mini_batches = [
        #         training_data[k:k + mini_batch_size]
        #         for k in xrange(0, n, mini_batch_size)]
        #     for mini_batch in mini_batches:
        #         # 根据每个小样本来更新 w 和 b，代码在下一段
        #         self.update_mini_batch(mini_batch, lr)
        #     # 输出测试每轮结束后，神经网络的准确度
        #     if test_data:
        #         print("Epoch {0}: {1} / {2}".format(j, self.evaluate(test_data), n_test))
        #     else:
        #         print("Epoch {0} complete".format(j))

    def update_mini_batch(self, input_arr, output_arr, eta):
        """
        更新 w 和 b 的值
        :param input_arr: 输入
        :param output_arr: 输出
        :param eta: 学习率
        """
        for x, y in zip(input_arr, output_arr):
            # 根据样本中的每一个输入 x 的其输出 y，计算 w 和 b 的偏导数
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            # 更新根据偏导值更新 w 和 b
            self.weights = [w + eta * nw
                            for w, nw in zip(self.weights, delta_nabla_w)]
            self.biases = [b + eta * nb
                           for b, nb in zip(self.biases, delta_nabla_b)]

    def backprop(self, x, y):
        """
        :param x:
        :param y:
        :return:
        """
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        # 前向传输
        activation = x.reshape((self.sizes[0], 1))
        a = x.reshape((self.sizes[0], 1))
        y2 = y.reshape((self.sizes[-1], 1))
        # 储存每层的神经元的值的矩阵，下面循环会 append 每层的神经元的值
        activations = [a]
        # 储存每个未经过 sigmoid 计算的神经元的值
        zs = []
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation) + b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
        # 求 δ 的值
        delta = self.cost_derivative(y2, activations[-1]) * self.derivate(activations[-1])
        nabla_b[-1] = delta
        # 乘于前一层的输出值
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())
        for l in xrange(2, self.num_layers):
            # 从倒数第 l 层开始更新，-l 是 python 中特有的语法表示从倒数第 l 层开始计算
            # 下面这里利用 l+1 层的 δ 值来计算 l 的 δ 值
            z = activations[-l]
            sp = self.derivate(z)
            delta = np.dot(self.weights[-l + 1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l - 1].transpose())
        return nabla_b, nabla_w

    def evaluate(self, test_input_data, test_output_data):
        # 获得预测结果
        test_results = [(np.rint(np.power(10, (self.feedforward(x) * self.max_log))) - 1, y)
                        for (x, y) in zip(test_input_data, test_output_data)]
        num = 0
        num_all = 0
        t = 0
        for (x, y) in test_results:
            for x1, y1 in zip(x, y):
                num_all += 1
                if x1 != 0 and x1 != 9844:
                    t += 1
                if x1 == y1:
                    num += 1
        # 返回正确识别的个数
        print(t)
        return num / num_all

    def cost_derivative(self, output_activations, y):
        """损失计算函数"""
        error = output_activations - y
        return error

    def derivate(self, output_activation):
        return (1 - output_activation) * output_activation


def main(learing_rate=0.2, training_epochs=100):
    td = Train_Data()
    # 输出层的最大值
    max_output = td.return_len_c()
    # 输入层的神经元个数
    n_input = td.return_len_u()
    # 输出层神经元个数
    n_output = 250
    # 隐藏层神经元个数
    n_hidden1 = int(np.rint(numpy.math.sqrt(n_output * n_input)))
    # n_hidden2 = n_hidden1
    # n_hidden1 = 9845
    # 初始化BP神经网络
    # size = [n_input, n_hidden1, n_hidden1, n_hidden1, n_output]
    size = [n_input, n_output]
    # bpnet = BP(size, max_output=max_output)
    bp_para = pandas.read_pickle("bp6.pkl")
    bpnet = BP(size, weights=bp_para[0], biases=bp_para[1], max_output=max_output, similarity_degree=bp_para[2])
    # 测试集内容
    input_arr = numpy.loadtxt("D:/作业/选题/ICSS/Data/1_u.txt")
    output_arr = numpy.loadtxt("D:/作业/选题/ICSS/Data/1_c.txt")
    # e = bpnet.evaluate(test_input_data=input_arr, test_output_data=output_arr)
    # print(e)
    bpnet.SGD(training_epochs, learing_rate, input_arr, output_arr)


main()
