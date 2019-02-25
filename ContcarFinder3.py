import os
from decimal import *
import numpy as np
   
try :
    f = open(r"00/CONTCAR","r")
except FileNotFoundError:
    print("please make sure CONTCAR has been renamed POSCAR!")
    f = open(r"00/POSCAR","r")
    CONTCAR_Start = (f.readlines() )
    f.close()
    
else:
    CONTCAR_Start = (f.readlines() )

    f.close()

try :
    f2 = open(r"08/CONTCAR","r")
except FileNotFoundError:
    print("please make sure CONTCAR has been renamed POSCAR!")
    f2 = open(r"08/POSCAR","r")
    CONTCAR_End = (f2.readlines() )
    f2.close()
else:
    CONTCAR_End = (f2.readlines() )

    f2.close()



def getLineElement(Lines):

    

#print(f.readlines()[1:])

    line_numbers=[]
    #print("-------------------------")
    for line in Lines:
        line=line+" "
    

        numbers = []

        number = ""
        #print(line)

        #print("-------------------------")
        for s in line:


        
            if s == " " :
                if number!="":
                    numbers.append(number)
                number = ""


            if s != " " and s !="\n":
                number = number + s
                #print(number)

        line_numbers.append(numbers)    
        
                


    
    return line_numbers
#-----------------------------------------------------------
#print( getLineElement(My_Lines) )
def OUTCAR_position(CONTCAR_Lines):
    for cont , Line in enumerate( getLineElement(CONTCAR_Lines)):
        if "Direct"  in  Line:
            coordinates_position = cont
        if "Cartesian"  in  Line:
            coordinates_position = cont
    #print(coordinates_position )

    Atoms_position =[]



    for line in getLineElement(CONTCAR_Lines)[coordinates_position+1 :]:
    
        Atoms_position_num = []

        if line ==[]:
            break
        else :
            #print(line[:3])
        
            for num in line[:3]:
                Atoms_position_num.append( Decimal(num) )
 
                
        Atoms_position.append(Atoms_position_num)


    #print(Atoms_dynamic)

    return Atoms_position 
#----------------------------------------------------

#-----------------------------------------------------------
#print( getLineElement(My_Lines) )
def OUTCAR_dynamic(CONTCAR_Lines):
    for cont , Line in enumerate( getLineElement(CONTCAR_Lines)):
        if "Direct"  in  Line:
            coordinates_position = cont
        if "Cartesian"  in  Line:
            coordinates_position = cont
    #print(coordinates_position )


    Atoms_dynamic =[]


    for line in getLineElement(CONTCAR_Lines)[coordinates_position+1 :]:
    

        Atoms_dynamic_num = []
        if line ==[]:
            break
        else :
            #print(line[:3])
        

            for dynamic in line[3:]:
                Atoms_dynamic_num.append( dynamic )
                

        Atoms_dynamic.append(Atoms_dynamic_num)

    #print(Atoms_dynamic)

    return Atoms_dynamic 
#----------------------------------------------------
#----------------------------------------------------
def build_CONTCAR( name ,CONTCAR_Start,CONTCAR_End,n,i):
    for cont , Line in enumerate( getLineElement(CONTCAR_Start)):
        if "Direct"  in  Line:
            coordinates_position = cont
        if "Cartesian"  in  Line:
            coordinates_position = cont
    
    f=open(name,"w+")
    f.writelines( CONTCAR_Start[:coordinates_position+1] )
    
    result_array =   np.array(OUTCAR_position(CONTCAR_Start)) - np.array(OUTCAR_position(CONTCAR_End))
                            
    for line_num ,dynamic in zip((  np.array(OUTCAR_position(CONTCAR_Start)) - (result_array*i)/(n+1) ) ,OUTCAR_dynamic(CONTCAR_Start)):
        for num in line_num:
            #print(num)
            f.writelines( str(num )[:16] +"  ")
        f.writelines( "   ".join(dynamic) +"\n")
    f.close()
#----------------------------------------------------
n=7

#print(  (np.array(OUTCAR_position(CONTCAR_End))  - np.array(OUTCAR_position(CONTCAR_Start)))/n  )

for i in range(1,n+1):
    build_CONTCAR( "POSCAR"+"0"+str(i), CONTCAR_Start,CONTCAR_End,n,i)
    if os.path.exists("0"+str(i)):
        pass
    else:
        os.makedirs( "0"+str(i) )
    build_CONTCAR( r"0{}/POSCAR".format(i), CONTCAR_Start,CONTCAR_End,n,i)
    

print("finish")
