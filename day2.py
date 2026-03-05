def safe_report(nums):
    if len(nums) < 2:
        return True
    diffs = [nums[i + 1] - nums[i] for i in range(len(nums) - 1)]
    if all(d == 0 for d in diffs):
        return False
    direction = 1 if diffs[0] > 0 else -1
    for d in diffs:
        if d * direction <= 0:
            return False
        if abs(d) > 3 or abs(d) < 1:
            return False
    return True

with open("input.txt") as f:
    reports = [[int(x) for x in line.split()] for line in f]
print(sum(1 for r in reports if safe_report(r)))
