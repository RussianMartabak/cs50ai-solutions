import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # if number of cells and count is the same and is not zero
        if len(self.cells) == self.count and self.count > 0:
            return self.cells
        return None
        raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        #if its zero all the cells is definitely safe
        if len(self.cells) > 0 and self.count == 0:
            return self.cells
        return None
        raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
        return
        raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
        return
        raise NotImplementedError


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)
        # make a sentence
        
        # get all cell's neighbors
        neighbors = []
        # if row is not zero add the upper three cells
        # if 8 skip bottom checking
        # if column is not zero add left and right too
        # if zero add only right if 8 add only left 
        row = cell[0]
        column = cell[1]
        # start at upper row and leftmost column, scan all column and move on
        for i in range(row - 1, row + 2, 1):
            for j in range(column - 1, column + 2, 1):
                currentCell = (i, j)
                if (i >= 0 and j >= 0 and currentCell != cell and i < self.height 
                and j < self.width):
                    neighbors.append((i, j))
        
        # add all neigbouring cells and its counts exclude a cell that has been marked
        for cell in neighbors:
            if cell in self.safes:
                neighbors.remove(cell)
            if cell in self.mines:
                neighbors.remove(cell)
                count -= 1
        # add knowledge 
        self.knowledge.append(Sentence(neighbors, count))
        # conclude a mine or safe based on existing knowledge
        safes = []
        mines = []
        for sentence in self.knowledge:
            if sentence.known_safes():
                safes = list(sentence.known_safes())
                for cell in safes:
                    self.mark_safe(cell) # this remove a cell from a sentence
            if sentence.known_mines():
                mines = list(sentence.known_mines())
                for cell in mines:
                    self.mark_mine(cell)
        # infer new sentences
        # if a sentence is a subset, make new sentence and delete both
        for sentence in self.knowledge:
            for peer in self.knowledge:
                if (len(sentence.cells.difference(peer.cells)) == 0  
                and len(peer.cells) > len(sentence.cells)):
                    # add new sentence that contains things that not exist in the subset
                    # handle count
                    cells = peer.cells.difference(sentence.cells)
                    counts = peer.count - sentence.count
                    self.knowledge.remove(peer)
                    
                    
                    # add new sentence
                    self.knowledge.append(Sentence(cells, counts))
                elif (len(peer.cells.difference(sentence.cells)) == 0  
                and len(sentence.cells) > len(peer.cells)):
                    # add new sentence that contains things that not exist in the subset
                    # handle count
                    cells = sentence.cells.difference(peer.cells)
                    counts = sentence.count - peer.count
                    # removing nothing because need to ensure they a
                    self.knowledge.remove(peer)
                    
                    
                    
                    # add new sentence
                    self.knowledge.append(Sentence(cells, counts))



        return
        raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # return known safe thats not in move made
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
       
        return None
        raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # check if knowledge if empty : random
        if len(self.knowledge) == 0:
            randi = random.randint(0, self.height - 1)
            randj = random.randint(0, self.width - 1)
            while ((randi, randj) in self.moves_made or (randi, randj) in self.mines):
                randi = random.randint(0, self.height - 1)
                randj = random.randint(0, self.width - 1)
            return (randi, randj)
        # get a list of sentences from knowledge that not contain explored cell
        cleanSentences = []
        
        for sentence in self.knowledge:
            clean = True
            for cell in self.mines:
                if cell in sentence.cells:
                    clean = False
                    break
            for cell in self.moves_made:
                if cell in sentence.cells:
                    clean = False
                    break
            if clean and len(sentence.cells) != 0 :
                cleanSentences.append(sentence)

        # pick the one that has the biggest ratio of munber of cells per count
        max = 0
        best = None
        for sentence in cleanSentences:
            if sentence.count == 0:
                continue
            ratio = len(sentence.cells) / sentence.count
            if ratio > max :
                max = ratio
                best = sentence.cells.copy()
        
        
        # pick a random cell from sentence's set if the best was found
        if best:
            index = random.randint(0, len(best))
            return best.pop()
        
        return None
        raise NotImplementedError
