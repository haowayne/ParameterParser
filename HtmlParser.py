import os

import esprima
from bs4 import BeautifulSoup


# todo:html中script的提取分析在javascript模块完成后完善
def HtmlParser(body):
    body_soup = BeautifulSoup(body, 'lxml')
    tag_form_list = body_soup.find_all('form')
    res_list = []
    for tag_form in tag_form_list:
        try:
            form_action = tag_form['action']
        except KeyError:
            form_action = ''
        try:
            form_method = tag_form['method'].upper()
        except KeyError:
            form_method = 'GET'
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
    res = []
    file_list = os.listdir(('./test/tenda ax3'))
    for i in file_list:
        if 'htm' in i:
            with open('./test/tenda ax3/' + i, 'r') as f:
                res += HtmlParser(f.read())
    for i in res:
        print(i)
