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