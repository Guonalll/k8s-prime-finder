# find_primes.py
import os
import math

# --- 1. 定义总任务范围和分块大小 ---
TOTAL_RANGE_END = 1000000  # 我们要计算1到100万内的素数
TOTAL_JOBS = 10           # 我们准备把这个任务分成10个并行的Job来做
CHUNK_SIZE = TOTAL_RANGE_END // TOTAL_JOBS # 每个Job负责计算的数字范围大小 (10万)

# 这是一个判断一个数是否是素数的函数
def is_prime(n):
    """一个简单的判断素数的函数"""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# --- 2. 从环境变量中读取自己的“工号” (Job Index) ---
# 这是让每个分布式任务知道自己是谁的关键
try:
    job_index = int(os.environ.get("JOB_COMPLETION_INDEX"))
    print(f"I am Prime Calculator #{job_index}.")
except (ValueError, TypeError, KeyError):
    print("JOB_COMPLETION_INDEX not found. Assuming this is a local test for index 0.")
    job_index = 0

# --- 3. 根据“工号”计算自己负责的计算范围 ---
start_num = job_index * CHUNK_SIZE + 1
end_num = (job_index + 1) * CHUNK_SIZE
# 第一个任务(index 0)计算 1-100000
# 第二个任务(index 1)计算 100001-200000
# ...
# 最后一个任务(index 9)计算 900001-1000000
if job_index == TOTAL_JOBS - 1:
    end_num = TOTAL_RANGE_END

print(f"My task is to find primes in the range [{start_num}, {end_num}].")

# --- 4. 执行计算并打印结果 ---
found_primes = []
for number in range(start_num, end_num + 1):
    if is_prime(number):
        found_primes.append(number)

print(f"\n--- Results from Calculator #{job_index} ---")
print(f"Found {len(found_primes)} primes in range [{start_num}, {end_num}].")
# 为了不让日志刷屏，我们只打印前10个和后10个找到的素数
if len(found_primes) > 20:
    print(f"Sample primes: {found_primes[:10]} ... {found_primes[-10:]}")
else:
    print(f"Sample primes: {found_primes}")
print("--- Calculation Finished ---")