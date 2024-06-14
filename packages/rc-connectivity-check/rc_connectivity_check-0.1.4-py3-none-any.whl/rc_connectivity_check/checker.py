import argparse
from collections import defaultdict
import socket
from typing import DefaultDict, Dict, List, NamedTuple, Tuple
import requests
import time
from statistics import mean
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from colorama import Fore, Style, init
import urllib3


# Initialize colorama
init(autoreset=True)

# Define the hostnames
hostnames = ["www.revenuecat.com", "app.revenuecat.com", "api.revenuecat.com"]


# Function to resolve DNS and get all IPs
def resolve_dns(hostname: str) -> List[str]:
    try:
        return socket.gethostbyname_ex(hostname)[2]
    except socket.gaierror:
        return []


class TestResult(NamedTuple):
    hostname: str
    ip: str
    failures: int
    min_latency: float
    max_latency: float
    avg_latency: float


def get_request_on_custom_ip(
    ip: str,
    domain: str,
    location: str,
    https: bool,
    timeout: int,
) -> Tuple[int, bytes]:
    if https:
        pool = urllib3.HTTPSConnectionPool(
            ip,
            server_hostname=domain,
            timeout=timeout,
            retries=False,
        )
    else:
        pool = urllib3.HTTPConnectionPool(
            ip,
            timeout=timeout,
            retries=False,
        )
    response = pool.request(
        "GET",
        location,
        headers={"Host": domain},
        redirect=False,
    )
    return response.status, response.data


# Function to issue HTTP requests and measure latencies
def measure_latency(
    ip: str, hostname: str, https: bool = False, timeout: int = 5
) -> TestResult:
    latencies: List[float] = []
    failures = 0

    for _ in range(10):
        start_time = time.time()
        try:
            status_code, _ = get_request_on_custom_ip(
                ip, hostname, "/favicon-32x32.png", https, timeout
            )
            if status_code < 400:
                ok = True
            elif status_code == 404 and hostname == "api.revenuecat.com":
                ok = True
            else:
                ok = False

            if not ok:
                raise Exception(
                    f"Failed to fetch from {hostname} at {ip}:{443 if https else 80}: {status_code}"
                )
        except Exception as e:
            print(f"{error('ERROR')}: Failed to connect to {hostname} at {ip}: {e}")
            failures += 1
        latency = time.time() - start_time
        latencies.append(latency)

    return TestResult(
        hostname=f"{'https' if https else 'http'}://{hostname}",
        ip=ip,
        failures=failures,
        min_latency=min(latencies, default=0),
        max_latency=max(latencies, default=0),
        avg_latency=mean(latencies) if latencies else 0,
    )


# Function to print results with colors
def print_results(hostname: str, results: List[TestResult]):
    print(f"\nResults for {color(hostname, Fore.CYAN)}:")
    for result in results:
        if result.failures == 0:
            res = ok("OK")
        else:
            res = error(f"FAILURES [{result.failures}/10]")

        print(f"  - {color(result.ip, Fore.YELLOW)}: {res}")
        print(
            f"    Latencies (min/max/avg): {result.avg_latency*1000:.1f}ms / {result.max_latency*1000:.1f}ms / {result.avg_latency*1000:.1f}ms"
        )


def color(msg: str, color: Fore) -> str:
    return f"{color}{msg}{Style.RESET_ALL}"


def error(msg: str):
    return color(msg, Fore.RED)


def ok(msg: str):
    return color(msg, Fore.GREEN)


def find_client_ip() -> str:
    try:
        return requests.get("http://ifconfig.me/ip").text.strip()
    except requests.RequestException as e:
        print(f"{error('ERROR')}: Failed to get client IP: {e}")
        return "Unknown"


# Main logic
def main():
    parser = argparse.ArgumentParser(description="RevenueCat Connectivity Check tool")
    parser.add_argument(
        "--timeout",
        type=int,
        default=5,
        help="Request timeout, in seconds (default: 5)",
    )
    args = parser.parse_args()

    print("Finding client Public IP...")
    ip = find_client_ip()
    print(f"Client Public IP: {color(ip, Fore.YELLOW)}")

    print("")
    print("Resolving hostnames...")
    hostname_ips: Dict[str, List[str]] = {}
    for hostname in hostnames:
        ips = resolve_dns(hostname)
        if not ips:
            print(f"* {color(Fore.CYAN, hostname)}: {error('Failed to resolve')}")
            continue
        print(f"* {color(Fore.CYAN, hostname)}: {ok('Resolved ok')}")
        for ip in ips:
            print(f"  - {ip}")
        hostname_ips[hostname] = ips

    print("")
    print("Connectivity check...")
    with ThreadPoolExecutor() as executor:
        futures: List[Future[TestResult]] = []
        for hostname, ips in hostname_ips.items():
            for ip in ips:
                for https in [True, False]:
                    futures.append(
                        executor.submit(
                            measure_latency, ip, hostname, https, args.timeout
                        )
                    )

        results: DefaultDict[str, List[TestResult]] = defaultdict(list)
        for future in as_completed(futures):
            try:
                result = future.result()
                results[result.hostname].append(result)
            except Exception as e:
                print(f"{error('ERROR')}: Error ocurred: {e}")

        for hostname, res in results.items():
            print_results(hostname, res)

        failed_ips = set()
        for res in results:
            for result in results[res]:
                if result.failures > 0:
                    failed_ips.add(result.ip)

        if failed_ips:
            print()
            print(error("There were some connectivity failures!"))
            print("Please help us investigate by following the next steps:")
            print()
            print("1: Check network routes:")
            print("  - Install mtr:")
            print("    - macOS: brew install mtr")
            print("    - Ubuntu: sudo apt-get install mtr")
            print("  - Run mtr using the following command:")
            print(
                "    sudo mtr --report -n --tcp --port=443 --gracetime=5 --timeout=5 "
                + " ".join(failed_ips)
            )
            print()
            tcpdump_cmd = "tcpdump -i <INTERFACE> -w rc_connectivity_check.pcap -s 0 tcp and port 80"
            print("2: Capture network traffic while running this script:")
            print("  - In one terminal run:")
            print("    - On macOS, over WIFI:")
            print("      " + tcpdump_cmd.replace("<INTERFACE>", "en0"))
            print("    - On macOS, over ethernet:")
            print("      " + tcpdump_cmd.replace("<INTERFACE>", "en1"))
            print("    - On linux, find the interface name with ifconfig and use:")
            print("      " + tcpdump_cmd)
            print("  - In another terminal, run this script again:")
            print("    rc-connectivity-check")
            print("  - Once completed, stop the tcpdump process with `Ctrl+C`")
            print(
                "  - Send the resulting rc_connectivity_check.pcap file to RevenueCat support"
            )


if __name__ == "__main__":
    main()
