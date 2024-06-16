import random
import time
from tqdm import tqdm
from matching_statistics.MatchingStatistics import MatchingStatistics

def generate_random_string(alphabet, size):
    return ''.join(random.choices(alphabet, k=size))

def generate_random_pattern(alphabet, size):
    return generate_random_string(alphabet, size)

def naive_matching_statistics(input_string, input_pattern):
    """
    Compute the Matching Statistics using the Naive Algorithm.
    
    input:
        input_string: the large text
        input_pattern: the string for which matching statistics needs to be calculated
    output:
        MS_TABLE: Matching statistics table containing the first occurrence & length of the maximal-exact-match of each suffix in pattern  
    """
    MS_TABLE = dict()

    for i in range(len(input_pattern)):
        max_match_length = 0
        max_match_index = None
        
        for j in range(len(input_string)):
            curr_match_length = 0

            while (j + curr_match_length < len(input_string) and 
                   i + curr_match_length < len(input_pattern) and
                   input_string[j + curr_match_length] == input_pattern[i + curr_match_length]):
                curr_match_length += 1
        
            if curr_match_length > max_match_length:
                max_match_length = curr_match_length
                max_match_index = j
        
        MS_TABLE[i] = (max_match_index, max_match_length)
    
    return MS_TABLE

def compare_matching_statistics(input_string, input_pattern):
    # Using MatchingStatistics class for suffix tree matching statistics
    matching_statistics = MatchingStatistics(input_string)
    st_result = matching_statistics.get_matching_statistics_table(input_pattern)
    
    start_cpu_naive = time.time()
    naive_result = naive_matching_statistics(input_string, input_pattern)
    end_cpu_naive = time.time()
    naive_cpu_time = end_cpu_naive - start_cpu_naive
    
    start_cpu_st = time.time()
    st_result = matching_statistics.get_matching_statistics_table(input_pattern)
    end_cpu_st = time.time()
    st_cpu_time = end_cpu_st - start_cpu_st
    
    return naive_result == st_result, naive_cpu_time, st_cpu_time

def main(input_string_size, num_patterns_start, num_patterns_end):
    alphabet = "abc"
    
    input_string = generate_random_string(alphabet, input_string_size)

    for pattern_size in tqdm(range(num_patterns_start, num_patterns_end + 1, 5), desc='Generating patterns'):
        input_pattern = generate_random_pattern(alphabet, pattern_size)
        
        try:
            result, naive_cpu_time, st_cpu_time = compare_matching_statistics(input_string, input_pattern)
            if not result:
                print(f"Input String: {input_string}")
                print(f"Input Pattern: {input_pattern}")
                print(f"Unexpected result: {result}")
                print("-" * 50)
                print(f"Pattern Size: {pattern_size}, Naive Time: {naive_cpu_time:.6f}s, Suffix Tree Time: {st_cpu_time:.6f}s")
        
        except Exception as e:
            print(f"Some error occurred: {e}")
            print(f"Input String: {input_string}")
            print(f"Input Pattern: {input_pattern}")

if __name__ == "__main__":
    INPUT_STRING_START = 800
    INPUT_STRING_END = 1201
    
    for i in range(INPUT_STRING_START, INPUT_STRING_END, 200):
        input_string_size = i
        num_patterns_start, num_patterns_end = 5, 400
        main(input_string_size, num_patterns_start, num_patterns_end)
