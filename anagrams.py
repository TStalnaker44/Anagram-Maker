
from collections import Counter
from itertools import permutations
import random

SEED = "make anagrams"

VOWELS = "aeiouy"
TRIGRAM_DROPOUT = .0001
DIGRAPH_DROPOUT = .001

def main():
    with open("anagram.txt", "w") as file:
        parts = []
        for part in SEED.split(' '):
            results = getAnagram(part)
            parts.append(results)
            for r in results: file.write(r + "\n")
            file.write(("-"*40) + "\n")
    # Print random anagram
    for x in range(10):
        print(" ".join([random.choice(p) for p in parts]))
        
        


def getAnagram(seed):

    seed = seed.lower()
    
    # Read in the dictionary of words
    with open("words.txt", "r") as file:
        words = file.readlines()

    # Read in the trigram frequencies
    with open("trigram_freqs.txt", "r") as file:
        tri_freqs = [tuple(x.split()) for x in file.readlines()]
        tri_total = sum([int(x[1]) for x in tri_freqs])
        tri_freqs = [(t[0], int(t[1]) / tri_total) for t in tri_freqs]
        trigrams = [y[0] for y in filter(lambda x: x[1] < TRIGRAM_DROPOUT, tri_freqs)]

    # Read in the digraph frequencies
    with open("digraph_freqs.txt", "r") as file:
        di_freqs = [tuple(w.lower() for w in line.split()) for line in file.readlines()]
        di_total = sum([int(x[1]) for x in di_freqs])
        di_freqs = [(d[0], int(d[1]) / di_total) for d in di_freqs]
        digraphs = [y[0] for y in filter(lambda x: x[1] < DIGRAPH_DROPOUT, di_freqs)]

    # Get the list of words the same length as the seed
    wordLyst = [w.lower() for w in words if len(w)==len(seed)]

    # Build c-v mapping for words in wordLyst
    cvmapping = cvMap(wordLyst)

    # Filter on c-v mapping
    results = cvFilter(seed, cvmapping)

    # Filter on trigrams
    results = ngramFilter(results, trigrams)

    # Filter on digrams
    results = ngramFilter(results, digraphs)

    results = list(results)
    results.sort()
    return results

def cvMap(words):
    wordMap = []
    for w in words:
        wordMap.append("".join(["v" if l in VOWELS else "c" for l in w]))
    totalPatterns = len(set(wordMap))
    percentToRemove = .05
    numToRemove = int(totalPatterns * percentToRemove)
    topPatterns = Counter(wordMap).most_common(totalPatterns-numToRemove)
    return set([pattern for pattern, count in topPatterns])

def cvFilter(i, cvMapping):
    perms = {"".join(p) for p in permutations(i)}
    cvfilter = set()
    for word in perms:
        if "".join(["v" if l in VOWELS else "c" for l in word]) in cvMapping:
            cvfilter.add(word)
    return cvfilter

def ngramFilter(current, ngrams):
    nfilter = set()
    for word in current:
        for t in ngrams:
            if t in word:
                nfilter.add(word)
                break
    return current - nfilter

    
    

if __name__ == "__main__":
    main()
