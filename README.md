Quick-and-dirty experiment looking at the rate of common misspellings on Reddit over time.

- `clusters.txt`: each line is a comma-separated list of spellings of a particular term, with the first being the correct spelling, and the rest being incorrect spellings. These may also be multi-word phrases. Lines beginning with '#' are ignored.
- `ngrams.py`: script to query the Pushshift API for annual counts of each of the forms in clusters.txt
- `data/`: directory of json files which are the result of running ngrams.py.
- `viz.ipynb`: IPython notebook exploring and visualizing the data

## Choice of misspellings

The patterns in `clusters.txt` were mostly taken from the Wikipedia article [Commonly misspelled English words](https://en.wikipedia.org/wiki/Commonly_misspelled_English_words). I was interested in misspellings born out of ignorance, rather than deliberate casual shortenings ("u", "imma") or typos ("thsi").

I included some multi-word phrases indicative of homophone errors (e.g. "take a peak") - since these are less likely to be flagged or autocorrected by software, they provide an interesting sort of control group.

A number of common misspellings needed to be excluded because they were valid words in other languages. For example: *ocasion*, *adress*, *dilema*.

## Future work

It would be interesting to see whether the patterns found on Reddit replicated for other social media datasets over the same time period. Because Twitter provides metadata about what platform a tweet was composed on ("Twitter for Android", "Twitter for desktop", etc.), it would be especially useful for investigating the effect of spellcheck/autocorrect of different platforms on misspelling rates.
