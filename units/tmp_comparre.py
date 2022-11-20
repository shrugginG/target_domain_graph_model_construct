# -*- coding = utf-8 -*-
# @Time : 2022/7/12 14:01
# @Author: shrgginG
# @File : tmp_comparre.py
# @Software: PyCharm
import json

with open('../datas/20220614_0900.json', 'r') as f:
    raw_datas = [json.loads(line) for line in f.readlines()]

with open('../datas/result.json', 'r') as f:
    source_data = json.loads(f.read())
print(source_data)

for item in raw_datas:
    target_domain = item['sign'].split('_')[1]
    record_list = [i.split('_')[-1] for i in item['record_list']]
    total = len(record_list)
    sum = 0
    for domain in record_list:
        if domain in source_data[target_domain]:
            sum += 1
    item['rate'] = sum / total

raw_datas.sort(key=lambda x: x['rate'], reverse=True)

with open('../datas/result_rate.json', 'w') as f:
    for i in raw_datas:
        f.write(json.dumps(i) + '\n')
