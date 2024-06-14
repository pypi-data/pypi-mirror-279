import re

import matplotlib.pyplot as plt
import numpy

from . import cli

__project_name__ = "fardoes"


def main() -> int:
    args = cli.parse_args()

    with open(args.log_file, "r") as file:
        log = file.read()

    containers, times = parse_log(log)

    mean_time = numpy.mean(times)
    std_time = numpy.std(times)
    min_time = numpy.min(times)
    max_time = numpy.max(times)

    print(f"Mean time: {format_duration(mean_time)}")
    print(f"Standard deviation: {format_duration(std_time)}")
    print(f"Minimum time: {format_duration(min_time)}")
    print(f"Maximum time: {format_duration(max_time)}")

    plt.plot(containers, times, marker="o")
    plt.xlabel("Number of Containers")
    plt.ylabel("Time (seconds)")
    plt.title("Container Start Time")
    plt.grid(True)
    plt.show()

    return 0


def parse_log(log):
    pattern = r"Processed (\d+) containers in (\d+\.\d+)s"
    matches = re.findall(pattern, log)
    data = [(int(containers), float(time)) for containers, time in matches]
    return zip(*data)


def format_duration(seconds):
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    return f"{minutes} minutes {remaining_seconds} seconds"


if __name__ == "__main__":
    main()
