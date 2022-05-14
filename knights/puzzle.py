from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # TODO
    #exclusive or
    # how to represent not proposition, but a saying by A???
    # either his statement true or he is knave cuz lying
    Or(And(AKnight, AKnave), And(AKnave, Not(AKnight))),
    # A character can only be one
    Or(And(AKnight, Not(AKnave)), And(AKnave, Not(AKnight)))
    

)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # TODO
    # A character can only be one
    Or(And(AKnight, Not(AKnave)), And(AKnave, Not(AKnight))),
    Or(And(BKnight, Not(BKnave)), And(BKnave, Not(BKnight))),
    # Either A is lying so b is knight or else
    Or(And(AKnave, BKnave), And(AKnave, BKnight)),
    # If A is honest about his statement he is knight
    Implication(And(AKnave, BKnave), AKnight)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # TODO
     # A character can only be one
    Or(And(AKnight, Not(AKnave)), And(AKnave, Not(AKnight))),
    Or(And(BKnight, Not(BKnave)), And(BKnave, Not(BKnight))),
    # The statements and their implications
    Implication(Or(And(AKnave, BKnave), And(AKnight, BKnight)), And(AKnight, BKnave)),
    Implication(Or(And(AKnave, BKnight), And(AKnight, BKnave)), And(AKnave, BKnight)),
    
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # TODO
    # A character can only be one
    Or(And(AKnight, Not(AKnave)), And(AKnave, Not(AKnight))),
    Or(And(BKnight, Not(BKnave)), And(BKnave, Not(BKnight))),
    Or(And(CKnight, Not(CKnave)), And(CKnave, Not(CKnight))),
    # implications of whether C is knave or not
    # only one between B and C can be knight
    # if C is honest then A is a knight and B lying
    Implication(CKnave, And(BKnight, AKnave)),
    Implication(CKnight, And(BKnave, AKnight)),
    # if A say he is knave and he is actually knave and he is a knight cus honest 
    # at the same time 
    Implication(And(BKnight, CKnave), And(AKnave, AKnight))
    
    
    
    # If he A says he is Knave and right that would make him a Knight lol 
    # which is not possible but ok


)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
