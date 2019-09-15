from deal_svg import *
import shutil
def produce():
    filenames = os.listdir("../datasets/scatter3089/")
    for fid, fn in enumerate(filenames):
        with open("../datasets/scatter3089/" + fn) as f:
            print(fn, 'begin processing')
            filedata = json.load(f)
            svg_string = filedata['data']['svg_string']
            origin_id = filedata['data']['data_array']
            dpList, data, soup = parse_unknown_svg(svg_string)
            elements = [getCircleList(dp) for dp in dpList]
            if(len(elements)<7):
                for k in range(7-len(elements)):
                    elements.append([0 for i in range(60)])
            idarray = [i for i in range(len(dpList))]
            for i, ele in enumerate(data['data_array']):
                e0 = ele['q0']
                e1 = ele['q1']
                dis = 5000
                for oid, origin in enumerate(origin_id):
                    o0 = origin['q0']
                    o1 = origin['q1']
                    d = abs(e0-o0)+abs(e1-o1)
                    if d < dis:
                        idarray[i] = origin['id']
                        dis = d
            sentences = filedata['data']['sentences']
            # A_numpy = numpy.asarray(elements)
            B_numpy = get_scatter_B_order_numpy(sentences, idarray)
            #B_numpy = get_B_order_numpy(sentences, idarray)
            #print(B_numpy)
            # numpy.save('trainA/'+fn[0:-5], A_numpy)
            numpy.save('trainB/'+fn[0:-5], B_numpy)
def moveDir():
    filenames = os.listdir("trainA")
    testfile = filenames[0:3000:10]
    for file in testfile:
        shutil.move('trainA/'+file[0:-5], 'testA/'+file)
        shutil.move('trainB/'+file[0:-5], 'testB/'+file)
    return

if __name__=="__main__":
    # data = numpy.load("ocq_super_rule_ocq_web_2018_09_18_12_22_52_0007477.npy")
    # print(data.shape)
    produce()
    moveDir()
