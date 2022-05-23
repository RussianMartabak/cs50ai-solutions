import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000
# actually 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # look at page links to other page then calculate probability
    result = {}
    unlinked = []
    randomChoice = 1 - damping_factor

    # page is a key in corpus dict, given the string get all links in set
    # need to exclude the linked page from random choice calcr 
    # loop over linked pages from current page
    links = corpus[page]
    # assign random prob to everything
    for webpage in corpus:
        result[webpage] = randomChoice / len(corpus)
    # if no link add same prob to eveything
    if len(links) == 0:
        for item in result:
            result[item] += damping_factor / len(corpus)
        return result
    # if link, add prob between them
    for link in links:
        result[link] += damping_factor / len(links)
    # set up prob for a link to be clicked
    return result
    raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # make a list of weights for each corpus
    counts = {}
   
    curPage = random.choice(list(corpus))
    # set up counter
    for webpage in corpus:
        counts[webpage] = 0
    
    # start sampling
    for i in range(n):
        counts[curPage] += 1
        weights  = []
        probs = transition_model(corpus, curPage, damping_factor)
        for prob in probs:
            weights.append(probs[prob])
        nextPage = random.choices(list(probs), weights=weights, k=1)
        curPage = nextPage[0]

        # change startpage everytime we resolve it

    # sum all counts
    sum = 0
    for key in counts:
        sum += counts[key]
    for key in counts:
        counts[key] /= sum

    return counts
    raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
