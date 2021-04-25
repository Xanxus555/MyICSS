import json

from py2neo import Graph

graph = Graph("http://localhost:7474", username="neo4j", password="liao123")
print("连接数据库成功")
print("开始删除原有数据库")
graph.delete_all()
print("删除原有数据库成功")
cql = "USING PERIODIC COMMIT 5000 LOAD CSV WITH HEADERS FROM 'file:///neo4j_user.csv' AS row " \
      "CALL apoc.cypher.doIt('CREATE(n:'+row.LABEL+'{name:$name,q_id:'+row.q_id+'})'," \
      "{name:row.name}) YIELD value return 1"
graph.run(cql)
print("问句实体导入成功")
cql = "USING PERIODIC COMMIT 5000 LOAD CSV WITH HEADERS FROM 'file:///neo4j_customer.csv' AS row " \
      " CALL apoc.cypher.doIt('MERGE(n:'+row.LABEL+'{name:$name}) ON CREATE SET n.a_id = '+row.a_id" \
      "+'ON MATCH SET n.a_id = '+row.a_id,{name:row.name}) YIELD value return 1"
graph.run(cql)
print("答句实体导入成功")
cql = "USING PERIODIC COMMIT 5000 LOAD CSV WITH HEADERS FROM 'file:///neo4j_user_to_customer_after.csv' AS row" \
      " match (a) where a.name=row.START_NAME" \
      " match (b) where b.name=row.END_NAME" \
      " call apoc.merge.relationship(a,row.TYPE,{},{},b) yield rel return count(*)"
graph.run(cql)
print("关系导入成功")
