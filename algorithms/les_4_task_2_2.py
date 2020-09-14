from itertools import islice


def odd():
    """Infinite generator of odd numbers"""
    num = 0
    while True:
        yield num * (num & 1)
        num += 1


def sieve(i):
    if i < 2:
        return None
    if i == 2:
        return 2
    primes = [2]
    array_size = 1000
    array_start = 0
    g = odd()
    array = list(islice(g, array_size))
    array[1] = 0
    idx = 3
    while idx < array_size:
        p = array[idx]
        if p:
            primes.append(p)
            if len(primes) == i:
                break
            j = idx ** 2
            for j in array[p ** 2::p]:
                array[j] = 0
        idx += 1
    while len(primes) < i:
        array_start += array_size
        array = list(islice(g, array_size))
        for p in primes:
            idxrange = (idx - array_start
                        for idx in range(0, array_start + array_size, p)
                        if idx >= array_start)
            for j in idxrange:
                array[j] = 0
        for el in array:
            if el:
                primes.append(el)
                if len(primes) == i:
                    break
    return primes[-1]

print(sieve(1000))

