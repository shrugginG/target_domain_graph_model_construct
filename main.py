# -*- coding = utf-8 -*-
# @Time : 2022/7/12 10:21
# @Author: shrgginG
# @File : main.py
# @Software: PyCharm
import datetime

from tests.test_associate import associate
from units.get_target_website_co_domains import update_family_info_to_csv
from units.neo4j.info.shrugging_cn_neo4j_info import TENCENT_HOST_NEO4J_INFO
from units.neo4j.op_neo4j import OperateNeo4j
from loguru import logger

if __name__ == '__main__':
    # 1. print date
    # 2. crawl co_domains
    # 3. update csv
    # 4. neo4j !
    logger.add('/home/shrugging/projects/pyhton/target_domain_graph_model_construct/logs/{time:YYYY-MM-DD}.log', format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", level="INFO", mode='w')
    logger.info(f'############### {str(datetime.datetime.now()).split(".")[0]} ###############')
    update_family_info_to_csv()
    print('Daily family info update succeed!')

    Operator = OperateNeo4j(TENCENT_HOST_NEO4J_INFO)
    Operator.delete_all()
    logger.info(f'Clean the history family graph model succeed!')
    # Add the constraint for unique fqdn.
    # constraint_cypher = 'CREATE CONSTRAINT fqdnConstraint FOR (domain:Domain) REQUIRE domain.fqdn IS UNIQUE'
    # Test.execute_cypher(constraint_cypher)

    domain_cypher = """
    LOAD CSV WITH HEADERS FROM "file:////home/shrugging/projects/pyhton/target_domain_graph_model_construct/datas/today_family_graph/domain.csv" AS csvLine
    MERGE (d:Domain {fqdn: csvLine.fqdn, created_time: csvLine.created_time})
    """

    # 8月1日发现逻辑错误，回滚家族图谱至2022-07-12
    load_cypher = """
    LOAD CSV WITH HEADERS FROM "file:////home/shrugging/projects/pyhton/target_domain_graph_model_construct/datas/today_family_graph/cross_load.csv" AS csvLine_1
    LOAD CSV WITH HEADERS FROM "file:////home/shrugging/projects/pyhton/target_domain_graph_model_construct/datas/today_family_graph/dns_prefetch.csv" AS csvLine_2
    MATCH (anchor_domain_1:Domain {fqdn: csvLine_1.anchor_fqdn}), (target_fqdn_1:Domain {fqdn: csvLine_1.target_fqdn})
    MATCH (anchor_domain_2:Domain {fqdn: csvLine_2.anchor_fqdn}), (target_fqdn_2:Domain {fqdn: csvLine_2.target_fqdn})
    MERGE (anchor_domain_1)-[:CROSS_LOAD {created_time: csvLine_1.created_time}]->(target_fqdn_1)
    MERGE (anchor_domain_2)-[:DNS_PREFETCH {created_time: csvLine_2.created_time}]->(target_fqdn_2)
    """
    Operator.execute_cypher(domain_cypher)
    Operator.execute_cypher(load_cypher)
    logger.info(f'Refactor the family graph model succeed!')
