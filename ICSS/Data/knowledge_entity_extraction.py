import pymysql


class knowledge_entity:
    def __init__(self):
        # 连接mysql数据库
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='liao123.',
            db='dataset',
            charset='utf8',
            # 关闭自动提交数据库语句功能
            autocommit='false',
            # 字典形式获得数据库中数据
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cur = self.conn.cursor()

    def return_word_dict_list(self):
        # 获取词性为名词和动词的问句词典
        sql = "select name,part,count(name) from word" \
              " where q_or_a = 0 and name != '' and" \
              "(part like '/v%' or part like '/n%')" \
              "group by name,part order by count(name) desc"
        self.cur.execute(sql)
        word_dict_list = self.cur.fetchall()
        return word_dict_list

    def return_word_list(self):
        # 获取词性为名词和动词的词，词性以及词的数据位置
        sql = "select name,part,label,Sequence from word" \
              " where (part like '/v%' or part like '/n%') and name != '' " \
              " and q_or_a = 0"
        self.cur.execute(sql)
        word_list = self.cur.fetchall()
        return word_list

    def return_relation_word_list(self):
        # 获取词性为形容词的词，词性以及词的数据位置
        sql = "select name,part,label,Sequence from word" \
              " where (part like '/a%' or part like '/q%' or part like '/d%')" \
              " and name!='' " \
              " and q_or_a = 0"
        self.cur.execute(sql)
        relationship_word_list = self.cur.fetchall()
        return relationship_word_list

    def return_a_word_list(self):
        # 获取所有词(客服回答)的词性，以及词的数据位置
        sql = "select name,part,label,Sequence from word " \
              " where q_or_a = 1 and name != '' and part !=''"
        self.cur.execute(sql)
        a_word_list = self.cur.fetchall()
        return a_word_list

    def return_customer_word_list(self):
        # 获取答句词典
        sql = "select name,part,count(name) from word" \
              " where q_or_a = 1 and name != '' and part!='' " \
              " group by name,part order by count(name) desc"
        self.cur.execute(sql)
        customer_dict = self.cur.fetchall()
        return customer_dict

    # 返回第(flag-1)*100---flag*100条数据
    def return_flag_question_data(self, flag):
        sql = "select id,name,label,Sequence from word" \
              " where (part like '/v%' or part like '/n%') and" \
              " q_or_a = 0 and name!='' and part != '' and " \
              " label > "+str((flag-1)*1000)+" and label <="+str(flag*1000)
        self.cur.execute(sql)
        name_data = self.cur.fetchall()
        return name_data

    def return_flag_relation_data(self, flag):
        sql = "select id,name,label,Sequence from word" \
              " where q_or_a = 0 and" \
              " (part like '/a%' or part like '/q%' or part like '/d%')" \
              " and name!='' and" \
              " label > " + str((flag - 1) * 1000) + " and label <=" + str(flag * 1000)
        self.cur.execute(sql)
        name_data = self.cur.fetchall()
        return name_data

    def return_answer_data(self, flag):
        sql = "select id,name,label,Sequence from word where q_or_a = 1 and name != '' and part != '' and " \
              "label > " + str((flag - 1) * 1000) + " and label <=" + str(flag * 1000)
        self.cur.execute(sql)
        name_data = self.cur.fetchall()
        return name_data

    def return_test_answer(self):
        sql = "select id,name,label,Sequence from word where q_or_a = 1 and name != '' and part != '' and " \
              "label > 89000 and label <= 90000"
        self.cur.execute(sql)
        data = self.cur.fetchall()
        return data

