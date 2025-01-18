import re
import time
from hyperloglog import HyperLogLog

def load_ips_from_log(file_path):
    """
    Reads a log file line by line and extracts valid IP addresses.
    Also counts the total number of lines and valid IP addresses for debugging purposes.

    :param file_path: Path to the log file.
    :return: Generator yielding valid IP addresses.
    """
    ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
    total_lines = 0
    valid_ips_count = 0

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            total_lines += 1
            match = ip_pattern.search(line)
            if match:
                valid_ips_count += 1
                yield match.group(0)

    print(f"Total lines: {total_lines}, Valid IPs: {valid_ips_count}")

def exact_count_unique_ips(ip_iterable):
    """
    Counts the exact number of unique IPs using a Python set.

    :param ip_iterable: Iterable of IP addresses (e.g., list, generator).
    :return: Tuple containing the count of unique IPs and elapsed time in seconds.
    """
    start_time = time.time()
    unique_ips = set(ip_iterable)
    count_result = len(unique_ips)
    elapsed_time = time.time() - start_time
    return count_result, elapsed_time

def approx_count_unique_ips_hll(ip_iterable, error_rate=0.01):
    """
    Counts the approximate number of unique IPs using HyperLogLog.

    :param ip_iterable: Iterable of IP addresses (e.g., list, generator).
    :param error_rate: Desired error rate for HyperLogLog (default is 1%).
    :return: Tuple containing the approximate count of unique IPs and elapsed time in seconds.
    """
    start_time = time.time()
    hll = HyperLogLog(error_rate=error_rate)
    for ip in ip_iterable:
        hll.add(ip)
    count_result = len(hll)
    elapsed_time = time.time() - start_time
    return count_result, elapsed_time

def print_comparison_table(exact_count, exact_time, hll_count, hll_time):
    """
    Prints a simple comparison table for exact counting vs. HyperLogLog.

    :param exact_count: Number of unique elements (exact method).
    :param exact_time: Time taken for the exact method (seconds).
    :param hll_count: Number of unique elements (HyperLogLog method).
    :param hll_time: Time taken for the HyperLogLog method (seconds).
    """
    print("Comparison Results:\n")
    header = f"{'':<24} {'Exact Count':<16} {'HyperLogLog':<16}"
    row1 = f"{'Unique Elements':<24} {exact_count:<16.1f} {hll_count:<16.1f}"
    row2 = f"{'Execution Time (s)':<24} {exact_time:<16.3f} {hll_time:<16.3f}"
    print(header)
    print(row1)
    print(row2)

if __name__ == "__main__":
    # Specify the path to your log file
    log_file_path = "./lms-stage-access.log"  # Replace with the correct path to your log file

    # Load IPs from the log file and print debugging information
    ip_generator = load_ips_from_log(log_file_path)

    # Exact counting
    print("Performing exact counting...")
    exact_result, exact_time = exact_count_unique_ips(list(ip_generator))

    # Reload the generator for approximate counting
    ip_generator = load_ips_from_log(log_file_path)

    # Approximate counting using HyperLogLog
    print("Performing approximate counting with HyperLogLog...")
    hll_result, hll_time = approx_count_unique_ips_hll(ip_generator, error_rate=0.01)

    # Print the comparison table
    print_comparison_table(exact_result, exact_time, hll_result, hll_time)
