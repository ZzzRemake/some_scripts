import re
import sys
import statistics
import math

def percentile(data, p):
    """
    计算百分位（如 P99）
    使用常见的线性插值方法
    """
    if not data:
        return None
    k = (len(data) - 1) * (p / 100)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return data[int(k)]
    return data[f] * (c - k) + data[c] * (k - f)


def process_log(file_path):
    ratios = []
    forward_times = []

    forward_pattern = re.compile(r'\[forward\]:(\d+\.\d+)ms')
    dis_pattern = re.compile(r'\[dis_\d+\]:(\d+\.\d+)ms')

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if '[dis_' not in line:
                continue

            forward_match = forward_pattern.search(line)
            if not forward_match:
                continue

            forward_time = float(forward_match.group(1))
            if forward_time == 0:
                continue

            dis_matches = dis_pattern.findall(line)
            if not dis_matches:
                continue

            dis_sum = sum(float(x) for x in dis_matches)

            ratio = dis_sum / forward_time

            ratios.append(ratio)
            forward_times.append(forward_time)

    if not ratios:
        print("No valid data found.")
        return

    # 排序
    ratios.sort()
    forward_times.sort()

    # === ratio统计 ===
    ratio_min = ratios[0]
    ratio_max = ratios[-1]
    ratio_median = statistics.median(ratios)
    ratio_avg = sum(ratios) / len(ratios)
    ratio_p99 = percentile(ratios, 99)

    # === forward统计 ===
    f_min = forward_times[0]
    f_max = forward_times[-1]
    f_median = statistics.median(forward_times)
    f_avg = sum(forward_times) / len(forward_times)
    f_p99 = percentile(forward_times, 99)

    # 输出文件
    output_file = "dis_ratio_stats.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=== Sorted Ratios ===\n")
        for r in ratios:
            f.write(f"{r:.6f}\n")

        f.write("\n=== Ratio Statistics ===\n")
        f.write(f"Count: {len(ratios)}\n")
        f.write(f"Min: {ratio_min:.6f}\n")
        f.write(f"Max: {ratio_max:.6f}\n")
        f.write(f"Median: {ratio_median:.6f}\n")
        f.write(f"Average: {ratio_avg:.6f}\n")
        f.write(f"P99: {ratio_p99:.6f}\n")

        f.write("\n=== Forward Time Statistics (ms) ===\n")
        f.write(f"Count: {len(forward_times)}\n")
        f.write(f"Min: {f_min:.6f}\n")
        f.write(f"Max: {f_max:.6f}\n")
        f.write(f"Median: {f_median:.6f}\n")
        f.write(f"Average: {f_avg:.6f}\n")
        f.write(f"P99: {f_p99:.6f}\n")

    print(f"Done. Results written to {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <log_file>")
    else:
        process_log(sys.argv[1])