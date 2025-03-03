#!/usr/bin/env spack-python
"""
This script is meant to be run using:
    `spack python aggregate_logs.spack.py`
"""

import os

from llnl.util.tty import tty


def find_logs(prefix, filename):
    for root, _, files in os.walk(prefix):
        if filename in files:
            yield os.path.join(root, filename)


if __name__ == "__main__":
    import json
    from argparse import ArgumentParser

    parser = ArgumentParser("aggregate_logs")
    parser.add_argument("output_file")
    parser.add_argument("--log", default="install_times.json")
    parser.add_argument("--prefix", required=True)

    args = parser.parse_args()

    prefixes = [p for p in args.prefix.split(":") if os.path.exists(p)]

    # Aggregate the install timers into a single json
    data = []

    # Look in the CWD for logs
    local_log_path = os.path.join(os.getcwd(), args.log)
    if os.path.exists(local_log_path):
        with open(local_log_path, encoding="utf-8") as fd:
            data.append(json.load(fd))

    # Look in the list of prefixes for logs
    for prefix in prefixes:
        logs = [log for log in find_logs(prefix, args.log)]
        for log in logs:
            tty.debug(f"appending data for {log}")
            with open(log, encoding="utf-8") as fd:
                data.append(json.load(fd))

    tty.info(f"Writing {len(data)} records to {args.output_file}")
    with open(args.output_file, "w", encoding="utf-8") as fd:
        json.dump(data, fd)
