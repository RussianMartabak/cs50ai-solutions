from operator import ne
import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # each variable on domains contain a set of words
        # modify domains
       
        for var in self.domains:
            for word in self.domains[var].copy():
                if (len(word) != var.length):
                    self.domains[var].remove(word)
                
        return
                
            



        raise NotImplementedError

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        overlap = self.crossword.overlaps[x, y]
        i = overlap[0]
        j = overlap[1]
        for xword in self.domains[x].copy():
            # is there a suitable choice for y given the word we are checking rn?
            exist = False
            for yword in self.domains[y]:
                if xword != yword and xword[i] == yword[j]:
                    exist = True
                    break
            if not exist:
                self.domains[x].remove(xword)
                revised = True



        return revised
        raise NotImplementedError

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        queue = []
        if len(queue) == 0:
            for var in self.crossword.variables:
                neighbors = self.crossword.neighbors(var)
                for nei in neighbors:
                    queue.append((var, nei))
        else:
            queue = arcs
        
        while len(queue) != 0:
            convar = queue.pop(0)
            x = convar[0]
            y = convar[1]
            if self.revise(convar[0], convar[1]):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x):
                    if z != y:
                        queue.append((z, x))

        return True

        raise NotImplementedError

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """ 
        # keyerror?
        complete = True
        for var in self.crossword.variables:
            if var not in assignment or assignment[var] == None:
                complete = False
                break
        
        return complete
        raise NotImplementedError

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        consist = True
        for var in assignment:
            cword = assignment[var]
            if len(cword) != var.length:
                consist =  False
                break
            # WIP check overlaps consistency
            neighbors = self.crossword.neighbors(var)
            for y in neighbors:
                if y in assignment:
                    overl = self.crossword.overlaps[var, y]
                    i = overl[0]
                    j = overl[1]
                    yword = assignment[y]
                    if yword == cword or cword[i] != yword[j]:
                        consist = False
                        break
        return consist
        raise NotImplementedError

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        domains = {

        }
        for word in self.domains[var]:
            domains[word] = 0
        neighbors = self.crossword.neighbors(var)
        for neighbor in neighbors.copy():
            if neighbor in assignment:
                neighbors.remove(neighbor)
        # neighbors refer to unassigned neigbors
        # calculate n (number of impossible choices in y's domains)
        for val in domains:
            # word in x's domain
            for y in neighbors:
                overlap = self.crossword.overlaps[var, y]
                i = overlap[0]
                j = overlap[1] 
                for yword in self.domains[y]:
                    # count those that dont match
                    if val == yword or val[i] != yword[j]:
                        domains[val] += 1 

        # domains is a set
        # sort the dict and return list
        result = sorted(domains, key=lambda domain : domains[domain])
        return result

        raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # assignment is var : string dictionary
        variables = self.crossword.variables
        assigned = []
        for key in assignment:
            assigned.append(key)
        # fix heuristic late
        # heuristic: find mvr values
        minLen = 999999999
        for var in variables:
            if var not in assigned:
                minLen = min(minLen, len(self.domains[var]))
        # put a list of vars with the maximum len specified
        minLens = []
        for var in variables:
            if var not in assigned and len(self.domains[var])  == minLen:
                minLens.append(var)

        # pick the one with highest degrees if more 
        if len(minLens) == 1:
            return minLens[0]
        else:
            survivor = minLens[0]
            for var in minLens:
                degree = self.crossword.neighbors(var)
                survDegree = self.crossword.neighbors(survivor)
                if degree > survDegree:
                    survivor = var
            return survivor
        

        

        raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            if value not in assignment:
                assignment[var] = value
                if self.consistent(assignment):
                    result = self.backtrack(assignment)
                    if result:
                        return result
                del assignment[var]
        return False
        raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
