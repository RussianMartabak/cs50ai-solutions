import csv
import itertools
import sys
import copy

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # find the probabilities of all that thing and multiply it together. now thats a join one
    # make proper query first about genes
    # need unit test to make sure this works well
    query = copy.deepcopy(people)
    for person in people:
        people[person]['prob'] = 0
        if person in one_gene:
            query[person]["gene"] = 1
        elif person in two_genes:
            query[person]["gene"] = 2
        else:
            query[person]["gene"] = 0
        # set trait
        if person in have_trait:
            query[person]['trait'] = True
        else:
            query[person]['trait'] = False
        

    # make an array for parent's string
    calculatedProb = []
    
    
    
    for person in people:
        probability = QProbability(
            query[person],
            query, 
            query[person]['mother'],
            query[person]['father'],
            
            )
        calculatedProb.append(probability)


    result = 1
    for value in calculatedProb:
        result *= value
        
    return result
    raise NotImplementedError


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    people = []
    knowledge = {}
    # form a data for each person
    # find out all the people present
    # we have no info of those with 0 gene or not trait
    # we can steal those from argument!!
    for person in probabilities:
        if person in two_genes:
            target = probabilities[person]['gene'][2]
            probabilities[person]['gene'][2] += p
            
        elif person in one_gene:
            probabilities[person]['gene'][1] += p
            
            
        else:
            probabilities[person]['gene'][0] += p
            
        # now for trait
        if person in have_trait:
            probabilities[person]['trait'][True] += p
            
        else:
            probabilities[person]['trait'][False] += p
           
    return
        
    raise NotImplementedError


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        sumGene = 0
        
        
        for i in range(3):
            sumGene += probabilities[person]['gene'][i]
        
        geneConstant = 1 / sumGene
        for i in range(3):
            probabilities[person]['gene'][i] *= geneConstant
            probabilities[person]['gene'][i] = round(probabilities[person]['gene'][i], 4)
        
        # for trait
        sumTrait = probabilities[person]['trait'][False] + probabilities[person]['trait'][True]
        traitConstant = 1 / sumTrait
        probabilities[person]['trait'][False] *= traitConstant
        probabilities[person]['trait'][False] = round(probabilities[person]['trait'][False], 4)

        probabilities[person]['trait'][True]  *= traitConstant
        probabilities[person]['trait'][True] = round(probabilities[person]['trait'][True], 4)
    

def QProbability(personalquery, query, motherName=None, fatherName=None):
    # calculate an individual query
    # need a query, mother's query with probability
    # need to reason to make possibilities to be checked
    inheritProbs = {
        2: 1,
        0: 0,
        1: 0.5
    }
    # base state
    if motherName == None:
        geneNumber = personalquery['gene']
        geneProb = PROBS["gene"][geneNumber]
        if personalquery['trait'] is True:
            return PROBS['trait'][geneNumber][True] * geneProb
        elif personalquery['trait'] is False:
            return PROBS['trait'][geneNumber][False] * geneProb
    # here come recursiveness eh maybe not needed...
    # i just need to know the parent's genes and trait query. the rest can be multiplied
    # after every prob is calculated
    else:
        # has parent
        # need to calc trait too after this
        father = query[fatherName]
        mother = query[motherName]
        traitProb = PROBS["trait"][personalquery['gene']][personalquery['trait']]
        if personalquery["gene"] == 0:
            # prob of m and f not inheriting
            mchance = abs(1 - inheritProbs[mother['gene']] - PROBS['mutation'])
            fchance = abs(1 - inheritProbs[father['gene']] - PROBS["mutation"])
            inheritProb = mchance * fchance
            return inheritProb * traitProb
        elif personalquery["gene"] == 1:
            # prob of m and not f, f and not m
            mchance = abs(inheritProbs[mother['gene']] - PROBS['mutation'])
            fchance = abs(1 - inheritProbs[father['gene']] - PROBS['mutation'])
            case1 = mchance * fchance
            # f not m
            mchance = abs(inheritProbs[father['gene']] - PROBS['mutation'])
            fchance = abs(1 - inheritProbs[mother['gene']] - PROBS['mutation'])
            case2 = mchance * fchance
            inheritProb = case1 + case2
            return inheritProb * traitProb
        elif personalquery["gene"] == 2:
            # prob of both m and f inherit
            mchance = abs(inheritProbs[mother['gene']] - PROBS['mutation'])
            fchance = abs(inheritProbs[father['gene']] - PROBS['mutation'])
            inheritProb = mchance * fchance
            return inheritProb * traitProb
    raise NotImplementedError
    
if __name__ == "__main__":
    main()
