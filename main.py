import json
from itertools import islice
from datetime import timedelta, datetime

DATE_FULL_FORMAT = '%Y-%m-%dT%H:%M:%S'
DATE_SHORT_FORMAT = '%Y-%m-%d'
DATE_WEEKDAY_READABLE_FORMAT = '%A'
DATE_HOUR_FORMAT = '%H'

TOP_MESSAGE_COUNT = 5
TOP_CHARACTER_COUNT = 5
TOP_CHARACTER_PER_MESSAGE = 5
TOP_WEEKDAYS_COUNT = 7
TOP_STREAK_PEOPLE_COUNT = 5
TOP_STREAK_STREAKS_COUNT = 3
REALLY_BIG_NUMBER = 100000


def parse_data(history_dir_path):
    with open(history_dir_path + '\\result.json', encoding="utf8") as f:
        history = f.read()
    json_history = json.loads(history)
    return json_history['messages']


def get_character_count_top(parsed_data, top_count=REALLY_BIG_NUMBER):
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


def get_message_count_top(parsed_data, top_count=REALLY_BIG_NUMBER):
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


def get_average_characters_per_message(parsed_data, top_count=TOP_CHARACTER_PER_MESSAGE, lowest=False):
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


def get_top_weekdays(parsed_data, top_count=TOP_WEEKDAYS_COUNT):
    message_counts = {}

    for message in parsed_data:
        if message['type'] != 'service':
            weekday = datetime.strptime(message['date'], DATE_FULL_FORMAT).strftime(DATE_WEEKDAY_READABLE_FORMAT)
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
            date = datetime.strptime(message['date'], DATE_FULL_FORMAT).strftime(DATE_SHORT_FORMAT)
            if date in message_counts:
                message_counts[date] += 1
            else:
                message_counts[date] = 1
    return message_counts


def get_message_count_per_hour(parsed_data):
    message_counts = {}

    for message in parsed_data:
        if message['type'] != 'service':
            hour = datetime.strptime(message['date'], DATE_FULL_FORMAT).strftime(DATE_HOUR_FORMAT)
            if hour in message_counts:
                message_counts[hour] += 1
            else:
                message_counts[hour] = 1
    return dict(sorted(message_counts.items(), key=lambda item: item[0], reverse=False))


def get_top_day_streak(parsed_data, top_people=TOP_STREAK_PEOPLE_COUNT, top_streaks=TOP_STREAK_STREAKS_COUNT):
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
            date_as_string = date.strftime(DATE_SHORT_FORMAT)
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


def find_top_ranges(active_ranges, top_people, top_streaks):
    result = {}
    for person in active_ranges:
        if active_ranges[person] != {}:
            sorted_data = dict(sorted(active_ranges[person].items(), key=lambda item: item[1], reverse=True))
            result[person] = take_from_dict(sorted_data, top_streaks)
    result = dict(sorted(result.items(), key=lambda item: list(item[1].items())[0][1], reverse=True))
    result = take_from_dict(result, top_people)
    return result


def get_message_dates_for_person(messages, person):
    person_dates_of_messages = []
    for message in messages[person]:
        person_dates_of_messages.append(
            datetime.strptime(message['date'], DATE_FULL_FORMAT).strftime(DATE_SHORT_FORMAT))
    return person_dates_of_messages


def generate_date_range(start_date, end_date):
    date_earliest = datetime.strptime(start_date, DATE_FULL_FORMAT)
    date_latest = datetime.strptime(end_date, DATE_FULL_FORMAT)
    delta = date_latest - date_earliest
    date_range = []
    for i in range(delta.days + 1):
        date_range.append(date_earliest + timedelta(days=i))

    return date_range


def take_from_dict(d, entry_count):
    return dict(islice(d.items(), entry_count))


def print_dict(name, d, excel_friendly=False):
    if excel_friendly:
        separator = '\t'
    else:
        separator = ': '
    print(name)
    for entry in d:
        print(f'{entry}{separator}{d[entry]}')
    print('_______________________\n')


if __name__ == '__main__':
    dir_path = 'C:\\Users\\Worker\\Desktop\\ChatExport_2023-10-24 - Copy'
    parsed_data = parse_data(dir_path)
    print_dict('= TOP MESSAGE COUNT BY AUTHOR =', get_message_count_top(parsed_data, TOP_MESSAGE_COUNT))
    print_dict('= TOP SYMBOLS BY AUTHOR =', get_character_count_top(parsed_data, TOP_CHARACTER_COUNT))
    print_dict('= TOP SYMBOLS PER MESSAGE =', get_average_characters_per_message(parsed_data, lowest=False))
    print_dict('= LOWEST SYMBOLS PER MESSAGE =', get_average_characters_per_message(parsed_data, lowest=True))
    print_dict('= MOST ACTIVE DAY BY AVERAGE MESSAGES =', get_top_weekdays(parsed_data))
    print_dict('= MESSAGES PER DATE =', get_message_count_per_date(parsed_data), excel_friendly=True)
    print_dict('= MESSAGES PER HOUR =', get_message_count_per_hour(parsed_data), excel_friendly=True)
    print_dict('= TOP DAY STREAK =', get_top_day_streak(parsed_data))