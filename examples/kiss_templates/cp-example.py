import sys

sys.setrecursionlimit(200000)


def _input_stream():
    for line in sys.stdin:
        for token in line.split():
            yield token


_stream = _input_stream()


def rs():
    return next(_stream)


def ri():
    return int(next(_stream))


def rli(n=None):
    if n is None:
        return list(map(int, sys.stdin.readline().split()))
    return [int(next(_stream)) for _ in range(n)]


def pr(*args, sep=" ", end="\n"):
    sys.stdout.write(sep.join(map(str, args)) + end)


def solve():
    pass


if __name__ == "__main__":
    solve()
