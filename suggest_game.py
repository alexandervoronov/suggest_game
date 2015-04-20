#!python3

import requests
import argparse
import markdown
import os
import json

suggest_url = 'http://google.com/complete/search?client=firefox&output=json&ie=UTF-8&q={}'

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--request', dest='request', type=str, nargs='+',
                        help='Request string.')
    parser.add_argument('--partial', dest='partial', default=False, action='store_true',
                        help='Don\'t interpret last word as a whole one')
    parser.add_argument('-b', '--batch', dest='batch', default=None,
                        help='JSON file with batch request.')
    parser.add_argument('--proxy', dest='proxy', default=None,
                        help='Proxy setting')
    
    return parser.parse_args()

def retrieve_suggests(request, partial=False, proxy=None):
    request_string = ' '.join(request) + (' ' if not args.partial else '')
    query = suggest_url.format(request_string)
    response = requests.get(query, proxies=proxy)
    answers = response.json()[1]
    return answers

def convert_to_markdown(request, answers):
    markdown_string = request + '\n'
    markdown_string += '=' * len(request) + '\n'
    markdown_string += '* ' + '\n* '.join(answers) + '\n'
    markdown_string += '\n'
    return markdown_string

def json_batch_suggests(json_path, partial=False, proxy=None):
    assert os.path.isfile(json_path)
    requests = []
    md = ''
    with open(json_path, encoding='utf8') as f:
        requests = json.load(f)
    for single_request in requests:
        ans = retrieve_suggests([single_request], partial, proxy)
        req_md = convert_to_markdown(single_request, ans)
        md += req_md
    return md

if __name__ == '__main__':
    args = parse_args()
    md = ''
    proxy = None
    if args.proxy:
        proxy = {
            "http"  : "{}".format(args.proxy),
            "https" : "{}".format(args.proxy)
        }
    if args.batch:
        md = json_batch_suggests(args.batch, args.partial, proxy)
    elif args.request:
        answers = retrieve_suggests(args.request, args.partial, proxy)
        md = convert_to_markdown(' '.join(args.request), answers)

    print(md)
    # print(markdown.markdown(convert_to_markdown(' '.join(args.request), answers))) # html
