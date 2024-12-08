import re


def parse_time_info(time_str):
    match = re.search(r'(\d+|[一二三四五六七八九十]+)个?([天月年])', time_str)

    if match:
        number = match.group(1)
        unit = match.group(2)

        print(number, unit)

        if number.isdigit():
            number = int(number)
        else:
            chinese_to_arabic = {
                '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
                '六': 6, '七': 7, '八': 8, '九': 9, '十': 10
            }
            number = chinese_to_arabic.get(number, None)

        if unit == '天':
            return number
        elif unit == '月':
            return number * 30
        elif unit == '年':
            return number * 365

    return None


def clean_number_with_chinese(text):
    text = re.sub(r'(\d[\d,]*\.?\d*)', lambda x: x.group(0).replace(',', ''), text)
    cleaned_text = re.sub(r'(\d[\d,]*\.?\d*)([^\d\s]+)', r'\1', text)
    return float(cleaned_text or 0)


def extract_floor_info(floor_string):
    match = re.match(r'([^\(]+)\(共(\d+)层\)', floor_string)

    if match:
        floor_info = match.group(1).strip()  # 括号外的信息
        total_floors = int(match.group(2))  # 总楼层数
        return floor_info, total_floors
    else:
        return None, None


def get_address_detail(address_info):
    address_info_list = [address.strip() for address in address_info.split("|")]
    if len(address_info_list) == 7:
        layout, area, orientation, renovation, floor, year, build_type = address_info_list
    elif len(address_info_list) == 6:
        layout, area, orientation, renovation, floor, build_type = address_info_list
        year = 0
    else:
        layout, area, orientation, renovation, floor, year, build_type = ["", "", "", "", "", "", ""]
    return layout, area, orientation, renovation, floor, year, build_type
