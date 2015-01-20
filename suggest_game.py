#!python3

import requests
import argparse
import markdown

suggest_url = 'http://google.com/complete/search?client=firefox&output=json&ie=UTF-8&q={}'

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--request', dest='request', type=str, nargs='+',
                        help='Request string.')
    parser.add_argument('--partial', dest='partial', default=False, action='store_true',
                        help='Don\'t interpret last word as a whole one')
    return parser.parse_args()

def retrieve_suggests(request, partial=False):
    request_string = ' '.join(request) + (' ' if not args.partial else '')
    query = suggest_url.format(request_string)
    response = requests.get(query)
    answers = response.json()[1]
    return answers

def convert_to_markdown(request, answers):
    markdown_string = request + '\n'
    markdown_string += '=' * len(request) + '\n'
    markdown_string += '* ' + '\n* '.join(answers) + '\n'
    return markdown_string



if __name__ == '__main__':
    args = parse_args()
    answers = retrieve_suggests(args.request, args.partial)

    # print('\n'.join(answers))
    print (convert_to_markdown(' '.join(args.request), answers))
    # print(markdown.markdown(convert_to_markdown(' '.join(args.request), answers))) # html
    
