import re
import time
from hyperloglog import HyperLogLog

def load_ips_from_log(file_path):
    """
    Reads a log file line by line, extracting the IP address if it exists.
    Returns a list of valid IP addresses.
    """
    ip_pattern = re.compile(r'(\d{1,3}\.){3}\d{1,3}')
    valid_ips = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = ip_pattern.search(line)
            if match:
                valid_ips.append(match.group(0))
            # If the line doesn't contain a valid IP address, we ignore it

    return valid_ips


def exact_count_unique_ips(ip_list):
    """
    Counts the number of unique IPs using a Python set.
    This method is exact but may use more memory for very large datasets.
    """
    start_time = time.time()
    unique_ips = set(ip_list)
    count_result = len(unique_ips)
    elapsed_time = time.time() - start_time
    return count_result, elapsed_time


def approx_count_unique_ips_hll(ip_list, error_rate=0.01):
    """
    Counts the number of unique IPs using HyperLogLog (approximate).
    :param ip_list: list of IP addresses (strings)
    :param error_rate: desired error rate for HyperLogLog
    """
    start_time = time.time()
    hll = HyperLogLog(error_rate=error_rate)
    for ip in ip_list:
        hll.add(ip)
    count_result = len(hll)
    elapsed_time = time.time() - start_time
    return count_result, elapsed_time


def print_comparison_table(exact_count, exact_time, hll_count, hll_time):
    """
    Prints a simple comparison table of results: exact vs. HyperLogLog.
    """
    print("Comparison Results:\n")
    header = f"{'':<24} {'Exact Count':<16} {'HyperLogLog':<16}"
    row1  = f"{'Unique Elements':<24} {exact_count:<16.1f} {hll_count:<16.1f}"
    row2  = f"{'Execution Time (s)':<24} {exact_time:<16.3f} {hll_time:<16.3f}"
    print(header)
    print(row1)
    print(row2)


if __name__ == "__main__":
    # 1. Load the IP addresses from the log file
    log_file_path = "lms-stage-access.log"  # Change this path to your log file
    ip_list = load_ips_from_log(log_file_path)

    # 2. Exact counting
    exact_result, exact_time = exact_count_unique_ips(ip_list)

    # 3. Approx counting with HyperLogLog
    #    The smaller the error_rate, the more memory/time is used, but the result is more accurate.
    hll_result, hll_time = approx_count_unique_ips_hll(ip_list, error_rate=0.01)

    # 4. Print comparison table
    print_comparison_table(exact_result, exact_time, hll_result, hll_time)
