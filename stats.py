import json
from utils import *
from datetime import datetime


def parse_data(history_dir_path):
    with open(history_dir_path + '\\result.json', encoding="utf8") as f:
        history = f.read()
    json_history = json.loads(history)
    return json_history['messages']


def get_character_count_top(parsed_data, top_count=9999):
    message_counts = {}

    for message in parsed_data:
        if message['type'] != 'service' and isinstance(message['text'], str) and message['text'] != '':
            author = message['from']
            if author in message_counts:
                message_counts[author] += len(message['text'])
            else:
                message_counts[author] = len(message['text'])
    sorted_data = dict(sorted(message_counts.items(), key=lambda item: item[1], reverse=True))
    return take_from_dict(sorted_data, top_count)


def get_message_count_top(parsed_data, top_count=conf.REALLY_BIG_NUMBER):
    message_counts = {}

    for message in parsed_data:
        if message['type'] != 'service' and isinstance(message['text'], str) and message['text'] != '':
            author = message['from']
            if author in message_counts:
                message_counts[author] += 1
            else:
                message_counts[author] = 1
    sorted_data = dict(sorted(message_counts.items(), key=lambda item: item[1], reverse=True))
    return take_from_dict(sorted_data, top_count)


def get_average_characters_per_message(parsed_data, top_count=conf.TOP_CHARACTER_PER_MESSAGE, lowest=False):
    top_messages = get_message_count_top(parsed_data)
    top_characters = get_character_count_top(parsed_data, 25)
    for entry in top_characters:
        top_characters[entry] = int(top_characters[entry]/top_messages[entry])
    if not lowest:
        sorted_data = dict(sorted(top_characters.items(), key=lambda item: item[1], reverse=True))
        return take_from_dict(sorted_data, top_count)
    else:
        sorted_data = dict(sorted(top_characters.items(), key=lambda item: item[1], reverse=False))
        return take_from_dict(sorted_data, top_count)


def get_top_weekdays(parsed_data, top_count=conf.TOP_WEEKDAYS_COUNT):
    message_counts = {}

    for message in parsed_data:
        if message['type'] != 'service':
            weekday = datetime.strptime(message['date'], conf.DATE_FULL_FORMAT).strftime(conf.DATE_WEEKDAY_READABLE_FORMAT)
            if weekday in message_counts:
                message_counts[weekday] += 1
            else:
                message_counts[weekday] = 1
    sorted_data = dict(sorted(message_counts.items(), key=lambda item: item[1], reverse=True))
    return take_from_dict(sorted_data, top_count)


def get_message_count_per_date(parsed_data):
    message_counts = {}

    for message in parsed_data:
        if message['type'] != 'service':
            date = datetime.strptime(message['date'], conf.DATE_FULL_FORMAT).strftime(conf.DATE_SHORT_FORMAT)
            if date in message_counts:
                message_counts[date] += 1
            else:
                message_counts[date] = 1
    return message_counts


def get_message_count_per_hour(parsed_data):
    message_counts = {}

    for message in parsed_data:
        if message['type'] != 'service':
            hour = datetime.strptime(message['date'], conf.DATE_FULL_FORMAT).strftime(conf.DATE_HOUR_FORMAT)
            if hour in message_counts:
                message_counts[hour] += 1
            else:
                message_counts[hour] = 1
    return dict(sorted(message_counts.items(), key=lambda item: item[0], reverse=False))


def get_top_day_streak(parsed_data, top_people=conf.TOP_STREAK_PEOPLE_COUNT, top_streaks=conf.TOP_STREAK_STREAKS_COUNT):
    messages = {}
    active_ranges = {}

    for message in parsed_data:
        if message['type'] != 'service':
            author = message['from']
            if author in messages:
                messages[author].append(message)
            else:
                messages[author] = [message]
                active_ranges[author] = {}

    for person in messages:

        person_dates_of_messages = get_message_dates_for_person(messages, person)
        full_date_range = generate_date_range(messages[person][0]['date'], messages[person][-1]['date'])

        current_range_counter = 0
        range_start_date = None
        old_date = None

        for date in full_date_range:
            date_as_string = date.strftime(conf.DATE_SHORT_FORMAT)
            if date_as_string in person_dates_of_messages:
                if range_start_date is None:
                    range_start_date = date_as_string
                current_range_counter += 1
                old_date = date_as_string
            else:
                if range_start_date:
                    active_ranges[person][f'{range_start_date} - {old_date}'] = current_range_counter
                    range_start_date = None
                    current_range_counter = 0
    return find_top_ranges(active_ranges, top_people, top_streaks)