# matching-statistics

The MatchingStatistics library computes matching statistics for a pattern string against an input string using a suffix tree. It efficiently determines the position and length of the longest exact match for each suffix of the pattern within the input string.

## Installation

```bash
pip install matching-statistics
```

## Usage

```python
from matching_statistics.MatchingStatistics import MatchingStatistics

# Initialize with input string
input_string = "your_input_string_here"
matching_statistics = MatchingStatistics(input_string)

# Compute matching statistics for a pattern
input_pattern = "your_pattern_here"
ms_table = matching_statistics.get_matching_statistics_table(input_pattern)
```
# Comparison of Implementations

## Naive Implementation

The naive approach computes matching statistics by directly comparing the pattern with substrings of the input string. The time complexity of this approach is O(pattern_length * pattern_length * input_string_length). This arises because for each position in the input string, we potentially compare up to the length of the pattern.

## Suffix Tree Implementation

The suffix tree implementation leverages advanced data structures to achieve efficient pattern matching statistics computation. Specifically, it operates in linear time relative to the length of the pattern, O(pattern_length). This efficiency stems from the preprocessing step that constructs the suffix tree from the input string. Once constructed, the tree allows rapid lookup and comparison of patterns against suffixes of the input string.

## Performance Comparison

The performance difference between the two approaches can be significant for large input strings and patterns. While the naive method's complexity grows quadratically with the pattern length and linearly with the input string length, the suffix tree method ensures that the time complexity remains linear in relation to the pattern length. Therefore, for longer patterns or large input strings, the suffix tree implementation provided by `matching-statistics` offers considerable performance advantages.

![Time Complexity Comparison](images/time.png)