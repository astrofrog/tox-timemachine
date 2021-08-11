import sys
from datetime import datetime
import subprocess

def parse_iso(dt):
    try:
        return datetime.strptime(dt, '%Y-%m-%d')
    except:
        return datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S')


def main():

    _, start_date, end_date, *args = sys.argv

    start = parse_iso(start_date)
    end = parse_iso(end_date)

    while True:

        if (end - start).total_seconds() < 3600:
            break

        target = start + (end - start) / 2.

        target_iso = target.isoformat()[:19]

        command = [sys.executable, '-m', 'tox', '--time-travel=' + target_iso] + args
        log_file = f'{target_iso}.log'

        print(f'Running {command} and outputting to {log_file}')

        with open(log_file, 'w') as out_file:
            exitcode = subprocess.call(command, stdout=out_file, stderr=out_file)

        if exitcode == 0:
            start = target
        else:
            end = target

    print(f"Build started failing between {start.isoformat()[:19]} and {end.isoformat()[:19]}")
