import osninja.banner

import osninja.mem

import argparse
import json
import time 
import os

import osninja.scanner

from colorama import Fore, Style

from urllib.parse import urlparse
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(prog=osninja.__program__, description=osninja.__description__) 

parser.add_argument('-u', help='input target host(s) to scan', dest='urls')
parser.add_argument('-l', help='input file containing list of hosts to process', dest='list')
parser.add_argument('-o', help='folder to write output results', dest='out_folder')
parser.add_argument('-p', help='http proxy to use', dest='http_proxy')
parser.add_argument('-rl', help='maximum requests to send per second (default 150)', dest='rate_limit', type=int, default=150)
parser.add_argument('-H',  help='custom http headers to send with request. can be supplied multiple times', dest='headers', action='append')
parser.add_argument('-k', help='list of known applications on the target', dest='known')

args = parser.parse_args() 

if args.list:
    with open(args.list, 'r') as f:
        osninja.mem.config['urls'] = f.readlines()
elif args.urls:
    osninja.mem.config['urls'] = args.urls.split(',')
else:
    parser.print_help()
    exit()

if args.out_folder:
    if os.path.exists(args.out_folder):
        print(f'{Fore.RED}[!] Output folder already exists: {args.out_folder}{Style.RESET_ALL}')
        exit()
else:
    osninja.mem.config['out_folder'] = f'out_{time.strftime("%H-%M-%S")}'

if args.http_proxy:
    osninja.mem.config['http_proxy'] = args.http_proxy

if args.rate_limit:
    osninja.mem.config['rate_limit'] = args.rate_limit

if args.headers:
    print(args.headers)

if args.known:
    osninja.mem.config['known'] = args.known.split(',')



def main():
    os.mkdir(osninja.mem.config['out_folder'])
    result = {}
    try:
        for url in osninja.mem.config['urls']:
            url = url.strip()
            print(f'{Fore.GREEN}[*] Scanning {url}{Style.RESET_ALL}')
            osninja.mem.config['current_target'] = url 
            result = osninja.scanner.scan(url)
            print(f'{Fore.GREEN}[*] Done scanning {url}{Style.RESET_ALL}')
        
            result['scanned_modules'] = list(result['scanned_modules'])

    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print(f'{Fore.RED}[!] Error: {e}{Style.RESET_ALL}')
    finally:
        for url in osninja.mem.config['urls']:
            hostname = urlparse(url).hostname
            with open(f'{osninja.mem.config["out_folder"]}/{hostname}.json', 'w') as f:
                json.dump(result, f, indent=4)

        print(f'{Fore.GREEN}[*] Results saved in {osninja.mem.config["out_folder"]}{Style.RESET_ALL}')
if __name__ == '__main__':
    main()