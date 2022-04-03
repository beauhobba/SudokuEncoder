import random 
import numpy as np
import math as math
import multiprocessing 
from multiprocessing import Event

combo_table = {
'E' :55,
'A' :42,
'R' :38,
'I' :38,
'O' :36,
'T' :35,
'N' :28,
'S' :27,
'L' :22,
'C' :18,
'U' :17,
'D' :16,
'P' :16,
'M' :15,
'H' :15,
'G' :12,
'B' :10,
'F' :10,
'Y' :9,
'W' :9,
'K' :8,
'V' :8,
'X' :5,
'Z' :5,
'J' :5,
'Q' :5,
    }

seed = 1 


# rule 1: 9x9 grid
# rule 2: each row must range from 1-9
# rule 3: each number must not be repeated in a single row or column 


# NOW SOME ENCODING RULES 
# The first bits are used for  determining the encoder 

# The first five letters must be all different/ have enough combo unlocks 



def create_dictionary(): 
    v1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    A = []  

    # Brute forces a random solution for all the letters 
    sol_attempts = len(v1)*(len(v1)-1)*(len(v1)-2)
    while(len(A) < sol_attempts):
        l1 = len(v1)
        
        x = random.randint(0, l1-1)
        y = random.randint(0, l1-1)
        z = random.randint(0, l1-1)
        
        val1 = v1[x]
        val2 = v1[y]
        val3 = v1[z]
        
        if(val1 == val2 or val1 == val3 or val2 == val3):
            continue
        else:
            if([val1, val2, val3] in A):
                pass
            else:
                A.append([val1, val2, val3])

    fin_dic = {} 
    count = 0


    # print(A)

    # Creates the dictionary for all the letters 
    for key, val in combo_table.items():
        fin_dic[key] = []
        for i in range(val):
            fin_dic[key].append(A[count])
            count += 1 
            
    return fin_dic 



def check_sudoku_rules(grid, position, number): 
    
    x = position[0]
    y = position[1]


    for i in range(0, 9):
        if(((grid[x, i] == number) and (i != y)) or ((grid[i, y] == number) and (i != x))):
            return True 
        
        
    # now the square check
    x_quad = math.floor((x)/3) 
    y_quad = math.floor((y)/3)
    # print("===")    
    # print("Nu: %s, X %s, y, %s "%(str(number), x, y))
    if(x  < 1):
        return False 
    for i in range(3):
        for j in range(3):
            
            # print("Grid: %s, x_q: %s, y_q: %s"%(grid[x_quad*3+i, y_quad*3+j], x_quad*3+i, y_quad*3+j))
            if(grid[x_quad*3+i, y_quad*3+j] == number and ((x_quad*3+i != x) and (y_quad*3+j != y))):
                return True 
   
               
    return False  
        
    # first check the vertical line
    # second check the horizontal line
    # next check the square 


# Create the grid 

# Preset the random seed 
# sudoku_grid[0, 0] = 1
# sudoku_grid[0, 1] = 2
# sudoku_grid[0, 2] = 3

    
 

def run_sudoku_sol(message, thread_type, flag):
    grid = (9, 9)
    sudoku_grid = np.zeros(grid)

    
    attempt_count = 100000000
    attempt = 0 

    restart = False 


    finished = False 
    

    while(flag.is_set()==False):
        remainder = attempt % 10000
        if(remainder == 0):
            print("Thread:%s  Attempts so far: %s" % (thread_type, str(attempt)))
        
        # print(sudoku_grid)
        # print("+++++++++++++++++")
        fin_dic   = create_dictionary()
        
        og_grid = [0, 0]
        forwards = True 
        
        for char_idx, char in enumerate(list(message)):
            if(restart== True):
                restart = False
                attempt += 1 
                # print("Restarting")
                grid_square = og_grid.copy() 
                break
            
            key_arr = fin_dic[char.capitalize()]

            
            for i, it in enumerate(key_arr):
                
                grid_square = og_grid.copy() 
                
                # if((og_grid[0] >= 1 and og_grid[1] <= 4) or og_grid[0] >= 2 ):
                #     print("Og, %s, IT: %s, GS: %s, char %s,"%(str(og_grid), it, grid_square, char))
                failed = False 
                for val in it: 
                    new_grid = sudoku_grid
                    new_grid[grid_square[0], grid_square[1]] = val
                    
                    res = check_sudoku_rules(new_grid, grid_square, val)
                    if(res == True):
                        failed = True 
                        if(i != len(key_arr)-1):
                            continue
                        else:
                            restart = True   
                            break 
                    
                    if(forwards):
                        grid_square[1] = grid_square[1]+1 
                    else:
                        grid_square[1] = grid_square[1]-1
                        
                    if(grid_square[1] > 8):
            
                        grid_square[1] = 8
                        grid_square[0] = grid_square[0]+1 
                        forwards = False
                    
                    elif(grid_square[1] < 0 and forwards==False):
                        grid_square[1] = 0
                        forwards = True
                        grid_square[1] = grid_square[1]+1 
                    
                    
                if(failed == True):
                    continue    


                sudoku_grid = new_grid
                og_grid = grid_square 


                if(char_idx == len(message)-1):
                    print("Thread: %s - Attempts: %s"%(thread_type, str(attempt)))
                    finished = True
                    flag.set()
                    print(sudoku_grid)
                    print("DONE")
                    return  
                else:
                    break

    if(finished == True):
        print(sudoku_grid)
        flag.set()
        return 
    return 
            
    


# while(flag==False):
if __name__ == '__main__':
    processes = []
    flag = Event()
    for i in range(0,10):
        p = multiprocessing.Process(target=run_sudoku_sol, args=("helloworld", i, flag))
        processes.append(p)
        p.start()
        
    for process in processes:
        process.join()
                

    


