# -*- coding = utf-8 -*-
# @Time : 2022/7/12 12:42
# @Author: shrgginG
# @File : tmp_neo4j.py
# @Software: PyCharm
import logging

from neo4j import GraphDatabase

from units.get_target_website_co_domains import extract_domain, parse_the_rendered_content
from units.neo4j.info.shrugging_cn_neo4j_info import TENCENT_HOST_NEO4J_INFO


class Neo4j(object):

    def __init__(self, bolt_url, user, password):
        self.driver = GraphDatabase.driver(bolt_url, auth=(user, password))

    def close(self):
        self.driver.close()

    @staticmethod
    def enable_log(level, output_stream):
        handler = logging.StreamHandler(output_stream)
        handler.setLevel(level)
        logging.getLogger("neo4j").addHandler(handler)
        logging.getLogger("neo4j").setLevel(level)

    def execute_cypher_query(self, cypher_query):
        with self.driver.session() as session:
            return session.write_transaction(self._execute_cypher_query, cypher_query)

    @staticmethod
    def _execute_cypher_query(tx, cypher_query):
        return tx.run(cypher_query)


def create_family(url, graph):
    domain = extract_domain(url)
    print(domain)
    cypher_query = f"CREATE (:Domain:Anchor {{fqdn:\"{domain}\"}} )"
    print(cypher_query)
    graph.run(cypher_query)
    sets = parse_the_rendered_content('https://www.spp.gov.cn/')
    print(sets)
    for i in zip(range(2), ['cross_domain', 'dns_prefetch']):
        query_list = [
            "MERGE (d) -[:{} ]-> (:Domain {{ fqdn: \"{}\"}})"
            .format(i[1],
                    domain)
            for domain in sets[i[0]]
        ]
        print(query_list)
        query_list.insert(0, "MATCH (d:Domain:Anchor{{fqdn:\"{}\"}})".format(domain))
        query = " ".join(query_list)
        graph.run(query)


if __name__ == '__main__':
    from py2neo import Graph

    cypher_query = 'match(n) return n;'
    # 连接数据库
    # graph = Graph(
    #     "bolt://121.4.128.151:7687",
    #     username="neo4j",
    #     password="123456"
    # )
    graph = Graph("http://121.4.128.151:7474/", auth=("neo4j", "123456"))
    graph.run('match (n) detach delete n')
    # 查询，并使用.data()序列化数据
    urls = ['http://www.npc.gov.cn/',
            'http://www.cppcc.gov.cn/',
            'https://www.ccdi.gov.cn/',
            'https://www.spp.gov.cn/',
            'http://www.nhsa.gov.cn/',
            'https://www.samr.gov.cn/']
    for url in urls:
        print(url)
        print(create_family(url, graph))
