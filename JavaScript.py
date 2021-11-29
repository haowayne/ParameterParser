import os
import re
import esprima
import itertools
from util import visitor


# def match_url(check_string):
#     if isinstance(check_string, str):
#         url_match_restr_1 = r'/([\w.\/?%&=]*)?'
#         url_match_restr_2 = r'([\w.\?%&=]*)/([\w.\/?%&=]*)?'
#         if re.match(url_match_restr_1, check_string) is not None:
#             return True
#         if re.match(url_match_restr_2, check_string) is not None:
#             return True
#     return False
#
#
# def JSParser(program):
#     ast = esprima.parseScript(program).toDict()
#     program = visitor.objectify(ast)
#     literal_node_list = program.search_by_type('Literal')
#     url_list = []
#     for literal_node in literal_node_list:
#         if match_url(literal_node.value):
#             url_list.append(literal_node.value)
#
#     object_node_lsit = program.search_by_type('ObjectExpression')
#     kerword_list = []
#     for object in object_node_lsit:
#         target_flag = 1
#         for property in object.properties:
#             if property.value.type != 'Identifier' and property.value.type != 'Literal' and property.value.type != 'CallExpression':
#                 target_flag = 0
#         if target_flag:
#             keyword = []
#             for property in object.properties:
#                 if property.key.type == 'Identifier':
#                     keyword.append(property.key.name)
#                 elif property.key.type == 'Literal':
#                     keyword.append(property.key.value)
#             if len(keyword) != 0:
#                 kerword_list.append(keyword)
#     combine = itertools.product(url_list, ['GET', 'POST'], kerword_list)
#     request_list = []
#     for i in combine:
#         req = {
#             'url': i[0],
#             'method': i[1],
#             'parameter': {}
#         }
#         for key in i[2]:
#             req['parameter'][key] = ''
#         request_list.append(req)
#     return request_list


def check_call_expression(node):
    if node.callee.type == 'MemberExpression':
        if hasattr(node.callee.object, 'name') and node.callee.object.name == '$':
            if node.callee.property.name == 'get':
                return 'get'
            if node.callee.property.name == 'post':
                return 'post'
            if node.callee.property.name == 'ajax':
                return 'ajax'
        elif hasattr(node.callee.object, 'object') and hasattr(node.callee.object.object,
                                                               'name') and node.callee.object.object.name == '$':
            if node.callee.object.property.name == 'GetSetData':
                if node.callee.property.name == 'getData':
                    return 'getData'
                if node.callee.property.name == 'setData':
                    return 'setData'
    return 'not target callee'


def object_expression_analysis(check_expression_node):
    keyword = []
    for property in check_expression_node.properties:
        if property.key.type == 'Identifier':
            keyword.append(property.key.name)
        elif property.key.type == 'Literal':
            keyword.append(property.key.value)
    return keyword


def url_analysis(url_node):
    tmp = url_node.search_by_type('Literal')
    res = []
    for literal_node in tmp:
        if isinstance(literal_node.value, str):
            url = literal_node.value
            if url[len(url) - 1] == '?':
                url = url[:len(url) - 1]
            res.append(url)
    if len(res) == 1:
        return res[0]
    return res


def binary_expression_analysis(binary_expression_node):
    literal_node_list = binary_expression_node.search_by_type('Literal')
    res = []
    for literal_node in literal_node_list:
        if isinstance(literal_node.value, str):
            temp = literal_node.value.split('&')
            regex = r'\w*(?=\=)'
            for i in temp:
                match = re.match(regex, i)
                if match:
                    res.append(match.group())
    return res


def recur_find_data(node, var_name, **kwargs):
    def callback_search_identifer(checked_node):
        if checked_node.type == 'Identifier' and checked_node.name == var_name:
            return True
        return False

    param_list = []

    if 'checked_list' in kwargs.keys():
        checked_list = kwargs['checked_list']
    else:
        checked_list = []
    if node.type != 'FunctionDeclaration':
        checked_list.append(node)

    function_parent_node = visitor.find_function_parent(node)
    if function_parent_node is not None:
        identifier_list = function_parent_node.search(callback_search_identifer)
        for identifier in identifier_list:
            if identifier not in checked_list:
                if identifier.parent.type == 'VariableDeclarator':
                    if hasattr(identifier.parent, 'init') and identifier.parent.init is not None:
                        param_list += (binary_expression_analysis(identifier.parent.init))
                if identifier.parent.type == 'AssignmentExpression':
                    if identifier.parent.operator == '=':
                        if identifier.parent.right.type == 'BinaryExpression':
                            param_list += binary_expression_analysis(identifier.parent.right)
                        if identifier.parent.right.type == 'ObjectExpression':
                            param_list += object_expression_analysis(identifier.parent.right)
                        if identifier.parent.right.type == 'Literal' and isinstance(identifier.parent.right.value, str):
                            tmp = identifier.parent.right.value.split('$')
                            regex = r'\w*(?=\=)'
                            for i in tmp:
                                match = re.match(regex, i)
                                if match:
                                    param_list.append(match.group())
        if param_list is not []:
            return param_list
        return recur_find_data(function_parent_node, var_name, checked_list=checked_list)
    return []


def new_js_parser(program):
    ast = esprima.parseScript(program).toDict()
    program = visitor.objectify(ast)
    call_expression_node_list = program.search_by_type('CallExpression')
    res = []
    for call_expression_node in call_expression_node_list:
        callee_name = check_call_expression(call_expression_node)
        url = ''
        keyword_list = []

        # __________________________________get_and_getData_part_____________________
        if callee_name == 'get' or callee_name == 'getData':
            if call_expression_node.arguments[0].type == 'Literal':
                url = call_expression_node.arguments[0].value
            else:
                url_node = call_expression_node.arguments[0]
                if url_node.type == 'BinaryExpression':
                    url = url_analysis(url_node)
            res.append({
                'method': 'get',
                'url': url
            })

        # __________________________________post_and_setdata_part____________________
        if callee_name == 'post' or callee_name == 'setData':
            if call_expression_node.arguments[0].type == 'Literal':
                url = call_expression_node.arguments[0].value
            else:
                url_node = call_expression_node.arguments[0]
                if url_node.type == 'BinaryExpression':
                    url = url_analysis(url_node)

            param_node = call_expression_node.arguments[1]
            if call_expression_node.arguments[1].type == 'Literal':
                keyword_list += binary_expression_analysis(param_node)
            else:
                if param_node.type == 'Identifier':
                    keyword_list += recur_find_data(param_node, param_node.name)
                if param_node.type == 'BinaryExpression':
                    keyword_list += binary_expression_analysis(param_node)
            res.append({
                'method': 'post',
                'url': url,
                'parameter': keyword_list
            })

        # __________________________________ajax_part__________________________________
        if callee_name == 'ajax':
            if call_expression_node.arguments[0].type == 'ObjectExpression':
                ajax_param = call_expression_node.arguments[0]
                url = ''
                method = ''
                param_list = []
                for property in ajax_param.properties:
                    if property.key.type == 'Identifier':
                        if property.key.name == 'url':
                            if property.value.type == 'Literal':
                                url = property.value.value
                        if property.key.name == 'type':
                            if property.value.type == 'Literal':
                                method = property.value.value
                    elif property.key.type == 'Literal':
                        pass
                if method.lower() == 'post':
                    for property in ajax_param.properties:
                        if property.key.type == 'Identifier' and property.key.name == 'data':
                            if property.value.type == 'Identifier':
                                param_list += recur_find_data(property.value, property.value.name)
                            if property.value.type == 'BinaryExpression':
                                keyword_list += binary_expression_analysis(param_node)
                if url != '' and method != '':
                    if method.lower() == 'get':
                        res.append({
                            'method': 'get',
                            'url': url,
                        })
                    if method.lower() == 'post':
                        res.append({
                            'method': 'post',
                            'url': url,
                            'parameter': param_list
                        })
    return res


if __name__ == '__main__':
    # with open("./test/tenda ax3/js/main.js", 'r') as f:
    #     new_js_parser(f.read())
    #     # for i in new_js_parser(f.read()):
    #     #     print(i)

    file_list = os.listdir(('./test/tenda ax3/js'))
    for i in file_list:
        if os.path.isfile(os.path.join(os.getcwd(), './test/tenda ax3/js', i)):
            with open('./test/tenda ax3/js/' + i, 'r') as f:
                res = new_js_parser(f.read())
                if res:
                    print(i)
                    for t in res:
                        print(t)
                    print()
