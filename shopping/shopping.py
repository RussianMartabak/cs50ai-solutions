import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # read a file, handle the csv cells, need to classify columns
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        line = 0
        evidences = []
        labels = []
        for row in reader:
            if line > 0 :
                # all evidence for a cell
                cellEv = []
                # label for a cell
                cellLabel = 0
                curColumn = 0
                for column in row:
                    if curColumn < 17:
                        value = numeric_converter(column, curColumn)
                        cellEv.append(value)
                    elif column == "TRUE":
                        cellLabel = 1
                    curColumn += 1
                evidences.append(cellEv)
                labels.append(cellLabel)  
                     
            line += 1
        
        return (evidences, labels)

def numeric_converter(content, colnumber):
    # month is at col 10, visitor at col 15, week at col 16 
    varGruppen = {
        "int" : [0, 2, 4, 11, 12, 13, 14],
        "float" : [1, 3, 5, 6, 7, 8, 9]
    }
    months = {
        "Jan" : 0, "Feb" : 1, "Mar" : 2, "Apr" : 3, "May" : 4, "June" : 5, "Jul" : 6, "Aug" : 7,
        "Sep" : 8, "Oct" : 9, "Nov" : 10, "Dec" : 11
    }
    if colnumber in varGruppen["int"]:
        return int(content)
    elif colnumber in varGruppen["float"]:
        return float(content)
    # special vars
    elif colnumber == 10:
        return months[content]
    elif colnumber == 15:
        if content == "Returning_Visitor":
            return 1
        else:
            return 0
    elif colnumber == 16:
        if content == "TRUE":
            return 1
        else:
            return 0

    

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    ai = KNeighborsClassifier(n_neighbors=1)
    ai.fit(evidence, labels)
    return ai


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    truePositives = 0
    trueNegatives = 0
    for lab in labels:
        if lab == 1:
            truePositives += 1
        else:
            trueNegatives += 1
    correctPositives = 0
    correctNegatives = 0
    
    xy = zip(labels, predictions)
    comparison = list(xy)
    for c in comparison:
        if c[0] == c[1]:
            if c[0] == 1:
                correctPositives += 1
            elif c[0] == 0:
                correctNegatives += 1
    sensitivity = correctPositives / truePositives
    specificity = correctNegatives / trueNegatives
    
    return (sensitivity, specificity)

    

if __name__ == "__main__":
    main()
