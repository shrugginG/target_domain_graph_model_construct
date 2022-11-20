# -*- coding = utf-8 -*-
# @Time : 2022/7/12 10:23
# @Author: shrgginG
# @File : get_target_website_co_domains.py
# @Software: PyCharm
import datetime
import shutil
from urllib.parse import urlparse

from loguru import logger
from selenium import webdriver
from lxml import etree


def extract_domain(url):
    try:
        parse_result = urlparse(url)
        filter_port_result = parse_result.netloc.split(':')[0]
        return filter_port_result
    except:
        return None


# use the headless browser to get the target_domain co-domains.
def get_rendered_content(url):
    # TODO
    user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 15_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
    # proxy = "socks://localhost:7890"
    fiefox_options = webdriver.FirefoxOptions()
    fiefox_options.binary_location = "/opt/firefox/firefox"
    fiefox_options.add_argument(f"--user-agent={user_agent}")
    fiefox_options.add_argument('--headless')
    fiefox_options.add_argument('--ignore-certificate-errors-spki-list')

    browser = webdriver.Firefox(
        executable_path="/home/shrugging/projects/pyhton/similar_websites_crawler/drivers/geckodriver",
        options=fiefox_options)

    try:
        browser.get(url)
        return browser.page_source
    finally:
        browser.close()


def parse_the_rendered_content(url):
    content = get_rendered_content(url)
    target_domain = extract_domain(url)
    html_tree = etree.HTML(content)
    hrefs = html_tree.xpath('//*[@href]/@href')
    srcs = html_tree.xpath('//*[@src]/@src')
    filtered_srcs = {extract_domain(src) for src in srcs if extract_domain(src)}
    filtered_srcs.discard(target_domain)
    filtered_hrefs = {extract_domain(href) for href in hrefs if extract_domain(href)}
    filtered_hrefs.discard(target_domain)
    return filtered_srcs, filtered_hrefs


def get_family_info():
    with open('/home/shrugging/projects/pyhton/target_domain_graph_model_construct/datas/anchor_family.csv', 'r') as f:
        families = [(item.split(',')[0], item.split(',')[1].strip('\n')) for item in f.readlines()[1:]]
        return families


def update_family_info_to_csv():
    created_time = str(datetime.datetime.now()).split('.')[0]
    families_info = []
    for family in get_family_info():
        url, domain = family
        co_domains = parse_the_rendered_content(url)
        family_single_info = {"domain": domain,
                              "cross_load_co_domain": co_domains[0],
                              "dns_prefetch_co_domain": co_domains[1]}
        families_info.append(family_single_info)
        logger.info(f'Get {domain} co-domains succeed!')

    target_domains = {family["domain"] for family in families_info}
    co_domains = [set().union(family['dns_prefetch_co_domain'],
                              family['cross_load_co_domain'])
                  for family in families_info]
    current_domain_set = set.union(*co_domains, target_domains)

    current_cross_load_domain_set = [(family['domain'], cross_load_domain)
                                     for family in families_info
                                     for cross_load_domain in
                                     family['cross_load_co_domain']]
    current_dns_prefetch_domain_set = [(family['domain'], cross_load_domain)
                                       for family in families_info
                                       for cross_load_domain in
                                       family['dns_prefetch_co_domain']]

    with open('/home/shrugging/projects/pyhton/target_domain_graph_model_construct/datas/today_family_graph/domain.csv',
              'r') as domain_csv, \
            open(
                '/home/shrugging/projects/pyhton/target_domain_graph_model_construct/datas/today_family_graph/cross_load.csv',
                'r') as cross_load_csv, \
            open(
                '/home/shrugging/projects/pyhton/target_domain_graph_model_construct/datas/today_family_graph/dns_prefetch.csv',
                'r') as dns_prefetch_csv:
        existed_domains = {item.split(',')[0] for item in domain_csv.readlines()[1:]}
        existed_cross_load = [(item.split(',')[0], item.split(',')[1])
                              for item in cross_load_csv.readlines()[1:]]
        existed_dns_prefetch = [(item.split(',')[0], item.split(',')[1])
                                for item in dns_prefetch_csv.readlines()[1:]]

    with open('/home/shrugging/projects/pyhton/target_domain_graph_model_construct/datas/today_family_graph/domain.csv',
              'a') as domain_csv, \
            open(
                '/home/shrugging/projects/pyhton/target_domain_graph_model_construct/datas/today_family_graph/cross_load.csv',
                'a') as cross_load_csv, \
            open(
                '/home/shrugging/projects/pyhton/target_domain_graph_model_construct/datas/today_family_graph/dns_prefetch.csv',
                'a') as dns_prefetch_csv:
        if len(existed_domains) == 0:
            domain_csv.write("fqdn,created_time\n")
            cross_load_csv.write('anchor_fqdn,target_fqdn,created_time\n')
            dns_prefetch_csv.write('anchor_fqdn,target_fqdn,created_time\n')
            domain_content = [f"{str(item)},{created_time}\n"
                              for item in current_domain_set]
            domain_csv.writelines(domain_content)

            co_domain_content = [f"{item[0]},{item[1]},{created_time}\n"
                                 for item in current_cross_load_domain_set]
            cross_load_csv.writelines(co_domain_content)

            dns_prefetch_content = [f"{item[0]},{item[1]},{created_time}\n"
                                    for item in current_dns_prefetch_domain_set]
            dns_prefetch_csv.writelines(dns_prefetch_content)
        # 添加不存在的节点或边
        else:
            history_date = (datetime.datetime.now() - datetime.timedelta(1)).strftime('%Y-%m-%d')
            history_version_path = f'/home/shrugging/projects/pyhton/target_domain_graph_model_construct/datas/history_family_graph/{history_date}'
            shutil.copytree(
                '/home/shrugging/projects/pyhton/target_domain_graph_model_construct/datas/today_family_graph/',
                f'{history_version_path}')
            logger.info(f'Preserve the history version family info succeed!')
            logger.info(f'The the history version family info path: {history_version_path}')
            for domain in current_domain_set:
                if domain not in existed_domains:
                    # print(f'{domain},{created_time}\n')
                    domain_csv.write(f'{domain},{created_time}\n')
            for cross_load_item in current_cross_load_domain_set:
                if cross_load_item not in existed_cross_load:
                    # print(f'{cross_load_item[0]},{cross_load_item[1]},{created_time}\n')
                    cross_load_csv.write(f'{cross_load_item[0]},{cross_load_item[1]},{created_time}\n')
            for dns_prefetch_item in current_dns_prefetch_domain_set:
                if dns_prefetch_item not in existed_dns_prefetch:
                    # print(f'{cross_load_item[0]},{cross_load_item[1]},{created_time}\n')
                    dns_prefetch_csv.write(f'{cross_load_item[0]},{cross_load_item[1]},{created_time}\n')


if __name__ == '__main__':
    urls = ['http://www.nhsa.gov.cn', 'http://www-nhsa-gov-cn-1305404260.cos.ap-beijing.myqcloud.com/index.html']
    result = {}
    for url in urls:
        set1, set2 = parse_the_rendered_content(url)
        result[extract_domain(url)] = {
            'src': set1,
            'href': set2
        }
    print(result)