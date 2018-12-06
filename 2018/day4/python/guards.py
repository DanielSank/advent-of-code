import collections
import datetime
import re

import numpy as np


RE = re.compile(r'\[(\d\d\d\d)-(\d\d)-(\d\d) (\d\d):(\d\d)\] (.+)')
SHIFT_BEGIN = re.compile(r'Guard #([0-9]+) begins shift')


Log = collections.namedtuple("Log", ["datetime", "text"])
# Event types
GuardShift = collections.namedtuple("GuardShift", ["number", "datetime"])
Wakeup = collections.namedtuple("Wakeup", ["datetime"])
FallAsleep = collections.namedtuple("FallAsleep", ["datetime"])


class GuardRecord:
    def __init__(self):
        self.laziest_minute = None
        self.sleep_record = {} # minute -> sleep count

    @property
    def time_at_laziest_minute(self):
        try:
            return self.sleep_record[self.laziest_minute]
        except KeyError:
            return 0


def line_to_log(line):
    """Convert a test line to a Log"""
    result = RE.match(line).groups()
    return Log(
        datetime.datetime(*(int(x) for x in result[:-1])),
        result[-1],)


def log_to_event(log):
    """Convert a Log to an Event"""
    event_text = log.text
    if 'begins shift' in event_text:
        guard_number = int(SHIFT_BEGIN.match(event_text).groups()[0])
        return GuardShift(guard_number, log.datetime)
    elif event_text == 'wakes up':
        return Wakeup(log.datetime)
    elif event_text == 'falls asleep':
        return FallAsleep(log.datetime)
    else:
        raise ValueError("Could not parse: {}".format(event_text))


def sort_logs(logs):
    return sorted(logs, key = lambda log: log.datetime)


def get_sorted_events(filename):
    with open(filename) as f:
        lines = f.read().split('\n')[0:-1]
    logs = [line_to_log(line) for line in lines]
    events = [log_to_event(log) for log in sort_logs(logs)]
    return events


def scan_events(events):
    """Build a lookup table of which guard was asleep at which minutes."""
    guard_records = {}  # id -> GuardRecord
    active_guard = None
    fell_asleep_at_minute = None

    for event in events:
        if type(event) is GuardShift:
            active_guard = event.number
        elif type(event) is FallAsleep:
            fell_asleep_at_minute = event.datetime.minute
        elif type(event) is Wakeup:
            wakeup_at_minute = event.datetime.minute
            record = guard_records.setdefault(
                active_guard,
                GuardRecord(),)
            for minute in np.arange(fell_asleep_at_minute, wakeup_at_minute):
                count = record.sleep_record.setdefault(minute, 0) + 1
                if count > record.time_at_laziest_minute:
                    record.laziest_minute = minute
                record.sleep_record[minute] = count
    return guard_records


def find_laziest_guard(guard_records):
    laziest = None
    longest_sleep = 0
    for guard_id, record in guard_records.items():
        total_sleep = sum(record.sleep_record.values())
        if total_sleep > longest_sleep:
            laziest = guard_id
            longest_sleep = total_sleep
            print("Setting laziest to {} with total {}".format(
                laziest, total_sleep))
    return laziest


def part_1(filename):
    events = get_sorted_events(filename)
    guard_records = scan_events(events)
    id_of_laziest = find_laziest_guard(guard_records)
    laziest_minute = guard_records[id_of_laziest].laziest_minute
    return id_of_laziest * laziest_minute


def part_2(filename):
    guard_records = scan_events(get_sorted_events(filename))

    max_slept_at_a_minute = 0
    laziest_guard = None

    for guard_id, record in guard_records.items():
        if record.time_at_laziest_minute > max_slept_at_a_minute:
            laziest_guard = guard_id
            max_slept_at_a_minute = record.time_at_laziest_minute

    return laziest_guard * guard_records[laziest_guard].laziest_minute
