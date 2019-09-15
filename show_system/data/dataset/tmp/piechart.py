import os
import sys
import json
from random import randint, shuffle
def generate(template, num):
    category = [['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
    'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'],
     ['America', 'UK', 'China', 'Russia', 'India', 'Australia', 'Argentina', 'Others', 'Japan', 'Iran'],
     ['Apple', 'Banana', 'Grape', 'Peach', 'Orange', 'Melon', 'Lemon', 'Grapefruit', 'Strawberry', 'Blueberry']]
    title = ['Consumption', 'Production', 'Fruit Consumption']
    color = ['#bc80bd', '#ffed6f', '#b3de69', '#80b1d3', '#fccde5', '#d9d9d9', '#fdb462', '#ccebc5', '#bebada', '#8dd3c7', '#ffffb3', '#fb8072']
    for tid in range(num):
        n = randint(2, 10)
        theme = randint(0, 2)
        name = f'20190325_pie_{tid}.json'
        template['user_name'] = name
        template['data']['title'] = title[theme]
        template['data']['data_array'] = [{'id': i, 'c0': i, 'q0': randint(10,90)}\
         for i in range(n)]
        if theme != 0:
            shuffle(category[theme])
        shuffle(color)
        #print(color, type(color))
        tmpc0 = list(category[theme][0:n])
        tmpc0.sort()
        template['data']['c0'] = tmpc0
        template['data']['color'] = color[0:n]
        template['data']['vis_type']='load_pie_chart'
        template['data']['type'] = 'cq'
        template['data']['major_name'] = 'c0'
        template['vis_type'] = 'load_pie_chart'
        template['type'] = 'cq'
        template['svg_string'] = ''
        template['sentences'] = []
        template['data']['sentences'] = []
        template['data']['pre_gen_focus'] = []
        template['pre_gen_focus'] =''
        #print(template)
        with open ('pie/'+name, 'w') as f:
            json.dump(template, f)
    return

if __name__ == '__main__':
    num = int(sys.argv[1])
    with open('190324_pie_1111111.json', 'r') as f:
        template = json.load(f)
    generate(template, num)
