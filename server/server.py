# -*- coding: utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
from save_data import save
from tornado.escape import url_unescape
from generate_data.data_generator import get_data

from uuid import uuid4
import json, ast
import time
import urllib
# import urllib2
import re
import time
import random
import os
import requests
from multiprocessing.dummy import Pool as ThreadPool
from tornado.log import enable_pretty_logging
# enable_pretty_logging()
import logging
from sentence_generator.sentence_generator import generate_sentence_by
from qq_generator import generate_toy_qq_sentence
import sys

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('../machinelearning'))
sys.path.append(os.path.abspath('./sentence_generator'))

if __name__ != '__main__':
    from test_numpy import get_data_json, parse_to_id_array, get_data_svg
    from extract_svg import get_modified_svg_data


logger = logging.getLogger(__name__)

machine_model = '';


from tornado.options import define, options
define("port", default=8000, help = "run on the given port", type = int)
define("show", default=False, help = "run on the given port", type = bool)

# the path to server html, js, css files
client_file_root_path = os.path.join(os.path.split(__file__)[0],'../data_collect_system')
client_file_root_path = os.path.abspath(client_file_root_path)

show_file_root_path = os.path.join(os.path.split(__file__)[0], '../show_system')
show_file_root_path = os.path.abspath(show_file_root_path)

def get_page(url):
    user_agent_str = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"
    time.sleep(random.uniform(0,1))
    return requests.get(url, headers={"Connection":"keep-alive", "User-Agent": user_agent_str}).text

class getSentenceHandler(tornado.web.RequestHandler):
    def post(self):
        data = self.get_body_argument('data')
        compare_id = self.get_body_argument('compare_id')
        focus_id = self.get_body_argument('focus_id')
        major_name = self.get_body_argument('major_name')
        second_name = self.get_body_argument('second_name')
        logger.info(data)
        data = json.loads(data)
        compare_id = json.loads(compare_id)
        focus_id = json.loads(focus_id)
        sentences = generate_sentence_by(data, focus_id, compare_id, major_name, second_name)
        # if len(sentences) > 0:
        #     sentences[0]['sentence'] = "小猫小狗"

        logger.info(sentences)
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps(sentences))
        self.finish()

class submitAnswerHandler(tornado.web.RequestHandler):
    def post(self):
        data_string = self.get_body_argument('data_string')
        sentences_string = self.get_body_argument('sentences_string')
        svg_string = self.get_body_argument('svg_string')
        major_dim = self.get_body_argument('major_name')
        second_dim = self.get_body_argument('second_name')
        user_name = self.get_body_argument('user_name')
        total_number = self.get_body_argument('total_number')
        # logger.info(sentences_string)
        data = {}
        data['user_name'] = user_name
        data['total_number'] = total_number
        data['data'] = json.loads(data_string)
        data['svg_string'] = svg_string
        data['sentences'] = json.loads(sentences_string)
        data['major_dim'] = major_dim
        data['second_dim'] = second_dim
        save(data)

        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps({'message': 'ok'}))
        self.finish()

class getDataHandler(tornado.web.RequestHandler):
    def post(self):
        # with open("../data_collect_system/json/Ielts_new_principle/ielts_data/0016.json") as f:
        #     data = json.load(f)
        data_type = self.get_body_argument('data_type')
        data = get_data(data_type)
        if 'pre_gen_focus' in data.keys():
            sentences = []
            for sentence in data['pre_gen_focus']:
                focus_id = sentence['focus_id']
                compare_id = sentence['compare_id']
                major_name = data['major_name']
                second_name = data['second_name']
                answers = generate_sentence_by(data, focus_id, compare_id, major_name, second_name)
                for answer in answers:
                    if answer['type'] == sentence['type']:
                        sentences.append(answer)
                        break;
            data['sentences'] = sentences

        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps(data))
        self.finish()


class queryAddressHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Content-type', 'application/json')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self):
        # data = json.loads()
        # logger.info(self.request.body)
        logger.info(url_unescape(self.request.body))
        logger.info(self.request)#(self.request.body)
        print(self.request)
        # print('liucan')

        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps({'message': 'ok'}))
        self.finish()

    def post(self):
        # logger.info(self.request.body)
        # param = self.request.body.decode('utf-8')
        # param = json.loads(param)
        # logger.info(param)
        # data = tornado.escape.json_decode(self.request.body)
        logger.info(url_unescape(self.request.body))
        svg_string = self.get_body_argument('content')
        logger.info(svg_string)
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps({'message': 'ok'}))
        self.finish()
        # self.finish()


class getModifySvgSentence(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Content-type', 'application/json')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    def get(self):
        print("get method")

    def post(self):
        # with open("../data_collect_system/json/Ielts_new_principle/ielts_data/0016.json") as f:
        #     data = json.load(f)
        begin_time = time.time()
        svg_string = self.get_body_argument('svg_string')
        print('svg_string, weird', svg_string)
        svg_string, data_json = get_modified_svg_data(svg_string)
        print("data_json", data_json)
        print('modified svg_string', svg_string)
        input, id_array = get_data_svg(svg_string)
        machine_model.set_input(input)
        output = machine_model.test()
        focal_array = parse_to_id_array(output, id_array)
        # 获取到关注数组
        if 'vis_type' in data_json and data_json['vis_type'] == 'load_scatter_plot':
            sentences = generate_toy_qq_sentence(focal_array, data_json)
        else:
            major_name = data_json['major']
            second_name = data_json['second']
            sentences = []
            sentence_type = ['compare_trend', 'compare_ave', 'sum_trend', 'all_trend', 'local_trend', 'local_sum_trend']
            for i, setting in enumerate(focal_array):
                print(setting)
                this_sentences = generate_sentence_by(data_json, setting['focus_id'], setting["compare_id"], major_name, second_name)
                for sentence in this_sentences:
                    if sentence['type'] == sentence_type[i]:
                        sentence['strength'] = setting['strength']
                        sentences.append(sentence)
                        break

        sentences = sorted(sentences,key = lambda x:-x['strength'])
        # print(sentences)

        send_data = {}
        send_data['sentences'] = sentences
        send_data['svg_string'] = svg_string
        send_data['data'] = data_json
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps(send_data))
        self.finish()
        end_time = time.time()
        inter_time = end_time - begin_time
        print(f"Total spend {inter_time} seconds")


class getMachineAnswer(tornado.web.RequestHandler):
    def get(self):
        # with open("../data_collect_system/json/Ielts_new_principle/ielts_data/0016.json") as f:
        #     data = json.load(f)
        data, id_array = get_data_json('../server/user_collected_data/2018_08_20_14_38_19_6309872.json')
        machine_model.set_input(data)
        output = machine_model.test()
        focal_array = parse_to_id_array(output, id_array)

        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps(focal_array))
        self.finish()
    def post(self):
        # with open("../data_collect_system/json/Ielts_new_principle/ielts_data/0016.json") as f:
        #     data = json.load(f)
        data_string = self.get_body_argument('data_string')
        svg_string = self.get_body_argument('svg_string')
        major_name = self.get_body_argument('major_name')
        second_name = self.get_body_argument('second_name')

        data_json = json.loads(data_string)

        input, id_array = get_data_svg(svg_string)
        machine_model.set_input(input)
        output = machine_model.test()
        focal_array = parse_to_id_array(output, id_array)
        sentences = []
        sentence_type = ['compare_trend', 'compare_ave', 'sum_trend', 'all_trend', 'local_trend', 'local_sum_trend']
        for i, setting in enumerate(focal_array):
            # print(setting)
            this_sentences = generate_sentence_by(data_json, setting['focus_id'], setting["compare_id"], major_name, second_name)
            # if sentence_type == 'local_trend':
            #     for sentence in this_sentence:
            #         print(sentence)
            for sentence in this_sentences:
                if sentence['type'] == sentence_type[i]:
                    sentences.append(sentence)
                    break
        sentences = sorted(sentences,key = lambda x:x['strength'])
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps(sentences))
        self.finish()

class getFileName(tornado.web.RequestHandler):
    def get(self):
        filenames = os.listdir("../show_system/data/dataset/tmp/")
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps(filenames))
        self.finish()

    def post(self):
        data_string = self.get_body_argument('svg')
        data_path = self.get_body_argument('path')
        save_path = self.get_body_argument('save')
        with open(data_path) as f:
            data = json.load(f)
            data['svg_string'] = data_string
        with open(save_path, 'w') as fw:
            json.dump(data, fw, indent=2)
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps({'msg': 'OK'}))
        self.finish()



class Application(tornado.web.Application):
    def __init__ (self):
        handlers = [
            (r'/vis2description/get_file_name', getFileName),
            (r'/get_svg_data', getModifySvgSentence),
            (r'/vis2description/get_svg_data', getModifySvgSentence),
            (r'/vis2description/getsentence', getSentenceHandler),
            (r'/vis2description/heiheihei', queryAddressHandler),
            (r'/vis2description/submit_answer', submitAnswerHandler),
            (r'/vis2description/get_data_json', getDataHandler),
            (r'/vis2description/get_machine_answer', getMachineAnswer),
            (r'/vis2description/(.*)', tornado.web.StaticFileHandler, {'path': client_file_root_path, 'default_filename': 'index.html'}), # fetch client file
            (r'/getsentence', getSentenceHandler),
            (r'/heiheihei', queryAddressHandler),
            (r'/submit_answer', submitAnswerHandler),
            (r'/get_data_json', getDataHandler),
            (r'/get_machine_answer', getMachineAnswer),
            (r'/(.*)', tornado.web.StaticFileHandler, {'path': client_file_root_path, 'default_filename': 'index.html'}), # fetch client file
            (r'/show/(.*)', tornado.web.StaticFileHandler, {'path': show_file_root_path, 'default_filename': 'index.html'}), # fetch client file
            ]

        settings = {
            'static_path': 'static',
            'debug': True
            }
        tornado.web.Application.__init__(self, handlers, **settings)

def run_server(port, model, is_show = False):
    global machine_model
    global client_file_root_path
    machine_model = model
    if is_show:
        client_file_root_path = show_file_root_path
    print(f'Root path: {client_file_root_path}')
    app = Application()
    print('server running at 127.0.0.1:%d ...'%(port))
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
  tornado.options.parse_command_line()
  print('server running at 127.0.0.1:%d ...'%(tornado.options.options.port))
  show = False
  if (show):
      client_file_root_path = show_file_root_path

  app = Application()
  http_server = tornado.httpserver.HTTPServer(app)
  http_server.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()
