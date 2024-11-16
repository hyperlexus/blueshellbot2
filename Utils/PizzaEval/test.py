# all hail test.py
# from datetime import datetime
#
# def helper_calcdifftime(end_str: str) -> str:
#     return f"{int(int((datetime.strptime(end_str, '%Y-%m-%dZ%H:%M:%S') - datetime.now()).total_seconds()) // (24 * 3600)):02d}d {int((int((datetime.strptime(end_str, '%Y-%m-%dZ%H:%M:%S') - datetime.now()).total_seconds()) % (24 * 3600)) // 3600):02d}h {int((int((datetime.strptime(end_str, '%Y-%m-%dZ%H:%M:%S') - datetime.now()).total_seconds()) % 3600) // 60):02d}m"
#
# print(helper_calcdifftime('2024-11-18Z19:10:00'))


# def is_allowed_complex_input(read_string: str) -> int | bool:
#     """Checks if string is allowed input for pizza type 'complex'"""
#     print(1, read_string)
#     print(2, all(i not in read_string for i in ['is ', 'in ', 'start ', 'end ']))
#     if all(i not in read_string for i in ['is ', 'in ', 'start ', 'end ']):
#         return 1
#     if all(i not in read_string for i in ['|', '&']):
#         return 2
#     return True
#
# print(is_allowed_complex_input('a'))
#
# print(1 != True)

# a = "start b | in c"
# print(a.split(' | '))

# def fella(type, b, a):
#     if type == 'a':
#         return a.startswith(b)
#     if type == 'b':
#         return a.endswith(b)
#     if type == 'c':
#         return a == b
#     if type == 'd':
#         return b in a
#
# print(fella('a', 'nig', 'fella'))
# print(fella('b', 'nig', 'fella'))
# print(fella('c', 'nig', 'nig'))
# print(fella('d', 'nig', 'fella'))

# print(True ^ True)

import re

# Input string
input_string = "is a | is 'b | is c' | is 'd & is e'"

# Regular expression to match quoted strings
pattern = r"'[^']*'"

# Find all quoted segments
result = [match for match in re.findall(pattern, input_string)]

print(result)

