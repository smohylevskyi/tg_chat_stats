from stats import *
import sys

if __name__ == '__main__':
    parsed_data = parse_data(sys.argv[1])

    print_dict('= TOP MESSAGE COUNT BY AUTHOR =', get_message_count_top(parsed_data, conf.TOP_MESSAGE_COUNT))
    print_dict('= TOP SYMBOLS BY AUTHOR =', get_character_count_top(parsed_data, conf.TOP_CHARACTER_COUNT))
    print_dict('= TOP SYMBOLS PER MESSAGE =', get_average_characters_per_message(parsed_data, lowest=False))
    print_dict('= LOWEST SYMBOLS PER MESSAGE =', get_average_characters_per_message(parsed_data, lowest=True))
    print_dict('= MOST ACTIVE DAY BY AVERAGE MESSAGES =', get_top_weekdays(parsed_data))
    print_dict('= MESSAGES PER DATE =', get_message_count_per_date(parsed_data), excel_friendly=True)
    print_dict('= MESSAGES PER HOUR =', get_message_count_per_hour(parsed_data), excel_friendly=True)
    print_dict('= TOP DAY STREAK =', get_top_day_streak(parsed_data))