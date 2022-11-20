# -*- coding = utf-8 -*-
# @Time : 2022/7/12 16:55
# @Author: shrgginG
# @File : test_py2neo4j.py
# @Software: PyCharm

from py2neo import Graph, Node, Relationship, NodeMatcher, Subgraph

graph = Graph("bolt://121.4.128.151:7687", auth=("neo4j", "123456"))
# a = Node("Person", name="Alice")
# b = Node("Person", name="Bob")
# ab = Relationship(a, "KNOWS", b)
# graph.create(ab)

tx = graph.begin()

'MERGE (d) -[:{} ]-> (:Domain {{ fqdn: \"{}\"}})'
cypher = """
MATCH 
    (d:Person {name:"Bob"}),
    
MERGE (d) -[:KNOWS]-> (d1:Person {name:"shrugginG"})
"""
tx.run(cypher=cypher)
tx.commit()
