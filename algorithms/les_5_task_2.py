"""
2. Написать программу сложения и умножения двух шестнадцатеричных чисел.
При этом каждое число представляется как массив, элементы которого — цифры числа.
Например, пользователь ввёл A2 и C4F.
Нужно сохранить их как [‘A’, ‘2’] и [‘C’, ‘4’, ‘F’] соответственно.
Сумма чисел из примера: [‘C’, ‘F’, ‘1’], произведение - [‘7’, ‘C’, ‘9’, ‘F’, ‘E’].
"""
from collections import deque
from itertools import dropwhile
from functools import reduce, partial
import random


numbase16 = ('0', '1', '2', '3', '4', '5', '6', '7',
             '8', '9', 'A', 'B', 'C', 'D', 'E', 'F')


def add_digits(dx, dy, numbase):
    result_right = deque(numbase, maxlen=len(numbase))
    result_left = deque(numbase[0] * len(numbase), maxlen=len(numbase))
    if dx != numbase[0]:
        for digit in numbase[1:]:
            result_right.rotate(-1)
            result_left.append(numbase[1])
            if dx == digit:
                break
    for digit, left, right in zip(numbase, result_left, result_right):
        if dy == digit:
            return left, right


def remove_leading_zeros(digits, numbase):
    return list(dropwhile(lambda x: x == numbase[0], digits))


def add(x, y, numbase):
    xdeque = deque(x)
    ydeque = deque(y)
    result = deque()
    from_right = numbase[0]
    if len(ydeque) > len(xdeque):
        xdeque, ydeque = ydeque, xdeque
    xdeque.appendleft(numbase[0])
    while ydeque:
        xdigit = xdeque.pop()
        ydigit = ydeque.pop()
        left1, right = add_digits(xdigit, ydigit, numbase=numbase)
        left2, right = add_digits(right, from_right, numbase=numbase)
        from_right = left1 if left2 == numbase[0] else left2
        result.appendleft(right)
    while xdeque:
        xdigit = xdeque.pop()
        from_right, right = add_digits(xdigit, from_right, numbase=numbase)
        result.appendleft(right)

    return remove_leading_zeros(result, numbase)


def mul_digits(dx, dy, numbase):
    if dx == numbase[0] or dy == numbase[0]:
        return numbase[0], numbase[0]
    left = numbase[0]
    right = numbase[0]
    for digit in numbase[1:]:
        _sum = add([left, right], [numbase[0], dy], numbase=numbase)
        left, right = [numbase[0], *_sum][-2:]
        if dx == digit:
            break
    return left, right


def mul(x, y, numbase):
    if x == [numbase[0]] or y == [numbase[0]]:
        return [numbase[0]]
    if x == [numbase[1]]:
        return y
    if y == [numbase[1]]:
        return x
    xdeque = deque(x)
    ydeque = deque(y)
    if len(ydeque) > len(xdeque):
        xdeque, ydeque = ydeque, xdeque
    terms = deque()
    ypadding = deque()
    while ydeque:
        xpadding = deque()
        ydigit = ydeque.pop()
        xcopy = xdeque.copy()
        while xcopy:
            xdigit = xcopy.pop()
            term = deque(mul_digits(xdigit, ydigit, numbase=numbase))
            term.extend(xpadding)
            term.extend(ypadding)
            terms.append(term)
            xpadding.append(numbase[0])
        ypadding.append(numbase[0])
    add_base = partial(add, numbase=numbase)
    return reduce(add_base, terms)


# Testing
num_1 = ['0', '0', 'A', '2']
num_2 = ['0', 'C', '4', 'F']
print(add(num_1, num_2, numbase=numbase16))
print(mul(num_1, num_2, numbase=numbase16))
assert add(num_1, num_2, numbase=numbase16) == ['C', 'F', '1']
assert mul(num_1, num_2, numbase=numbase16) == ['7', 'C', '9', 'F', 'E']

for _ in range(100):
    a = random.randint(0, 16**4)
    b = random.randint(0, 16**10)
    a_b = a + b
    hex_a, hex_b, hex_ab = map(lambda x: hex(x).upper()[2:], (a, b, a_b))
    operation_ab = ''.join(add(hex_a, hex_b, numbase=numbase16))
    assert hex_ab == operation_ab
    a_b = a * b
    hex_a, hex_b, hex_ab = map(lambda x: hex(x).upper()[2:], (a, b, a_b))
    operation_ab = ''.join(mul(hex_a, hex_b, numbase=numbase16))
    assert hex_ab == operation_ab
