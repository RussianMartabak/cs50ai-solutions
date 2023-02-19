import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | NP VP Conj NP VP | NP VP Conj VP | NP VP P NP | NP VP P NP
NP -> N | Det N | Det N P N | NP P N | Det Adj N | Det N Adv | Det Adj Adj Adj N | Det N P Det N
VP -> V | V NP | V P NP | N V | V P NP VP | Adv V NP | V Adv | V VP V P N | V NP P Det Adj N

"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def check_NP(subtree):
    # check the subtree's child
    # bug = the subtree will be obliterated if contain an NP
    subpos = 0
    for sub in subtree.subtrees():
        subpos += 1
        if sub.label() == 'NP' and subpos > 1:
            return False
    return True

def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    r = nltk.tokenize.word_tokenize(sentence)
    for i in range(len(r) - 1, -1, -1):
        r[i] = r[i].lower()
        if r[i].isalpha() == False:
            r.remove(r[i])
    return r
    raise NotImplementedError


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # will need to use subtrees, label and leaves methods
    rs = []
    for subt in tree.subtrees():
        if subt.label() == 'NP' and check_NP(subt) == True:    
            rs.append(subt)
    return rs
    raise NotImplementedError


if __name__ == "__main__":
    main()
