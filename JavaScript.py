import os
import re
import esprima
import itertools
from util import visitor


def match_url(check_string):
    if isinstance(check_string, str):
        url_match_restr_1 = r'/([\w.\/?%&=]*)?'
        url_match_restr_2 = r'([\w.\?%&=]*)/([\w.\/?%&=]*)?'
        if re.match(url_match_restr_1, check_string) is not None:
            return True
        if re.match(url_match_restr_2, check_string) is not None:
            return True
    return False


def new_js_parser():
    # todo:迭代精准搜索url和keyword
    pass


def JSParser(program):
    ast = esprima.parseScript(program).toDict()
    program = visitor.objectify(ast)
    literal_node_list = program.search_by_type('Literal')
    object_node_lsit = program.search_by_type('ObjectExpression')
    url_list = []
    kerword_list = []
    for literal_node in literal_node_list:
        if match_url(literal_node.value):
            url_list.append(literal_node.value)
    for object in object_node_lsit:
        target_flag = 1
        for property in object.properties:
            if property.value.type != 'Identifier' and property.value.type != 'Literal' and property.value.type != 'CallExpression':
                target_flag = 0
        if target_flag:
            keyword = []
            for property in object.properties:
                if property.key.type == 'Identifier':
                    keyword.append(property.key.name)
                elif property.key.type == 'Literal':
                    keyword.append(property.key.value)
            if len(keyword) != 0:
                kerword_list.append(keyword)
    combine = itertools.product(url_list, ['GET', 'POST'], kerword_list)
    request_list = []
    for i in combine:
        req = {
            'url': i[0],
            'method': i[1],
            'parameter': {}
        }
        for key in i[2]:
            req['parameter'][key] = ''
        request_list.append(req)
    return request_list


if __name__ == '__main__':
    res = []
    file_list = os.listdir(('./test/tenda ax3/js'))
    for i in file_list:
        if os.path.isfile(os.path.join(os.getcwd(), './test/tenda ax3/js', i)):
            with open('./test/tenda ax3/js/' + i, 'r') as f:
                print(i)
                res = JSParser(f.read())
                for i in res:
                    print(i)
                print()
