# RC Connectivity Check tools

This PIP package measures the latencies to various hosts and provides statistics such as failure rates and latencies.

## Installation

```bash
pip install rc_connectivity_check
```

## Usage
Just run `rc-connectivity-check`

Also accepts an optional `--timeout` flag to increase request timeouts:
```
usage: checker.py [-h] [--timeout TIMEOUT]

RevenueCat Connectivity Check tool

options:
  -h, --help         show this help message and exit
  --timeout TIMEOUT  Request timeout, in seconds (default: 5)
```

Example output (simulating an error):
```
$ rc-connectivity-check
Finding client Public IP...
Client Public IP: 1.2.3.4

Resolving hostnames...
* www.revenuecat.com: Resolved ok
  - 18.154.22.73
  - 18.154.22.30
  - 18.154.22.107
  - 18.154.22.26
* app.revenuecat.com: Resolved ok
  - 108.157.109.77
  - 108.157.109.6
  - 108.157.109.82
  - 108.157.109.103
* api.revenuecat.com: Resolved ok
  - 34.196.186.56
  - 52.22.245.243
  - 3.208.129.96
  - 54.163.59.173
  - 3.214.67.56
  - 3.223.26.133
  - 1.2.3.4

Connectivity check...
ERROR: Failed to connect to api.revenuecat.com at 1.2.3.4: (<urllib3.connection.HTTPSConnection object at 0x105e60b90>, 'Connection to 1.2.3.4 timed out. (connect timeout=5)')
ERROR: Failed to connect to api.revenuecat.com at 1.2.3.4: (<urllib3.connection.HTTPConnection object at 0x105e611c0>, 'Connection to 1.2.3.4 timed out. (connect timeout=5)')
[...]
ERROR: Failed to connect to api.revenuecat.com at 1.2.3.4: (<urllib3.connection.HTTPSConnection object at 0x105e60440>, 'Connection to 1.2.3.4 timed out. (connect timeout=5)')
ERROR: Failed to connect to api.revenuecat.com at 1.2.3.4: (<urllib3.connection.HTTPSConnection object at 0x105e78ef0>, 'Connection to 1.2.3.4 timed out. (connect timeout=5)')

Results for http://www.revenuecat.com:
  - 18.154.22.30: OK
    Latencies (min/max/avg): 16.6ms / 20.0ms / 16.6ms
  - 18.154.22.73: OK
    Latencies (min/max/avg): 17.5ms / 20.8ms / 17.5ms
  - 18.154.22.26: OK
    Latencies (min/max/avg): 17.4ms / 20.1ms / 17.4ms
  - 18.154.22.107: OK
    Latencies (min/max/avg): 17.7ms / 24.1ms / 17.7ms

Results for http://app.revenuecat.com:
  - 108.157.109.77: OK
    Latencies (min/max/avg): 17.1ms / 21.8ms / 17.1ms
  - 108.157.109.6: OK
    Latencies (min/max/avg): 18.3ms / 22.6ms / 18.3ms
  - 108.157.109.82: OK
    Latencies (min/max/avg): 19.0ms / 23.6ms / 19.0ms
  - 108.157.109.103: OK
    Latencies (min/max/avg): 18.9ms / 25.7ms / 18.9ms

Results for https://app.revenuecat.com:
  - 108.157.109.6: OK
    Latencies (min/max/avg): 36.7ms / 42.8ms / 36.7ms
  - 108.157.109.82: OK
    Latencies (min/max/avg): 34.4ms / 44.4ms / 34.4ms
  - 108.157.109.103: OK
    Latencies (min/max/avg): 35.8ms / 43.1ms / 35.8ms
  - 108.157.109.77: OK
    Latencies (min/max/avg): 60.9ms / 277.5ms / 60.9ms

Results for https://www.revenuecat.com:
  - 18.154.22.26: OK
    Latencies (min/max/avg): 46.9ms / 154.1ms / 46.9ms
  - 18.154.22.30: OK
    Latencies (min/max/avg): 47.6ms / 154.1ms / 47.6ms
  - 18.154.22.107: OK
    Latencies (min/max/avg): 48.0ms / 148.6ms / 48.0ms
  - 18.154.22.73: OK
    Latencies (min/max/avg): 50.7ms / 154.0ms / 50.7ms

Results for http://api.revenuecat.com:
  - 34.196.186.56: OK
    Latencies (min/max/avg): 182.3ms / 190.7ms / 182.3ms
  - 52.22.245.243: OK
    Latencies (min/max/avg): 175.9ms / 178.9ms / 175.9ms
  - 54.163.59.173: OK
    Latencies (min/max/avg): 176.3ms / 195.9ms / 176.3ms
  - 3.208.129.96: OK
    Latencies (min/max/avg): 181.0ms / 191.7ms / 181.0ms
  - 3.214.67.56: OK
    Latencies (min/max/avg): 178.3ms / 186.5ms / 178.3ms
  - 3.223.26.133: OK
    Latencies (min/max/avg): 170.9ms / 177.1ms / 170.9ms
  - 1.2.3.4: FAILURES [10/10]
    Latencies (min/max/avg): 5004.7ms / 5007.9ms / 5004.7ms

Results for https://api.revenuecat.com:
  - 34.196.186.56: OK
    Latencies (min/max/avg): 361.0ms / 378.4ms / 361.0ms
  - 52.22.245.243: OK
    Latencies (min/max/avg): 363.8ms / 388.3ms / 363.8ms
  - 54.163.59.173: OK
    Latencies (min/max/avg): 365.8ms / 376.5ms / 365.8ms
  - 3.208.129.96: OK
    Latencies (min/max/avg): 371.7ms / 404.5ms / 371.7ms
  - 3.214.67.56: OK
    Latencies (min/max/avg): 369.5ms / 392.8ms / 369.5ms
  - 3.223.26.133: OK
    Latencies (min/max/avg): 369.6ms / 388.6ms / 369.6ms
  - 1.2.3.4: FAILURES [10/10]
    Latencies (min/max/avg): 5006.7ms / 5012.6ms / 5006.7ms

There were some connectivity failures!
Please help us investigate by following the next steps:

1: Check network routes:
  - Install mtr:
    - macOS: brew install mtr
    - Ubuntu: sudo apt-get install mtr
  - Run mtr using the following command:
    sudo mtr --report -n --tcp --port=443 --gracetime=5 --timeout=5 1.2.3.4

2: Capture network traffic while running this script:
  - In one terminal run:
    - On macOS, over WIFI:
      tcpdump -i en0 -w rc_connectivity_check.pcap -s 0 tcp and port 80
    - On macOS, over ethernet:
      tcpdump -i en1 -w rc_connectivity_check.pcap -s 0 tcp and port 80
    - On linux, find the interface name with ifconfig and use:
      tcpdump -i <INTERFACE> -w rc_connectivity_check.pcap -s 0 tcp and port 80
  - In another terminal, run this script again:
    rc-connectivity-check
  - Once completed, stop the tcpdump process with `Ctrl+C`
  - Send the resulting rc_connectivity_check.pcap file to RevenueCat support
```
