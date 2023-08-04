import random


def create_ladder(num_rows, win_number):
    if num_rows <= 0 or not isinstance(num_rows, int):
        raise ValueError("Number of rows must be a positive integer.")
    if win_number <= 0 or win_number > num_rows or not isinstance(win_number, int):
        raise ValueError("Winning position must be within the range of the number of rows.")
    
    # Initialize top and bottom rungs
    top_rung = [str(i + 1) for i in range(num_rows)]#[chr(97 + i) for i in range(num_rows)]
    bottom_rung = ['0' if i+1 != win_number else '1' for i in range(num_rows)]

    # Initialize an empty grid for the ladder
    ladder = [[' ' for _ in range(num_rows-1)] for _ in range(num_rows)]

    # Randomly place the switches
    for row in ladder:
        i = 0
        while i < num_rows-1:
            if random.random() < 0.5:  # 50% chance to place a switch
                row[i] = '-'
                i += 2  # Skip the next position to avoid adjacent switches
            else:
                i += 1

    # Combine the top rung, ladder rows, and bottom rung into a single string
    ladder_str = '  '.join(top_rung) + '\n'  # First row
    for row in ladder:
        ladder_str += '|' + '|'.join(row) + '|\n'  # Ladder rows
    ladder_str += ' '.join(bottom_rung)  # Last row

    return ladder_str


def evaluate_ladder(ladder_str):
    data = ladder_str.split("\n")
    top_rung = data[0].split()
    bottom_rung = data[-1].split()

    for line in data[1:-1]:
        switches = line.split('|')
        for i, sw in enumerate(switches):
            if sw == '-':
                bottom_rung[i-1], bottom_rung[i] = bottom_rung[i], bottom_rung[i-1]

    result = {d1: '당첨' if d2 == '1' else '꽝' for d1, d2 in zip(top_rung, bottom_rung)}
    return result

def make_ladder_text(num_rows, win_number):
    ladder_graphic = create_ladder(num_rows, win_number)
    ladder_result = evaluate_ladder(ladder_graphic)
    ladder_text = str(ladder_graphic) + "\n\n" + str(ladder_result)
    return ladder_text
"""
# Test the function
num_rows = 6
win_number = 2

try:
    ladder_str = create_ladder(num_rows, win_number)
    print(ladder_str)
    result = evaluate_ladder(ladder_str)
    print(result)
except ValueError as e:
    print(e)
"""
