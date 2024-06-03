from datetime import datetime
from time import perf_counter


def measure_time(func: callable):
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        print(f'The function was working: {perf_counter() - start} seconds.')
        return result
    return wrapper


def convert_datetime(datetime_str: str) -> datetime:
    # format example: 18 августа 2022 г. 7:58:28.012 мсек
    datetime_list = datetime_str.split(' ')
    day, month, year = datetime_list[0], datetime_list[1], datetime_list[2]
    month = get_month_number(month)

    time_list = datetime_list[4].split(':')
    hour, minute, second = time_list[0], time_list[1], time_list[2]
    second = int(round(float(second)))

    format = '%d%m%Y %H%M%S'
    return datetime.strptime(f'{day}{month}{year} {hour}{minute}{second}', format)


def get_month_number(month: str) -> int:
    months_dict = {
        'января': 1,
        'февраля': 2,
        'марта': 3,
        'апреля': 4,
        'мая': 5,
        'июня': 6,
        'июля': 7,
        'августа': 8,
        'сентября': 9,
        'октября': 10,
        'ноября': 11,
        'декабря': 12,
    }
    return months_dict.get(month, 8)


def compare_parameters(params: tuple, amplitude: int) -> bool:
    for index in range(1, len(params)):
        current_value = float(params[index].replace(',', '.'))
        previous_value = float(params[index - 1].replace(',', '.'))
        difference = current_value - previous_value
        if difference > amplitude:
            return True
    return False


def is_current_line_suitable(current_line: str, start: datetime, finish: datetime, amplitude: int) -> bool:
    recorded_datetime = current_line.split(';')[1]
    converted_datetime = convert_datetime(recorded_datetime)
    if start <= converted_datetime <= finish:
        params = tuple(current_line.split(';')[2:])
        if compare_parameters(params=params, amplitude=amplitude):
            return True
    return False


def get_suitable_table_lines(file: str, start: datetime, finish: datetime, amplitude: int) -> list[str]:
    with open(file, 'r', encoding='Windows-1251') as csv_file:
        counter = 0
        suitable_lines = []
        for line in csv_file:
            if counter == 0:
                suitable_lines.append(line)
                counter += 1
                continue
            if is_current_line_suitable(current_line=line, start=start, finish=finish, amplitude=amplitude):
                suitable_lines.append(line)

        return suitable_lines


@measure_time
def main(file: str, start: datetime, finish: datetime, amplitude: int) -> None:
    suitable_lines = get_suitable_table_lines(
        file=file,
        start=start,
        finish=finish,
        amplitude=amplitude,
    )
    with open('new_table.csv', 'w', encoding='Windows-1251') as csv_file:
        for line in suitable_lines:
            csv_file.write(line)


if __name__ == '__main__':
    file_name = 'table.csv'
    start_time = datetime(year=2022, month=8, day=18, hour=10, minute=47, second=40)
    finish_time = datetime(year=2022, month=8, day=18, hour=10, minute=53, second=45)
    amplitude_value = 1_000_000
    main(file=file_name, start=start_time, finish=finish_time, amplitude=amplitude_value)
