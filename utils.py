from itertools import islice
from datetime import timedelta, datetime
import config as conf


def find_top_ranges(active_ranges, top_people, top_streaks):
    result = {}

    for person, data in active_ranges.items():
        if data:
            sorted_data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))
            result[person] = dict(list(sorted_data.items())[:top_streaks])

    result = dict(sorted(result.items(), key=lambda item: list(item[1].items())[0][1], reverse=True))
    return take_from_dict(result, top_people)


def get_message_dates_for_person(messages, person):
    return [
        datetime.strptime(message['date'], conf.DATE_FULL_FORMAT).strftime(conf.DATE_SHORT_FORMAT)
        for message in messages[person]
    ]


def generate_date_range(start_date, end_date):
    date_earliest = datetime.strptime(start_date, conf.DATE_FULL_FORMAT)
    date_latest = datetime.strptime(end_date, conf.DATE_FULL_FORMAT)
    delta = date_latest - date_earliest
    date_range = [date_earliest + timedelta(days=i) for i in range(delta.days + 1)]
    return date_range


def get_messages_by_person(data):
    messages = {}

    for message in data:
        if message['type'] != 'service':
            author = message['from']
            if author in messages:
                messages[author].append(message)
            else:
                messages[author] = [message]

    return messages


def calculate_activity_date_ranges(data, person):
    person_dates_of_messages = get_message_dates_for_person(data, person)
    full_date_range = generate_date_range(data[person][0]['date'], data[person][-1]['date'])

    result = {}
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
                result[f'{range_start_date} - {old_date}'] = current_range_counter
                range_start_date = None
                current_range_counter = 0

    return result


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