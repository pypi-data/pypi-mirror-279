#3-Partition


def can_3_partition(nums):
    total_sum = sum(nums)
    subset_sum = total_sum // 3

    if total_sum % 3 != 0 or len(nums) < 3:
        return False

    nums.sort(reverse=True)
    used = [False] * len(nums)

    return partition(nums, used, 0, subset_sum, 0)

def partition(nums, used, current_sum, subset_sum, count):
    if count == 3:
        return True

    if current_sum == subset_sum:
        return partition(nums, used, 0, subset_sum, count + 1)

    for i in range(len(nums)):
        if not used[i] and current_sum + nums[i] <= subset_sum:
            used[i] = True

            if partition(nums, used, current_sum + nums[i], subset_sum, count):
                return True

            used[i] = False

    return False

# Example usage:
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

result = can_3_partition(nums)

if result:
    print("The set can be 3-partitioned")
else:
    print("The set cannot be 3-partitioned")
