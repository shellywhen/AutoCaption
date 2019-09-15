import json

def get_data():
    all_data = []
    with open("0-177_clean.csv") as f:
        each_data = []
        for line in f:
            if line.startswith("ID"):
                if len(each_data) != 0 :
                    all_data.append(each_data)
                each_data = []
            each_data.append(line)
        all_data.append(each_data)
        print(all_data[0])
        print(len(all_data))
    return all_data

all_data = get_data()

data_json_array = []

for data in all_data:
    ID = int(data[0].split(",")[1])
    print(ID)
    title = data[1].split(",")[1]
    dimension = [int(data[2].split(",")[1]), int(data[2].split(",")[2])]

    ordinal = [0,0]
    ordinal_index = data[2].split(",")[3]
    if (ordinal_index != ""):
        ordinal_index = int(ordinal_index)
        ordinal[ordinal_index] = 1
    dimension_name = {}
    dimension_name[1] = data[4].split(",")[1 : 1 + dimension[1]]
    for i in range(len(dimension_name[1])):
        dimension_name[1][i] = dimension_name[1][i].strip()
        # dimension_name.append(dimension_this)

    unit = data[6 + dimension[0]].split(",")[1]
    print(unit)
    dimension_name[0] = []
    for i in range(5, dimension[0] + 5):
        # print(data[i])
        dimension_name[0].append(data[i].split(",")[0].strip())
    print(dimension_name)
    for i in range(2):
        dimension_iter = dimension_name[i]
        # print(dimension_iter)

        for name in dimension_iter:
            assert(name != "")
    data_str = []
    for i in range(5, dimension[0] + 5):

        data_str.append(data[i].split(",")[1 : 1 + dimension[1]])
    print(data)
    data_num = []

    for item in data_str:
        datum_num = []
        for cell in item:
            cell = cell.strip().replace(" ",".")
            datum_num.append(float(cell))
        data_num.append(datum_num)
    if ordinal[0] == 1:
        dim_0_type = "o0"
        dim_1_type = "c0"
    elif ordinal[1] == 1:
        dim_0_type = "c0"
        dim_1_type = "o0"
    else:
        dim_0_type = "c0"
        dim_1_type = "c1"
    data_array = []
    id = 0
    for i, line in enumerate(data_num):
        dim_0_name = dimension_name[0][i]
        for j, cell in enumerate(line):
            dim_1_name = dimension_name[1][j]
            data_item = {}
            data_item["id"] = id
            data_item[dim_0_type] = i
            data_item[dim_1_type] = j
            data_item["q0"] = cell
            id = id + 1
            data_array.append(data_item)
    print(data_array)
    data_json = {}
    # data_json["dimension"] = dimension
    data_json[dim_0_type] = dimension_name[0]
    data_json[dim_1_type] = dimension_name[1]
    data_json["data_array"] = data_array
    data_json["unit"] = unit
    data_json["ID"] = ID
    data_json['title'] = title
    data_json_array.append(data_json)

for i, data_json in enumerate(data_json_array):
    file_name = "ielts_data/%04d.json" % i
    print("hahah",data_json)
    with open(file_name, "wb") as f:
        json.dump(data_json, f, indent=2)



# as the ?? goes from ... to ...
    # print(dimension_name)
    # for i in range(dimension[0]):
    #     for j in range(dimension[1]):
    #         num = data[]
