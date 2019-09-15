import json
import uuid
import os
import time

def save(data, data_dir = '../server/user_collected_data/'):
    current_time = time.time()
    format = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    # print(current_time)
    current_time_float = str(current_time).split('.')[1]

    file_name = data['data']['type'] + '_' + data['user_name'] + '_' + format + '_' + current_time_float + '.json'
    # print(file_name)
    file_name = os.path.join(data_dir, file_name)

    # print(data)

    with open(file_name, 'w') as f:
        json.dump(data, f, indent = 2)

if __name__ == '__main__':
    data = {"message": 'ok'}
    # data_dir = '../user_collected_data/'
    save(data)
