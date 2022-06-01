_OPEN = 'O'
_CLOSED = 'X'


# Takes in a drawing in the form of a list of strings
# Outputs the test case in the input format we defined
def drawing_to_input(drawing):
    height = len(drawing)
    width = len(drawing[0])
    blocked = []

    for y, line in enumerate(drawing):
        for x, character in enumerate(line):
            if character == _CLOSED:
                blocked.append((y + 1, x + 1))

    return height, width, blocked
