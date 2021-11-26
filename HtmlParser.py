# coding=utf-8
import os

# import esprima
from bs4 import BeautifulSoup
import os
from util import packet
from util import tools

MAX_THRESHOLD = 5

known_urls = []
all_js_script_list = []

# todo: javascript in html
def HtmlParser(body):
    global known_urls
    body_soup = BeautifulSoup(body, 'lxml')
    tag_form_list = body_soup.find_all('form')
    res_list = []
    for tag_form in tag_form_list:
        try:
            form_action = tag_form['action'].lstrip('//')
            known_urls.append(form_action)
        except KeyError:
            form_action = ''
        try:
            form_method = tag_form['method'].upper()
        except KeyError:
            form_method = ''
        r = {
            'url': form_action,
            'method': form_method,
            'parameter': {}
        }
        tag_input_list = tag_form.find_all('input')
        for tag_input in tag_input_list:
            try:
                attr_name = tag_input['name']
            except KeyError:
                attr_name = ''
            if attr_name != '':
                try:
                    attr_val = tag_input['value']
                except KeyError:
                    attr_val = ''
                r['parameter'][attr_name] = attr_val
        res_list.append(r)

    tag_src_list = body_soup.find_all('script',{"src" : True})
    js_script_list = []
    for js in tag_src_list:
        js_script_list.append(js['src'].strip('./'))
    all_js_script_list.append(js_script_list)

    return res_list

def classify_all_js_script_list():
    global all_js_script_list
    all_js_script_dict = {}
    for item in all_js_script_list:
        for js in item:
            if all_js_script_dict.get(js) == None:
                all_js_script_dict[js] = 1
            else:
                all_js_script_dict[js] += 1

    for i in range(len(all_js_script_list)):
        temp = dict(self_js=[],public_js=[])
        for js in all_js_script_list[i]:
            if all_js_script_dict[js] >= MAX_THRESHOLD:
                temp['public_js'].append(js)
            else:
                temp['self_js'].append(js)
        all_js_script_list[i] = temp

    print(all_js_script_dict)

if __name__ == '__main__':
    path = '../webroot_ro'
    ip = "http://192.168.0.1"
    cookie = ''
    res = []

    file_list = []
    file_list = tools.list_all_files(path,file_list)
    for i in file_list:
        if '.htm' in i:
            with open('../webroot_ro/' + i, 'r') as f:
                print(i)
                res += HtmlParser(f.read().encode())

    classify_all_js_script_list()
    res = sorted(res, key=lambda i: i.__getitem__('url'), reverse=True)
    # packet.auto_send_packet(ip, res, known_urls, cookie)
