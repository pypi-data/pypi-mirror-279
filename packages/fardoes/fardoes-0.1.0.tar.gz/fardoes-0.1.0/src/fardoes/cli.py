import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Analyze container start times from a log file."
    )
    parser.add_argument(
        "--log-file",
        type=str,
        default="./log.txt",
        help="Path to the log file (default: ./log.txt)",
    )
    return parser.parse_args()
