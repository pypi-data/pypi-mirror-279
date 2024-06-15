#Partition

def can_partition(nums):
    total_sum = sum(nums)
    if total_sum % 2 != 0:
        return False

    target_sum = total_sum // 2
    return subset_sum(nums, target_sum, 0)

def subset_sum(nums, target_sum, current_sum, index=0):
    if current_sum == target_sum:
        return True

    if current_sum > target_sum or index >= len(nums):
        return False

    if subset_sum(nums, target_sum, current_sum + nums[index], index + 1):
        return True

    return subset_sum(nums, target_sum, current_sum, index + 1)

# Example usage:
nums = [1, 5, 11, 5]

result = can_partition(nums)

if result:
    print("Set can be partitioned")
else:
    print("Set cannot be partitioned")
