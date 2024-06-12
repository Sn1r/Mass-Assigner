# Mass Assigner

Mass Assigner is a powerful tool designed to identify and exploit mass assignment vulnerabilities in web applications. It achieves this by first retrieving data from a specified request, such as fetching user profile data. Then, it systematically attempts to apply each parameter extracted from the response to a second request provided, one parameter at a time. This approach allows for the automated testing and exploitation of potential mass assignment vulnerabilities. **This code is made for security enthusiasts and professionals only. Use it at your own risk.**

## 🪄 Features

- Enables the addition of custom headers within requests
- Offers customization of various HTTP methods for both origin and target requests
- Supports rate-limiting to manage request thresholds effectively
- Provides the option to specify "ignored parameters" which the tool will ignore during execution

### 🔮 What's Next 
- Support additional content types, such as "application/x-www-form-urlencoded"
- Improving the support in nested arrays/objects inside JSON data in responses
  
## Installation & Usage
Install requirements

```bash
pip3 install -r requirements.txt
```

Run the script

```bash
python3 mass_assigner.py --fetch-from "http://example.com/path-to-fetch-data" --target-req "http://example.com/path-to-probe"
```

## Arguments
Forbidden Buster accepts the following arguments:

```bash
  -h, --help            show this help message and exit
  --fetch-from FETCH_FROM
                        URL to fetch data from
  --target-req TARGET_REQ
                        URL to send modified data to
  -H HEADER, --header HEADER
                        Add a custom header. Format: 'Key: Value'
  -p PROXY, --proxy PROXY
                        Use Proxy, Usage i.e: http://127.0.0.1:8080.
  -d DATA, --data DATA  Add data to the request body. JSON is supported with escaping.
  --rate-limit RATE_LIMIT
                        Number of requests per second
  --first-method FIRST_METHOD
                        HTTP method for the initial request. Default is GET.
  --second-method SECOND_METHOD
                        HTTP method for the modified request. Default is PUT.
  --ignore-params IGNORE_PARAMS
                        Parameters to ignore during modification, separated by comma.
```

Example Usage:
```bash
python3 mass_assigner.py --fetch-from "http://example.com/api/v1/me" --target-req "http://example.com/api/v1/me" --header "Authorization: Bearer XXX" --proxy "http://proxy.example.com" --data '{\"param1\": \"test\", \"param2\":true}'

```
