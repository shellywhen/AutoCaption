from deal_svg import *
import shutil
def produce():
    filenames = os.listdir("../../show_system/data/SVG")
    #filenames = ["ocq_super_rule_ocq_web_2018_09_18_12_23_02_344075.json"]
    for fid, fn in enumerate(filenames):
        with open("../../show_system/data/SVG/" + fn) as f:
            print(fn, 'begin processing')
            filedata = json.load(f)
            svg_string = filedata['svg_string']
            origin_id = filedata['data']['data_array']
            dpList, data, soup = parse_unknown_svg(svg_string)
            elements = [getDataPointList(dp) for dp in dpList]
            if(len(elements)<7):
                for k in range(7-len(elements)):
                    elements.append([0 for i in range(60)])
            idarray = [i for i in range(len(dpList))]
            for i, ele in enumerate(data['data_array']):
                o0 = int(data['o0'][int(ele['o0'])])
                c0 = data['c0'][int(ele['c0'])]
                for oid, origin in enumerate(origin_id):
                    o_o0 = int(filedata['data']['o0'][int(origin['o0'])])
                    o_c0 = filedata['data']['c0'][int(origin['c0'])]
                    if o0 == o_o0 and c0==o_c0:
                        idarray[i] = origin['id']
                        print(i, oid)
                        break
            print('CHECK IDARRAY', idarray)
            sentences = filedata['sentences']
            A_numpy = numpy.asarray(elements)
            B_numpy = get_B_order_numpy(sentences, idarray)
            numpy.save('trainA/'+fn[0:-5], A_numpy)
            numpy.save('trainB/'+fn[0:-5], B_numpy)
            # print('NUMPY:', i, A_numpy.shape, B_numpy)
            # break
def moveDir():
    filenames = os.listdir("trainA")
    testfile = filenames[0:3000:10]
    #shutil.move('test/hello.txt', 'hello.txt')
    for file in testfile:
        shutil.move('trainA/'+file, 'testA/'+file)
        shutil.move('trainB/'+file, 'testB/'+file)
    return

if __name__=="__main__":
    # data = numpy.load("ocq_super_rule_ocq_web_2018_09_18_12_22_52_0007477.npy")
    # print(data.shape)
    # produce()
    moveDir()
