import os
import json
def rename_line_chart():
    filenames = os.listdir('SVG')
    files = ['SVG/'+ name for name in filenames]
    for idf, file in enumerate(files):
        with open(file, 'r') as f:
            sheet = json.load(f)
            chop = len("ocq_super_rule_ocq_web_2018_09_18_12_29_27_57_")+1
            sheet['user_name'] = '190320_line_'+file[chop:]
            sheet['vis_type'] = 'load_scatter_line_plot'
            sheet['type'] = 'cqq'
            sheet['data']['vis_type'] = 'load_scatter_line_plot'
            sheet['data']['x'] = 'o0'
            sheet['data']['y'] = 'q0'
            sheet['data']['type'] = 'cqq'
            sheet['data']['unit1'] = 'year'
            sheet['data']['unit2'] = sheet['data']['unit']
            sheet['data']['major_name'] = 'o0'
            sheet['data']['second_name'] = 'c0'
            sheet['data']['quan'] = 'q0'
            o0 = [int(o) for o in sheet['data']['o0']]
            with open('Line/'+sheet['user_name'], 'w') as fw:
                json.dump(sheet, fw)


if __name__ == "__main__":
    rename_line_chart()
