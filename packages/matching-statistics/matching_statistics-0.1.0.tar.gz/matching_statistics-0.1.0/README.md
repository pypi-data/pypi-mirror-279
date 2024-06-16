# matching-statistics

The MatchingStatistics library computes matching statistics for a pattern string against an input string using a suffix tree. It efficiently determines the position and length of the longest exact match for each suffix of the pattern within the input string.

## Installation

```bash
pip install matching-statistics
```

## Usage

```python
from matching_statistics import MatchingStatistics

# Initialize with input string
input_string = "your_input_string_here"
matching_statistics = MatchingStatistics(input_string)

# Compute matching statistics for a pattern
input_pattern = "your_pattern_here"
ms_table = matching_statistics.get_matching_statistics_table(input_pattern)
```
