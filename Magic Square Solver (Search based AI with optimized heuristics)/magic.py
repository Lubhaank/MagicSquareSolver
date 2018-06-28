'''
--------------------------------------------------------------------------------
Specs: given a file like below, find a magic square with non-neg numbers
First line is dimension (n) of square
Next d lines contain the grid. -1 is placeholder for empty, modifiable value
Next line contains n row sums (first number is sum of top row)
Next line contains n col sums (first number is sum of leftmost col)
Next line contains 2 diag sums (first number is top-left to bottom-right)
--------------------------------------------------------------------------------
3
-1 -1 0
5 -1 2
-1 -1 -1
10 8 9
12 10 5
9 3
--------------------------------------------------------------------------------
From the above input, the following would be appropriate output (stdout)
--------------------------------------------------------------------------------
True
5 5 0
5 1 2
2 4 3
--------------------------------------------------------------------------------
'''

import sys
import copy

def read_input(path):
        #the actual grid
        input_grid = []
        with open(path) as reader:
                # dimension
                size = int(reader.readline().rstrip())

                for i in xrange(size):
                        vals = [int(x) for x in reader.readline().rstrip().split(' ')]
                        input_grid.append(vals)

                # Do stuff with these
                #constraints
                row_sums = [int(x) for x in reader.readline().rstrip().split(' ')]
                col_sums = [int(x) for x in reader.readline().rstrip().split(' ')]
                diag_sums = [int(x) for x in reader.readline().rstrip().split(' ')]
                #all positions that can be changed that is the varibles of the CSP


        return solveGrid(size,input_grid,row_sums,col_sums,diag_sums)



class Stack(object):

        def __init__(self):
                self.stack = []

        def pop(self):
                elem = self.stack[len(self.stack) - 1]
                self.stack.pop()
                return elem

        def push(self,elem):
                self.stack.append(elem)

        def isEmpty(self):
                if(len(self.stack) == 0):
                        return True
                return False
        def returnStack(self):
                return self.stack


def solveGrid(size,grid,row_sums,col_sums,diag_sums):

        variableIndexes = []
        mostConstrainedScoreRow = [0]*size
        mostConstrainedScoreCol = [0]*size
        mostConstrainedScoreDiag = [0,0]

        for x in range(0,size):
                        for y in range(0,size):
                                if(grid[x][y] == -1):
                                        variableIndexes.append([x,y])
                                else:
                                        mostConstrainedScoreRow[x] += 1
                                        mostConstrainedScoreCol[y] += 1
                                        if(x == y):
                                                mostConstrainedScoreDiag[0] += 1
                                        if( x == (size - y - 1)):
                                                mostConstrainedScoreDiag[1] += 1


        lenVariableIndexes = len(variableIndexes)
        tempVariableIndexes = [0]*lenVariableIndexes

        for i in range(0,lenVariableIndexes):
                score = 0
                row = variableIndexes[i][0]
                col = variableIndexes[i][1]
                score = mostConstrainedScoreRow[row] + mostConstrainedScoreCol[col]
                if(row == col):
                        score += mostConstrainedScoreDiag[0]
                if(row == size - col - 1):
                        score += mostConstrainedScoreDiag[1]
                tempVariableIndexes[i] = score

        for i in range(0,lenVariableIndexes):
                for j in range(0,lenVariableIndexes - i - 1):
                        if(tempVariableIndexes[j] < tempVariableIndexes[j + 1]):
                                tempVariableIndexes[j],tempVariableIndexes[j+ 1] = tempVariableIndexes[j+1],tempVariableIndexes[j]
                                variableIndexes[j],variableIndexes[j+ 1] = variableIndexes[j+1],variableIndexes[j]




        Domain = [0]*len(variableIndexes)
        for i in range(0,len(variableIndexes)):
                Domain[i] = [0,1,2,3,4,5,6,7,8,9]



        counterVariables = 0
        stackVariables = Stack()
        stackDomainIndex = Stack()
        firstVariable = variableIndexes[counterVariables]
        stackVariables.push(firstVariable)

        firstRow = firstVariable[0]
        firstCol = firstVariable[1]
        minValRow = 0
        minValCol = 0
        minValDiagOne = 0
        minValDiagTwo = 0
        for i in range(0,size):
                if(grid[firstRow][i] != -1):
                        minValRow += grid[firstRow][i]

                if(grid[i][firstCol] != -1):
                        minValCol += grid[i][firstCol]

                if(grid[firstRow][i] == -1):
                        if(i == firstCol):
                                minValRow += 0
                        else :
                                minValRow += 9

                if(grid[i][firstCol] == -1):
                        if(i == firstRow):
                                minValCol += 0
                        else:
                                minValCol += 9
                if(grid[i][i] != -1):
                        minValDiagOne += grid[i][i]
                if(grid[i][size - i -1] != -1):
                        minValDiagTwo += grid[i][size - i - 1]
                if(grid[i][i] == -1):
                        if(i == firstRow and i == firstCol):
                                minValDiagOne += 0
                        else:
                                minValDiagOne += 9
                if(grid[i][size - i -1] == -1):
                        if( i == firstRow and (size - i - 1) == firstCol):
                                minValDiagTwo += 0
                        else :
                                minValDiagTwo += 9

        lowLimitRow = row_sums[firstRow] - minValRow
        lowLimitCol = col_sums[firstCol] - minValCol
        lowLimitDiagOne = diag_sums[0] - minValDiagOne
        lowLimitDiagTwo = diag_sums[1] - minValDiagTwo
        if(firstRow == firstCol and firstRow == size - firstCol -1):
                startIndex = max([lowLimitRow,lowLimitCol,lowLimitDiagOne,lowLimitDiagTwo])
        elif(firstRow == firstCol):
                startIndex = max([lowLimitRow,lowLimitCol,lowLimitDiagOne])
        elif(firstRow == size - firstCol - 1):
                startIndex = max([lowLimitRow,lowLimitCol,lowLimitDiagTwo])
        else:
                startIndex = max([lowLimitRow,lowLimitCol])
        if(startIndex < 0):
                startIndex = 0
        stackDomainIndex.push(startIndex)
        check = allAssigned(size,grid)

        while(check == False):


                elem = stackVariables.pop()
                stackVariables.push(elem)

                index = stackDomainIndex.pop()
                stackDomainIndex.push(index)


                if(index > 9):


                        stackDomainIndex.pop()
                        if(stackDomainIndex.isEmpty() == True):

                                print("False")
                                return


                        prev_index = stackDomainIndex.pop()
                        stackDomainIndex.push(prev_index + 1)
                        prev = stackVariables.pop()
                        grid[prev[0]][prev[1]] = -1

                        counterVariables-=1
                        continue

                row = elem[0]
                col = elem[1]
                domain = Domain[variableIndexes.index(elem)]
                value = domain[index]
                temp = copy.deepcopy(grid)
                temp[row][col] = value
                sums = sum_row_col_diag(size,temp,row,col)

                if(validMove(sums,row_sums,col_sums,diag_sums,row,col,size)):

                        grid[row][col] = value

                        assignedCheck = assignedNew(size,grid,row,col)


                        if(assignedCheck[0] == True):
                                if( sums[0] != row_sums[row] ):
                                        grid[row][col] = -1
                                        index = stackDomainIndex.pop()
                                        stackDomainIndex.push(index + 1)
                                        continue

                        if(assignedCheck[1] == True):
                                if(sums[1] != col_sums[col]):
                                        grid[row][col] = -1
                                        index = stackDomainIndex.pop()
                                        stackDomainIndex.push(index + 1)
                                        continue

                        if(row == col):
                                if(assignedCheck[2] == True):
                                        if(sums[2] != diag_sums[0]):
                                                grid[row][col] = -1
                                                index = stackDomainIndex.pop()
                                                stackDomainIndex.push(index + 1)
                                                continue

                        if(row == size - col - 1):
                                if(assignedCheck[3] == True):
                                        if(sums[3] != diag_sums[1]):
                                                grid[row][col] = -1
                                                index = stackDomainIndex.pop()
                                                stackDomainIndex.push(index + 1)
                                                continue

                        if(counterVariables < len(variableIndexes) - 1 ):

                                counterVariables+= 1
                                firstVariable = variableIndexes[counterVariables]
                                stackVariables.push(firstVariable)
                                firstRow = firstVariable[0]
                                firstCol = firstVariable[1]
                                minValRow = 0
                                minValCol = 0
                                minValDiagOne = 0
                                minValDiagTwo = 0
                                for i in range(0,size):
                                        if(grid[firstRow][i] != -1):
                                                minValRow += grid[firstRow][i]

                                        if(grid[i][firstCol] != -1):
                                                minValCol += grid[i][firstCol]

                                        if(grid[firstRow][i] == -1):
                                                if(i == firstCol):
                                                        minValRow += 0
                                                else :
                                                        minValRow += 9

                                        if(grid[i][firstCol] == -1):
                                                if(i == firstRow):
                                                        minValCol += 0
                                                else:
                                                        minValCol += 9

                                        if(grid[i][i] != -1):
                                                minValDiagOne += grid[i][i]
                                        if(grid[i][size - i -1] != -1):
                                                minValDiagTwo += grid[i][size - i - 1]
                                        if(grid[i][i] == -1):
                                                if(i == firstRow and i == firstCol):
                                                        minValDiagOne += 0
                                                else:
                                                        minValDiagOne += 9
                                        if(grid[i][size - i -1] == -1):
                                                if( i == firstRow and (size - i - 1) == firstCol):
                                                        minValDiagTwo += 0
                                                else :
                                                        minValDiagTwo += 9

                                lowLimitRow = row_sums[firstRow] - minValRow
                                lowLimitCol = col_sums[firstCol] - minValCol
                                lowLimitDiagOne = diag_sums[0] - minValDiagOne
                                lowLimitDiagTwo = diag_sums[1] - minValDiagTwo
                                if(firstRow == firstCol and firstRow == size - firstCol -1):
                                        startIndex = max([lowLimitRow,lowLimitCol,lowLimitDiagOne,lowLimitDiagTwo])
                                elif(firstRow == firstCol):
                                        startIndex = max([lowLimitRow,lowLimitCol,lowLimitDiagOne])
                                elif(firstRow == size - firstCol - 1):
                                        startIndex = max([lowLimitRow,lowLimitCol,lowLimitDiagTwo])
                                else:
                                        startIndex = max([lowLimitRow,lowLimitCol])
                                if(startIndex < 0):
                                        startIndex = 0
                                if(startIndex < 0):
                                        startIndex = 0

                                stackDomainIndex.push(startIndex)

                else:

                        stackDomainIndex.pop()
                        prev = stackVariables.pop()
                        grid[prev[0]][prev[1]] = -1

                        if(stackDomainIndex.isEmpty()):

                                print(False)
                                return

                        new_index = stackDomainIndex.pop() + 1
                        stackDomainIndex.push(new_index)
                        counterVariables-=1

                        continue

                check = allAssigned(size,grid)

        if(checkComplete(size,grid,row_sums,col_sums,diag_sums)):

                print(True)
                for i in range(0,size):
                        for j in range(0,size):
                                print(grid[i][j]),
                        print
                return

        print(False)
        return





def assignedNew(size,grid,row,col):
        result = [True,True,True,True]

        for i in range(0,size):
                if(grid[row][i] == -1):
                        result[0] = False
                if(grid[i][col] == -1):
                        result[1] = False
                if(grid[i][i] == -1):
                        result[2] = False
                if(grid[i][size - i -1] == -1):
                        result[3] = False
        return result

def sum_row_col_diag(size,grid,row,col):
        result_row = 0
        result_col = 0
        result_diag = 0
        result_diag_second = 0
        for i in range(0,size):
                if(grid[row][i] != -1):
                        result_row += grid[row][i]
                if(grid[i][col] != -1):
                        result_col += grid[i][col]
                if(grid[i][i] != -1):
                        result_diag += grid[i][i]
                if(grid[i][size - i - 1] != -1):
                        result_diag_second += grid[i][size - i - 1]

        return [result_row,result_col,result_diag,result_diag_second]


def allAssigned(size,grid):

        for row in range(0,size):
                for col in range(0,size):
                        if(grid[row][col] == -1):
                                return False
        return True

#checks if assignment is correct
def checkComplete(size,grid,row_sums,col_sums,diag_sums):

        actual_row_sums = [0]*size
        actual_col_sums = [0]*size
        actual_diag_sums = [0]*2
        #current_row_sum = 0
        current_diag_sum_first = 0
        current_diag_sum_second = 0
        for row in range(0,size):
                for col in range(0,size):
                        actual_row_sums[row] += grid[row][col]
                        actual_col_sums[col] += grid[row][col]
                        if(row == col):
                                actual_diag_sums[0] += grid[row][col]
                        if(row == (size - col - 1)):
                            actual_diag_sums[1] += grid[row][col]
        return (actual_row_sums == row_sums) and (actual_col_sums == col_sums) and (actual_diag_sums == diag_sums)

#checks if a move
def validMove(check_sum,row_sums,col_sums,diag_sums,row,col,size):

        if(check_sum[0] > row_sums[row]):
                return False
        if(check_sum[1] > col_sums[col]):
                return False
        if(row == col):
                if(check_sum[2] > diag_sums[0]):
                        return False
        if(row == (size - col - 1)):
                if(check_sum[3] > diag_sums[1]):
                        return False
        return True



def print_result(grid):
        if grid is None:
                print 'False'
        else:
                print 'True'
                for i in xrange(len(grid)):
                        grid_str = [str(x) for x in grid[i]]
                        print ' '.join(grid_str)





if __name__ == '__main__':
        filename = sys.argv[1]
        grid = read_input(filename)
        print_result(grid)
