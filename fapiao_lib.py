import os
import itertools

def extract_number(filename):
    base_name = filename.rsplit('.', 1)[0]
    number_part = base_name.split('_')[0]
    try:
        return float(number_part)
    except ValueError:
        print(f"警告: 文件名 {filename} 的开始部分不是数字。")
        return None

def find_combinations(numbers, target):
    closest_sum = 0
    closest_combination = []
    # Iterate over all possible combinations of all sizes
    for r in range(1, len(numbers) + 1):
        for combination in itertools.combinations(numbers, r):
            current_sum = sum(comb[1] for comb in combination)
            if closest_sum < current_sum <= target:
                closest_sum = current_sum
                closest_combination = combination
    return closest_combination

def read_folder(folder_name):
    # List all the .pdf files in the given folder
    files = [f for f in os.listdir(folder_name) if f.endswith('.pdf')]
    # Extract numbers and associate them with their respective filenames
    numbers = [(f, extract_number(f)) for f in files if extract_number(f) is not None]
    return numbers

def format_money_to_chinese_units(value):
    # Convert to string with two decimal places
    value_str = f"{value:.2f}"
    # Remove the decimal point
    value_str = value_str.replace('.', '')
    # Remove leading zeros and ensure at least one zero if value is zero
    value_str = value_str.lstrip('0') or '0'
    # Right-align the number with the units, considering the width of Chinese characters
    # Each Chinese character is approximately as wide as two digits or spaces
    formatted_value = value_str
    # Add spaces to match Chinese characters width
    space_adjustment = ' '*4  # three spaces by default
    formatted_value_with_spaces = ''
    for i, char in enumerate(formatted_value):
        if i == len(formatted_value) - 4:  # Adjust spacing for 百 (hundreds) position
            space_adjustment = ' '*3  # four spaces for hundreds
        formatted_value_with_spaces += char + space_adjustment
        space_adjustment = ' '*4

    # Adjust the overall alignment
    formatted_value_with_spaces = formatted_value_with_spaces.strip().rjust(32, ' ')
    return formatted_value_with_spaces

def print_money_table(dining_sum, transport_sum):
    # Print table headers
    print("摘要      万   千   百   十   元   角   分")
    # Format and print the sums for 餐费 and 交通费
    print(f"餐费    {format_money_to_chinese_units(dining_sum)}")
    print(f"交通    {format_money_to_chinese_units(transport_sum)}")
    # Separator line, adjusting length as needed
    print("-" * 40)
    # Calculate and print the total
    total_sum = dining_sum + transport_sum
    print(f"总计   ¥{format_money_to_chinese_units(total_sum)}")

def number_to_capitalized_cn(num):
    # Capitalized Chinese number mappings
    num_map = {
        '0': '零', '1': '壹', '2': '贰', '3': '叁',
        '4': '肆', '5': '伍', '6': '陆', '7': '柒',
        '8': '捌', '9': '玖'
    }
    unit_map = {
        0: '角', 1: '分', 2: '元',
        3: '拾', 4: '佰', 5: '仟', 6: '万'
    }

    # Convert to string with two decimal places
    str_num = f"{num:,.2f}"
    str_num = str_num.replace(",", "")  # Remove comma

    # Split into whole and decimal part
    whole_part, decimal_part = str_num.split(".")

    # Reverse the whole part to map to Chinese units correctly
    whole_part = whole_part[::-1]

    # Map numbers to capitalized Chinese characters with units for whole part
    cn_num = ""
    for i, digit in enumerate(whole_part):
        if digit != '0' or (i > 0 and whole_part[i-1] != '0'):
            cn_num = num_map[digit] + (unit_map[i+2] if i+2 in unit_map else '') + cn_num
    
    # Process the decimal part
    decimal_cn_num = ""
    for i, digit in enumerate(decimal_part):
        if digit != '0':
            decimal_cn_num += num_map[digit] + unit_map[i]

    # Combine whole part with decimal part
    cn_num += decimal_cn_num
    
    if cn_num[-1] != '分':
        cn_num += '整'
    return cn_num.strip()