import os
import re
import esprima
import itertools
from util import visitor


def check_call_expression(node):
    if node.callee.type == 'MemberExpression':
        if hasattr(node.callee.object, 'name') and node.callee.object.name == '$':
            if node.callee.property.name == 'get':
                return 'get'
            if node.callee.property.name == 'post':
                return 'post'
            if node.callee.property.name == 'ajax':
                return 'ajax'
    return 'not target callee'


def find_url(node):
    pass


def new_js_parser(program):
    ast = esprima.parseScript(program).toDict()
    program = visitor.objectify(ast)
    call_expression_node_list = program.search_by_type('CallExpression')
    for call_expression_node in call_expression_node_list:
        callee_name = check_call_expression(call_expression_node)
        if callee_name == 'get':
            # print(callee_name)
            url_node = call_expression_node.arguments[0]
        if callee_name == 'post':
            if call_expression_node.arguments[0].type == 'Literal':
                url = call_expression_node.arguments[0].value
                print(url, end='   ')
            print(call_expression_node.arguments[0].type)
        if callee_name == 'ajax':
            print(callee_name)


def match_url(check_string):
    if isinstance(check_string, str):
        url_match_restr_1 = r'/([\w.\/?%&=]*)?'
        url_match_restr_2 = r'([\w.\?%&=]*)/([\w.\/?%&=]*)?'
        if re.match(url_match_restr_1, check_string) is not None:
            return True
        if re.match(url_match_restr_2, check_string) is not None:
            return True
    return False


def JSParser(program):
    ast = esprima.parseScript(program).toDict()
    program = visitor.objectify(ast)
    literal_node_list = program.search_by_type('Literal')
    url_list = []
    for literal_node in literal_node_list:
        if match_url(literal_node.value):
            url_list.append(literal_node.value)

    object_node_lsit = program.search_by_type('ObjectExpression')
    kerword_list = []
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
    with open("./test/tenda ax3/js/net_control.js",'r') as f:
        a = esprima.parseScript(f.read())
        print(a)
    # for i in file_list:
    #     if os.path.isfile(os.path.join(os.getcwd(), './test/tenda ax3/js', i)):
    #         with open('./test/tenda ax3/js/' + i, 'r') as f:
    #             # res = JSParser(f.read())
    #             print(i)
    #             new_js_parser(f.read())
    #             print()
    #             # for i in res:
    #             #     print(i)
