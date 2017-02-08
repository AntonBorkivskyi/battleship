import random


def generate_field():
    """
    () -> list()

    Generate field.
    Randomly choose starting coordinates.
    Then building ship.

    >>> generate_field()
       **   *

    * **   *
    *
    * **   *
    *      * *
        *
    ***

        *
    """
    board = [[" " for i in range(10)] for i in range(10)]
    for i in range(4, 0, -1):
        for j in range(5-i):
            while True:
                x, y = random.randint(0, 10 - i), random.randint(0, 10 - i)
                px = random.randint(0, 1)
                if checkfree(x, y, i, px, board):
                    break
            py = 1 - px
            for k in range(-1, 1 + i):
                try:
                    if (k == -1 or k == i):
                        if (py == 0 and x == 0 and k == -1)\
                                or (px == 0 and y == 0 and k == -1):
                            continue
                        board[y+k*py][x + k*px] = "-"
                    else:
                        board[y+k*py][x + k*px] = "*"
                    if px == 0:
                        if y == 0 and k == -1:
                            continue
                        if x != 0:
                            board[y+k*py][x-1+k*px] = "-"
                        board[y+k*py][x+1+k*px] = "-"
                    elif py == 0:
                        if x == 0 and k == -1:
                            continue
                        if y != 0:
                            board[y-1+k*py][x+k*px] = "-"
                        board[y+1+k*py][x+k*px] = "-"
                except IndexError:
                    continue
    return [print(''.join(line).replace('-', ' ')) for line in board]


def checkfree(x, y, n, px, b):
    """
    (int, int, int, int, list) -> bool

    Check if the area of potential ship and the area close to it is free.

    >>> checkfree(0, 0, 1, 0, [""])
    True
    >>> checkfree(7, 3, 2, 1, [""])
    False
    """
    py, iter = 1 - px, 0
    try:
        for i in range(n):
            if b[y + i * py][x + i * px] == " ":
                iter += 1
        return iter == n
    except IndexError:
        pass


def read_field(file):
    """
    (str) -> list(str)

    Reads the file and write it.

    >>> read_field("field.txt")
    ['  * *     ', '          ', '    ***  *',
    ' **      *', '    ***   ', '        * ',
    ' ****   * ', '          ', '   *      ', '         *']
    """
    with open(file) as fil:
        return [line[0:len(line) - 1] for line in fil]


def has_ship(data, tupl):
    """
    (list, tuple) -> bool

    Check if the ship is located in coordinates.

    >>> has_ship([""], ("E", 5))
    False
    >>> has_ship([""], ("B", 3))
    False
    """
    return data[tupl[1] - 1][ord(tupl[0]) - 65] != " "


def field_to_str(data):
    """
    (list) -> str

    Write the field into str-type.

    >>> field_to_str(["*** *", "    *"])
    "*** *\n    *"
    """
    return "\n".join(data)


def ship_size(data, tupl):
    """
    (list, tuple) -> int

    Return the length of the ship, which part is in coordinates.

    >>> ship_size(["*** *", "    *"],("A", 1))
    3
    """
    x, y = ord(tupl[0]) - 65, tupl[1] - 1
    if data[y][x] != "*":
        return 0
    pos, size = [[0, 1], [0, -1], [-1, 0], [1, 0]], 1
    for i in range(1, 4):
        bp = []
        for p in range(len(pos)):
            if y + pos[p][1] * i >= 0 and x + pos[p][0] * i >= 0\
                    and y + pos[p][1] * i < 10 and x + pos[p][0] * i < 10\
                    and data[y + pos[p][1] * i][x + pos[p][0] * i] == "*":
                size += 1
            else:
                bp.append(pos[p])
        for e in bp:
            pos.remove(e)
    return size


def is_valid(data):
    """
    (list) -> bool

    Check if the board is correct.

    >>> is_valid(['  * *     ', '          ', '    ***  *',\
    ' **      *', '    ***   ', '        * ', ' ****   * ',\
    '          ', '   *      ', '         *'])
    True
    """
    et = [10] * 10
    net = []
    for x in range(len(data)):
        net.append(0)
        for y in range(len(data[x])):
            net[x] += 1
    if net == et:
        pass
    else:
        return False

    l, a = 0, []
    e = [1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4]
    for i in range(10):
        for j in range(10):
            a.append(ship_size(data, (chr(j+65), i+1)))
    return sorted(a)[-20:] == e


# generate_field()
# for i in read_field("field.txt"):
#     print(i)
# print(read_field("field.txt"))
# print(field_to_str(read_field("field.txt")))
# print(is_valid(read_field("field.txt")))
