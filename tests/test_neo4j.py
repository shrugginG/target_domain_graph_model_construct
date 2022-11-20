# -*- coding = utf-8 -*-
# @Time : 2022/7/16 17:40
# @Author: shrgginG
# @File : test_neo4j.py
# @Software: PyCharm
from units.neo4j.info.shrugging_cn_neo4j_info import TENCENT_HOST_NEO4J_INFO
from units.neo4j.op_neo4j import OperateNeo4j

if __name__ == '__main__':
    Test = OperateNeo4j(TENCENT_HOST_NEO4J_INFO)
    str = 'match (:Domain {fqdn:"www.nhsa.gov.cn"}) -[*1]-> (n) return n'
    co_domains = [node['n']['fqdn'] for node in Test.get_cypher_result_data(str)]
    print(len(set(co_domains)))