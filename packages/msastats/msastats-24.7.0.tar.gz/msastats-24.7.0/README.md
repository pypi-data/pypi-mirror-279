# MSAStats

A simple utility to compute multiple sequence alignment statistics.

# Example usage:

```python
import msastats

# To calculate based on a list of string sequences:
msastats.calculate_msa_stats(["AA-A","AA-A","A--A"])

# To calculate based on a fasta msa file:
msastats.calculate_fasta_stats("/path/to/file.fasta")

# Get a list of the summary statistics names:
msastats.stats_names()
```