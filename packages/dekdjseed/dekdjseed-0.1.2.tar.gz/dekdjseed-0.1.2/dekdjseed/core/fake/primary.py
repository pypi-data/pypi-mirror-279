import string

string_queue = string.digits + string.ascii_letters
string_length = len(string_queue)

cursor_int = 0
cursor_str = [0]


def get_int():
    global cursor_int
    cursor_int += 1
    return cursor_int


def get_str():
    global cursor_str

    cursor = 0
    while cursor <= len(cursor_str) - 1:
        cursor_str[cursor] += 1
        if cursor_str[cursor] >= string_length:
            cursor_str[cursor] = 0
            cursor += 1
        else:
            break
    if cursor > len(cursor_str) - 1:
        cursor_str.append(0)

    return ''.join([string_queue[x] for x in cursor_str])
