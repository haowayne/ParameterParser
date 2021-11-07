import re
import esprima
from util import visitor


def match_url(check_string):
    if isinstance(check_string, str):
        url_match_restr = r'/([\w.\/?%&=]*)?$'
        if re.match(url_match_restr, check_string) is not None:
            print(check_string)
            return True
    return False


def JSParser(program):
    ast = esprima.parseScript(program).toDict()
    program = visitor.objectify(ast)
    a = program.search_by_type('Literal')
    url_node_list = []
    for node in a:
        if match_url(node.value):
            url_node_list.append(node)
    print(url_node_list)

    # # parser = json.loads(parser)


if __name__ == '__main__':
    with open('./test/tenda ax3/js/login.js', 'r') as f:
        JSParser(f.read())
