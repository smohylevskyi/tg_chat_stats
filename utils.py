from itertools import islice
from datetime import timedelta, datetime
import config as conf


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
            datetime.strptime(message['date'], conf.DATE_FULL_FORMAT).strftime(conf.DATE_SHORT_FORMAT))
    return person_dates_of_messages


def generate_date_range(start_date, end_date):
    date_earliest = datetime.strptime(start_date, conf.DATE_FULL_FORMAT)
    date_latest = datetime.strptime(end_date, conf.DATE_FULL_FORMAT)
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