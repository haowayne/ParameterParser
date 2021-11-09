import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.40'
}
proxies = {
    'http':'http://127.0.0.1:8080',
    'https': 'https://127.0.0.1:8080'
}

def auto_send_packet(ip: str, res: list, known_urls: list, cookie: str):
    headers['Cookie'] = cookie

    for http in res:
        #todo data variation
        data = http['parameter']
        for url in known_urls:
            http['url'] = '/' + http['url']
            url = ip + http['url']
            if http['method'] == '':
                r = requests.post(url, data=http['parameter'], headers=headers, proxies=proxies)
                r = requests.get(url, params=http['parameter'], headers=headers, proxies=proxies)
            elif http['method'].upper() == 'POST':
                r = requests.post(url, data=http['parameter'], headers=headers,proxies=proxies)
            elif http['method'].upper() == 'GET':
                r = requests.get(url, params=http['parameter'], headers=headers,proxies=proxies)


if __name__ == '__main__':
    auto_send_packet('http://www.baidu.com',
                     {'url': '/cgi-bin/UploadCfg', 'method': 'POST', 'parameter': {'filename': ''}},
                     ''
                     )
