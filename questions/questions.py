import nltk
import sys
import os
import string
import math
import copy

FILE_MATCHES = 1
SENTENCE_MATCHES = 3


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)

def count_word_occurence(word, exception, document):
    """
    Given an exception key and the documents dict count the word occurence
    """
    count = 0
    dockeys = document.keys()
    for key in dockeys:
        if word in document[key] and key != exception:
            count += 1
    return count


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    path = directory
    files = os.listdir(path)
    index = {}
    for file in files:
        with open(os.path.join(path, file), encoding='utf-8') as f:
            index[file] = f.read()
    
    return index


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    res = nltk.word_tokenize(document)
    for r in range(len(res) - 1, -1, -1):
        res[r] = res[r].lower()
        if res[r] in string.punctuation or res[r] in nltk.corpus.stopwords.words("english"):
            res.remove(res[r])
    return res
    


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    my_dict = {}
    dockeys = documents.keys()
    totaldocs = len(dockeys)
    for key in dockeys:
        for word in documents[key]:
            if word not in my_dict.keys():
                my_dict[word] = 1 + count_word_occurence(word, key, documents)
        
    wordkeys = my_dict.keys()
    for word in wordkeys:
        my_dict[word] = math.log(totaldocs / my_dict[word])
    return my_dict
    # need total number of documents and number of docs containing the specific word
    # each time encounter a word, look all the files that have it too
    raise NotImplementedError

def count_sumidf(query, file, idfs):
    """
    Given file (list of words), and idfs (dict of word -> idfs) return sum of idfs for words in query

    """
    tot = 0
    for f in file:
        if f in query:
            tot += idfs[f]
    return tot
def sort_idf(the_dict):
    """
    Given a dict, sort it descending based on its key (idfsum)
    """
    res = sorted(the_dict.items(), key=lambda x:x[1], reverse=True)
    return res
def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    # Files should be ranked according to the sum of tf-idf values for any word 
    # in the query that also appears in the file
    res = []
    index = {}
    fkeys = files.keys()
    # make a dict of filenames = idfsum
    for file in fkeys:
        idf = count_sumidf(query, files[file], idfs)
        index[file] = idf
    index = sort_idf(index)
    # sort the dict
    for i in range(n):
        res.append(index[i][0])
    # return the list of filenames with n restraint
    return res
    
def count_density(query, sentence):
    qw = 0
    for w in sentence:
        if w in query:
            qw += 1
    return qw / len(sentence)

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    res = []
    index = {}
    wkeys = sentences.keys()
    for file in wkeys:
        idf = count_sumidf(query, sentences[file], idfs)
        index[file] = idf
    index = sort_idf(index)
    
    # prune to only included n number of sentences
    for i in range(len(index) - 1, -1, -1):
        if i > n - 1:
            index.remove(index[i])
    # seek out tied items
    for i in range(0, len(index) - 2, 1):
        if index[i][1] == index[i + 1][1]:
            #switch
            temp = copy.deepcopy(index[i])
            if count_density(query, index[i + 1][0]) > count_density(query, index[i][0]):
                index[i] = index[i + 1]
                index[i + 1] = temp
    for i in range(n):
        res.append(index[i][0])
            
    return res
    

if __name__ == "__main__":
    main()
