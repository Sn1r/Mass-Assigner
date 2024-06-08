import requests
import argparse
import json
import urllib3
import time

from ansi_colors import *
from banner import print_banner

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def parse_headers(headers):
    headers_dict = {}
    if headers:
        for header in headers:
            key, value = header.split(":", 1)
            headers_dict[key.strip()] = value.strip()
    return headers_dict

def handle_json_response(response, url, method, headers):
    try:
        if response.status_code == 200 and response.headers.get("Content-Type") == "application/json":
            response_data = response.json()
            if isinstance(response_data, dict):
                modify_and_send_requests(url, method, headers, response_data)
            else:
                print("[-] The response JSON is not an object.")
        else:

            status_code = response.status_code

            if status_code in (200, 201, 202):
                status_color = GREEN
            elif status_code in (401, 403, 404, 405, 500, 501, 502, 503, 504, 505):
                status_color = RED
            elif status_code in (301, 302):
                status_color = YELLOW
            else:
                status_color = RESET

            print(f"{RED}[-] Failed to get a valid JSON response for '{url}'.{RESET}")
            print(f"Status Code: {status_color}{status_code}{RESET}")
            print("Response Body:", response.text)
    
    except json.JSONDecodeError:
        print(f"{RED}[-] Failed to decode JSON response from {url}.{RESET}")
        

def modify_and_send_request(url, method, headers, response_data, args):

    ignored_params = set(args.ignore_params.split(',') if args.ignore_params else set())
    modification_successful = False

    for key, value in response_data.items():

        if key in ignored_params:
            print(f"{YELLOW}[i] The '{key}' parameter is ignored and won't be modified.{RESET}\n")
            continue

        modified_data = {}
        if isinstance(value, bool):
            modified_data[key] = not value
        elif isinstance(value, int):
            modified_data[key] = value + 1
        elif isinstance(value, str):
            modified_data[key] = value + "_modified"
        else:
            continue
        
        if args.proxy:
            response = requests.request(method, url, headers=headers, json=modified_data, proxies={"http": args.proxy, "https": args.proxy}, verify=False)

        response = requests.request(method, url, headers=headers, json=modified_data)

        if args.rate_limit:
            time.sleep(1 / float(args.rate_limit))

        status_code = response.status_code

        if status_code in (200, 201, 202):
            modification_successful = True
            status_color = GREEN
        elif status_code in (401, 403, 404, 405, 500, 501, 502, 503, 504, 505):
            status_color = RED
        elif status_code in (301, 302):
            status_color = YELLOW
        else:
            status_color = RESET

        print(f"{YELLOW}[i] Attempting to modify the '{key}' key:{RESET}")
        print(f"[+] Status Code: {status_color}{status_code}{RESET}")
        print(f"[+] Response Body: \n{response.text}\n")

        if not modification_successful:
            print(f"{RED}[-] Modification attempt failed.\n{RESET}")
            continue
        
    if modification_successful:
        print(f"{GREEN}[+] All modification attempts completed.{RESET}")

def invoke_web_request(url, args, method, headers=None):
    headers_dict = parse_headers(headers)

    if args.proxy:
        response = requests.request(method, url, headers=headers_dict, proxies={"http": args.proxy, "https": args.proxy}, verify=False)
    else:
        response = requests.request(method, url, headers=headers_dict)
    
        return response

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fetch-from", help="URL to fetch data from", required=True)
    parser.add_argument("--target-req", help="URL to send modified data to", required=True)
    parser.add_argument("-H", "--header", action="append", help="Add a custom header. Format: 'Key: Value'")
    parser.add_argument("-p", "--proxy", help="Use Proxy, Usage i.e: http://127.0.0.1:8080.")
    parser.add_argument("--rate-limit", help="Number of requests per second")
    parser.add_argument("--first-method", help="HTTP method for the initial request. Default is GET.", default="GET")
    parser.add_argument("--second-method", help="HTTP method for the modified request. Default is PUT.", default="PUT")
    parser.add_argument("--ignore-params", help="Parameters to ignore during modification, separated by comma.")

    args = parser.parse_args()

    invoke_web_request(url=args.fetch_from, method=args.first_method, headers=args.header, args=args)

    response = requests.request(args.first_method, args.fetch_from, headers=parse_headers(args.header))
    if response.status_code == 200:
        response_data = response.json()
        if isinstance(response_data, dict):
            modify_and_send_request(args.target_req, args.second_method, parse_headers(args.header), response_data, args=args)
        else:
            print("[-] The response JSON is not an object.")
    else:
        print(f"\n{RED}[!] Failed to get a valid JSON response for '{args.fetch_from}'.{RESET}")
    

if __name__ == "__main__":
    print_banner()
    main()
