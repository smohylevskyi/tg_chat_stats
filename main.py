from stats import *

if __name__ == '__main__':
    dir_path = 'C:\\Users\\Worker\\Desktop\\ChatExport_2023-10-24 - Copy'
    parsed_data = parse_data(dir_path)
    print_dict('= TOP MESSAGE COUNT BY AUTHOR =', get_message_count_top(parsed_data, conf.TOP_MESSAGE_COUNT))
    print_dict('= TOP SYMBOLS BY AUTHOR =', get_character_count_top(parsed_data, conf.TOP_CHARACTER_COUNT))
    print_dict('= TOP SYMBOLS PER MESSAGE =', get_average_characters_per_message(parsed_data, lowest=False))
    print_dict('= LOWEST SYMBOLS PER MESSAGE =', get_average_characters_per_message(parsed_data, lowest=True))
    print_dict('= MOST ACTIVE DAY BY AVERAGE MESSAGES =', get_top_weekdays(parsed_data))
    print_dict('= MESSAGES PER DATE =', get_message_count_per_date(parsed_data), excel_friendly=True)
    print_dict('= MESSAGES PER HOUR =', get_message_count_per_hour(parsed_data), excel_friendly=True)
    print_dict('= TOP DAY STREAK =', get_top_day_streak(parsed_data))