# -*- coding = utf-8 -*-
# @Time : 2022/7/12 12:32
# @Author: shrgginG
# @File : op_neo4j.py
# @Software: PyCharm


from py2neo import Graph


class OperateNeo4j(object):
    def __init__(self, info_dict):
        self.handler = self.__get_neo4j_handler(info_dict)

    def __get_neo4j_handler(self, info_dict):
        graph = Graph(info_dict['bolt_url'],
                      auth=(info_dict['user'],
                            info_dict['password']))
        return graph

    def delete_all(self):
        self.handler.delete_all()

    def execute_cypher(self, cypher):
        tx = self.handler.begin()
        tx.run(cypher=cypher)
        tx.commit()

    def get_cypher_result_data(self, cypher):
        result = self.handler.run(cypher).data()
        return result
