
from string import ascii_lowercase
import sys

def draw(s, data):
    for i in range(s):
        for j in range(s):
            if data[i][j] == 0:
                sys.stdout.write("@")
            elif data[i][j] == 1:
                sys.stdout.write("~")   
            else:
                sys.stdout.write(chr(data[i][j] % 26 + ord('A')))
        print

def drawSolved(s, data2):
    for i in range(s):
        for j in range(s):
            value = data2[i][j]
            if data2[i][j] == 200 or data2[i][j] == 201 or data2[i][j] == 202 \
               or data2[i][j] == 210 or data2[i][j] == 211 or data2[i][j] == 212 \
               or data2[i][j] == 220 or data2[i][j] == 221 or data2[i][j] == 222 \
               or data2[i][j] == 230 or data2[i][j] == 231 or data2[i][j] == 232:
                for c in ascii_lowercase:               
                    sys.stdout.write(value + chr('A')) 
        print
        
def solve(n):   
    sides = 2**n   #compute the sides
    d = []  #list
    for i in range(sides):
                d.append([0] * sides)
    d[int(missing_x)][int(missing_y)] = 1   #start here     
    draw(sides, d)                      #draw the orginal 
    raw_input()
    recursiveSolve([0, sides-1], [0, sides-1], sides, d)
    #drawSolved(sides, d)               #draw the new one

#r = row, c = col, s = side, d = list
def recursiveSolve(r, c, s, d):
    #our base case is a 2x2 matrix  
    #take the row and take the max minus the low    
    #see if 0,0 is filled, if so fill the rest
    if s == 0:
        sys.stdout.write("Can't solve! Too small")
        return
    
    elif r[1] - r[0] == 0:    
        return 
    
    #alright, now lets take the next case on
    #we are gonna divide the square into 4, and indentify them as f1-f4
    #we then are gonna see outta the rows and columbs, where the X is located
    #from there, we will call the fucntion reservisely on each four respectively
    #it should solve and print our answer
    #heres for hoping for the best....
    
    else:  
        maxR = r[1]
        minR = r[0]
        maxC = c[1]
        minC = c[0]

        f1 = False
        f2 = False
        f3 = False
        f4 = False

        #alright, so currently this says there is nothing in our rows
        #Now lets find our values we need

        #fun fact, the // is different that /
        subMaxR = minR + (maxR - minR) // 2
        subMinR = subMaxR + 1
        subMaxC = minC + (maxC - minC) // 2
        subMinC = subMaxC + 1

        #check from lowest to highest + 1, indexing
        for r in range(minR, maxR+1):
            for c in range(minC, maxC+ 1):
                #for these cases, it is true
                if r <= subMaxR and c <= subMaxC:
                    if d[r][c] >= 1:
                       f1 = True
                elif r <= subMaxR and c > subMaxC:
                    if d[r][c] >= 1:
                       f2 = True
                elif r > subMaxR and c <= subMaxC:
                    if d[r][c] >= 1:
                       f3 = True
                elif r > subMaxR and c > subMaxC:
                    if d[r][c] >= 1:
                       f4 = True
    
        if f1:
            d[subMaxR][subMinC] = 200 
            d[subMinR][subMaxC] = 200 
            d[subMinR][subMinC] = 200 
        elif f2: 
            d[subMaxR][subMaxC] = 201 
            d[subMinR][subMaxC] = 201 
            d[subMinR][subMinC] = 201 
        elif f3:
            d[subMaxR][subMaxC] = 202 
            d[subMaxR][subMinC] = 202 
            d[subMinR][subMinC] = 202 
        elif f4:    
            d[subMaxR][subMaxC] = 203 
            d[subMaxR][subMinC] = 203 
            d[subMinR][subMaxC] = 203 

        draw(s, d)
        print (minR-subMaxR), (minC-subMaxC), (subMinR-maxR), (subMinC-maxC)
        raw_input() 
        recursiveSolve([minR, subMaxR], [minC, subMaxC], s, d)
        recursiveSolve([minR, subMaxR], [subMinC, maxC], s, d)
        recursiveSolve([subMinR, maxR], [minC, subMaxC], s, d)
        recursiveSolve([subMinR, maxR], [subMinC, maxC], s, d)

if __name__ == "__main__" :
    print("What is N?")
    n = raw_input()
    missing_x = raw_input()
    missing_y = raw_input()
    
solve(int(n))
