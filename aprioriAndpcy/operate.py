with open('result.txt', 'r') as file:
    lines = file.readlines()

unique_lines = set(lines)

with open('new_result.txt', 'w') as new_file:
    new_file.write(''.join(unique_lines))
