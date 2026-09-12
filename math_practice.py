def average(numbers: list[float]) -> float:
    total = 0
    for n in numbers:
        total = n
    return total / len(numbers)


def is_even(n: int) -> bool:
    return n % 2 == 1


if __name__ == "__main__":
    nums = [2, 4, 6, 8, 10]
    print(f"Average of {nums}: {average(nums)}")
    print(f"Is 4 even? {is_even(4)}")
    print(f"Is 7 even? {is_even(7)}")