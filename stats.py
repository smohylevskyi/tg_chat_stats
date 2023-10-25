import json
from utils import *
from datetime import datetime
from collections import OrderedDict


def parse_data(history_file_path):
    with open(history_file_path, encoding="utf8") as f:
        return json.loads(f.read())['messages']


def get_character_count_top(parsed_data, top_count=9999):
    message_counts = {}

    for message in parsed_data:
        if message['type'] != 'service' and isinstance(message['text'], str) and message['text']:
            author = message['from']
            message_counts[author] = message_counts.get(author, 0) + len(message['text'])

    sorted_data = dict(sorted(message_counts.items(), key=lambda item: item[1], reverse=True))
    return take_from_dict(sorted_data, top_count)


def get_message_count_top(parsed_data, top_count=conf.REALLY_BIG_NUMBER):
    message_counts = {}

    for message in parsed_data:
        if message['type'] != 'service' and isinstance(message['text'], str) and message['text']:
            author = message['from']
            message_counts[author] = message_counts.get(author, 0) + 1

    sorted_data = dict(sorted(message_counts.items(), key=lambda item: item[1], reverse=True))
    return take_from_dict(sorted_data, top_count)


def get_average_characters_per_message(parsed_data, top_count=conf.TOP_CHARACTER_PER_MESSAGE, lowest=False):
    top_messages = get_message_count_top(parsed_data)
    top_characters = get_character_count_top(parsed_data, 25)

    for entry, count in top_characters.items():
        top_characters[entry] = int(count / top_messages.get(entry, 1))

    sorted_data = dict(sorted(top_characters.items(), key=lambda item: item[1], reverse=not lowest))
    return take_from_dict(sorted_data, top_count)


def get_top_weekdays(parsed_data, top_count=conf.TOP_WEEKDAYS_COUNT):
    message_counts = {}

    for message in parsed_data:
        if message['type'] != 'service':
            weekday = datetime.strptime(message['date'], conf.DATE_FULL_FORMAT).strftime(conf.DATE_WEEKDAY_READABLE_FORMAT)
            message_counts[weekday] = message_counts.get(weekday, 0) + 1

    sorted_data = dict(sorted(message_counts.items(), key=lambda item: item[1], reverse=True))
    return take_from_dict(sorted_data, top_count)


def get_message_count_per_date(parsed_data):
    message_counts = {}

    for message in parsed_data:
        if message['type'] != 'service':
            date = datetime.strptime(message['date'], conf.DATE_FULL_FORMAT).strftime(conf.DATE_SHORT_FORMAT)
            message_counts[date] = message_counts.get(date, 0) + 1

    return message_counts


def get_message_count_per_hour(parsed_data):
    message_counts = {}

    for message in parsed_data:
        if message['type'] != 'service':
            hour = datetime.strptime(message['date'], conf.DATE_FULL_FORMAT).strftime(conf.DATE_HOUR_FORMAT)
            message_counts[hour] = message_counts.get(hour, 0) + 1

    sorted_dict = OrderedDict(sorted(message_counts.items()))
    sorted_dict.move_to_end('00', last=True)

    return sorted_dict


def get_top_day_streak(parsed_data, top_people=conf.TOP_STREAK_PEOPLE_COUNT, top_streaks=conf.TOP_STREAK_STREAKS_COUNT):
    messages = get_messages_by_person(parsed_data)
    active_ranges = {}

    for person in messages:
        active_ranges[person] = calculate_activity_date_ranges(messages, person)
    return find_top_ranges(active_ranges, top_people, top_streaks)