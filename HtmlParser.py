# coding=utf-8
import os

# import esprima
from bs4 import BeautifulSoup
import os
from util import packet

all_files = []
known_urls = []


def list_all_files(path):
    lsdir = os.listdir(path)
    dirs = [i for i in lsdir if os.path.isdir(os.path.join(
        path, i))]
    if dirs:
        for i in dirs:
            list_all_files(os.path.join(path, i))
    files = [i for i in lsdir if os.path.isfile(os.path.join(path, i))]
    for f in files:
        all_files.append(os.path.join(path, f))


# todo: javascript in html
def HtmlParser(body):
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
    return res_list


if __name__ == '__main__':
    path = '../ac9_webroot_ro'
    ip = "http://192.168.0.1"
    cookie = ''
    list_all_files(path)
    res = []
    file_list = os.listdir(path)
    for i in file_list:
        if '.htm' in i:
            with open('../ac9_webroot_ro/' + i, 'r') as f:
                print(i)
                res += HtmlParser(f.read().encode())
    res = sorted(res, key=lambda i: i.__getitem__('url'), reverse=True)
    packet.auto_send_packet(ip, res, known_urls, cookie)
