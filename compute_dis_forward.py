import re
import sys
import statistics

def process_log(file_path):
    ratios = []

    # 正则
    forward_pattern = re.compile(r'\[forward\]:(\d+\.\d+)ms')
    dis_pattern = re.compile(r'\[dis_\d+\]:(\d+\.\d+)ms')

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # 只处理包含 dis_xxx 的行
            if '[dis_' not in line:
                continue

            # 提取 forward
            forward_match = forward_pattern.search(line)
            if not forward_match:
                continue
            forward_time = float(forward_match.group(1))

            # 提取所有 dis_xxx
            dis_matches = dis_pattern.findall(line)
            if not dis_matches:
                continue

            dis_sum = sum(float(x) for x in dis_matches)

            # 避免除0
            if forward_time == 0:
                continue

            ratio = dis_sum / forward_time
            ratios.append(ratio)

    if not ratios:
        print("No valid data found.")
        return

    # 排序
    ratios.sort()

    # 统计
    min_ratio = min(ratios)
    max_ratio = max(ratios)
    median_ratio = statistics.median(ratios)
    avg_ratio = sum(ratios) / len(ratios)

    # 输出文件
    output_file = "dis_ratio_stats.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Sorted ratios:\n")
        for r in ratios:
            f.write(f"{r:.6f}\n")

        f.write("\nStatistics:\n")
        f.write(f"Count: {len(ratios)}\n")
        f.write(f"Min: {min_ratio:.6f}\n")
        f.write(f"Max: {max_ratio:.6f}\n")
        f.write(f"Median: {median_ratio:.6f}\n")
        f.write(f"Average: {avg_ratio:.6f}\n")

    print(f"Done. Results written to {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <log_file>")
    else:
        process_log(sys.argv[1])