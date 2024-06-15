## Czech Syllable Splitter
Alogirthm for splitting Czech words into syllables.
Inspired by a syllable counting algorithm from David Lukeš counting the vowels.

With Klára Bendová we put together rules to expand the vowels into syllables,
empirically finding some common letter groups to stay intact.

This is not a perfect solution, but it is a good start for Czech language processing.
Measuring the accuracy of this algorithm is a to-do, as well as adding more rules if needed.

### Installation
```bash
pip install czech-syllable-splitter
```
or using Poetry package manager
```bash
poetry add czech-syllable-splitter
```

### Usage

```python
from czech_syllable_splitter import count_syllables, split_to_syllables, split_to_characters

print(split_to_syllables("příliš"))
print(split_to_characters("přesný"))
print(count_syllables("přísný"))
```

### Lint & Test
```bash
poetry run python3 -m pytest
poetry run mypy czech_syllable_splitter
poetry run pylint czech_syllable_splitter

```
