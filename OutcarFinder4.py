import os
import matplotlib.pyplot as plt
import numpy as np

outcar_dir = { }

def StartFinder():
    file_list = list(os.listdir())

    print( file_list )
    print("-------------------------------------------------------")
    print()

                                                        
    for file_name in file_list:
    

        if "OUTCAR" in file_name:
    
            print(file_name,"_______________________________________")
    
            print()
        
     
        
            outcar_file = open(file_name,"r")

            outcar_info={ }
            atom_type = []
            atoms_info = []
            energy_without_entropy = []
            outcar_info["general_timing"] = False
        
            #line_cont = 0
            for line in outcar_file.readlines() :

                if "VRHFIN" in line :
                    
                    atom_type.append(line[11:13])
                    print(line[11:13])


                if "ions per type" in line :
                     line=line+" "
                     numbers = []
                     number = ""
                     for s in line[20:]:
                         if s == " " :
                             if number!="":
                                 numbers.append(int(number))

                             number = ""
                         if s != " " and s !="\n":
                             number = number + s
                     print(numbers)
                     atoms_info = list(zip(atom_type,numbers)) 


                    

                    

                if "energy  without entropy" in line :
                    print("energy  without entropy=  " , line[30:45])
                    energy_without_entropy.append( float (line[30:45]))
                
                
                
                
                if "General timing" in line :
                    print("YES,General timing")
                    outcar_info["general_timing"] = True

                    
                outcar_info["atoms_info"] = atoms_info
                outcar_info["energy_without_entropy"] = energy_without_entropy
                outcar_dir[file_name] = outcar_info
            
            outcar_file.close()
        
            print()

#print(outcar_dir)
    print("-------------------------------------------------------")
    print()
    outcar_dir_key = [] 
    for key in outcar_dir:
    
        print (   key  ,"energy_without_entropy ="+str(outcar_dir[key]["energy_without_entropy"][-1]).rjust(20)   )
    
        outcar_dir_key.append(key)


    print("\n\n\n"+"Analysis",outcar_dir_key,"completed !")
    #input()
    

#------------------------------------------------------------------

def PlotConvergenceLine(OutcarName):
    x1=range(0,len(outcar_dir[OutcarName]["energy_without_entropy"]))
    y1=outcar_dir[OutcarName]["energy_without_entropy"]
    plt.plot(x1,y1,label=OutcarName+" General timing: "+str(outcar_dir[OutcarName]["general_timing"]),linewidth=2,color='r',marker='o',markerfacecolor='yellow',markersize=6)
    if len(outcar_dir[OutcarName]["energy_without_entropy"])<12:
        for a, b in zip(x1, y1):  
            plt.text(a, b, b,ha='center', va='bottom', fontsize=8)
    else :
        plt.text(x1[-1], y1[-1], y1[-1],ha='center', va='bottom', fontsize=8)    
    plt.xlabel('Step') 
    plt.ylabel('Energy without entropy') 
    plt.title('Energy convergence steps = '+str(len(outcar_dir[OutcarName]["energy_without_entropy"]))) 
    plt.legend() 
    plt.show() 


#------------------------------------------------------------------
def OUT2XYZ(file_name):
    atoms_info=outcar_dir[file_name]["atoms_info"]

    atoms_type = []
    #print(atoms_info)

    for cont in atoms_info:
        for atom in range(cont[1]):
            atoms_type.append(cont[0])
    #print(atoms_type)


    file = open(file_name,'r')


    where = []
    start=[]
    end=[]

    cont_start = 0
    cont_end = 0


    for line in file.readlines():
        cont_start += 1
        cont_end += 1
        if "TOTAL-FORCE (eV/Angst)"in line:
        
        
            #print(cont_start+1)
            start.append(cont_start+1)

            
        
        if "    total drift:"in line:
            #print(cont_end-2)
            end.append(cont_end-2)

        

    where = list(zip( start,end))
    #print(where)
    file.close()


    fileXYZ = open(file_name.lower()+'.XYZ','w')


    for j,k in where  :
        #print(j,k)
        file = open(file_name,'r')
        #print(str(file.readlines()[j:k]))
        fileXYZ.writelines(str(k-j)+"\n")
        fileXYZ.writelines("something\n")
        cont = 0
        for line in file.readlines()[j:k]:
        
            fileXYZ.writelines(atoms_type[cont]+line[:40]+"\n" )
            cont +=1
        
        file.close()


    fileXYZ.close()
    print(file_name +" to .XYZ finish!")

#-----------------------------------------------------------------

def OUT2PDB(file_name):
    atoms_info=outcar_dir[file_name]["atoms_info"]

    atoms_type = []
    #print(atoms_info)

    for cont in atoms_info:
        for atom in range(cont[1]):
            atoms_type.append(cont[0])
    #print(atoms_type)


    file = open(file_name,'r')

#--------
    where = []
    start=[]
    end=[]
    cont_start = 0
    cont_end = 0
#--------
    vectors_where = []
    vectors_start=[]
    vectors_end=[]
    vectors_cont_start = 0
    vectors_cont_end = 0
#--------
#--------
    length_where = []
    length_start=[]
    length_end=[]
    length_cont_start = 0
    length_cont_end = 0
#--------    

    for line in file.readlines():
        cont_start += 1
        cont_end += 1

        
        if "TOTAL-FORCE (eV/Angst)"in line:

            #print(cont_start+1)
            start.append(cont_start+1)
      
        if "    total drift:"in line:
            #print(cont_end-2)
            end.append(cont_end-2)


#---------
        vectors_cont_start +=1
        vectors_cont_end +=1
        length_cont_start +=1
        length_cont_end += 1
        if "direct lattice vectors"in line:

            #print(cont_start+1)
            vectors_start.append(vectors_cont_start)
            vectors_end.append(vectors_cont_end+3)
        if "length of vectors"in line:

            #print(cont_start+1)
            length_start.append(length_cont_start)
            length_end.append(length_cont_end+1)            



        
#---------
        

    where = list(zip( start,end , vectors_start,vectors_end,length_start,length_end  ))
    #print(where)

#---------


    

    
    #print(where)
    file.close()


    fileXYZ = open(file_name.lower()+'.pdb','w')


    for j,k ,m,n ,s,t in where  :
        #print(j,k)
        
        #print(str(file.readlines()[j:k]))
        fileXYZ.writelines("REMARK   Outcar\n")
        fileXYZ.writelines("REMARK   Outcar\n")


        file = open(file_name,'r')
        line_numbers=[]
        for line in file.readlines()[m:n]:
            line=line+" "
            numbers = []
            number = ""
            #print(line)
            for s1 in line :
                if s1 == " " :
                    if number!="":
                        numbers.append(float(number))
                    number = ""


                if s1 != " " and s1 !="\n":
                    number = number + s1                
            line_numbers.append(numbers) 
        #print("linenumber",line_numbers[:][:3])
        file.close()
        
        file = open(file_name,'r')
        for line in file.readlines()[s:t]:
            angle = get_angle(line_numbers[0][:3] ,line_numbers[1][:3],line_numbers[2][:3]  )
            #print(angle)
            fileXYZ.writelines( "CRYST1  "+line[3:10]+"  "+line[16:23]+"  " +line[29:36]  +"  " +  str("%.2f" %angle[0] )+  "  "+str("%.2f" %angle[1]  )+"  "+str("%.2f" %angle[2] )+ " P1"+"\n" )
        file.close()

        
        fileXYZ.writelines("ORIGX1      1.000000  0.000000  0.000000        0.00000\n" )
        fileXYZ.writelines("ORIGX2      0.000000  1.000000  0.000000        0.00000\n" )
        fileXYZ.writelines("ORIGX3      0.000000  0.000000  1.000000        0.00000\n" )
        file = open(file_name,'r')
        SCALE=1
        for line in file.readlines()[m:n]:
           
            fileXYZ.writelines("SCALE"+str(SCALE)+"    "+ line[45:55]+ line[58:68]+line[71:81]+"        0.00000"+"\n" )
            SCALE +=1
        file.close()


           
        cont = 0
        b=[" ","  "]
        file = open(file_name,'r')
        for line in file.readlines()[j:k]:
        
            fileXYZ.writelines( "ATOM  "   +str(cont+1).center(5) + "  "+atoms_type[cont].center(4)+" MOL         "+line[3:11]+ line[16:24]+line[29:37] +"\n" )
            cont +=1
        file.close()
        
        fileXYZ.writelines("TER"+str(k-j+1).rjust(7)+"\n")
        fileXYZ.writelines("END\n")
        


    fileXYZ.close()
    print(file_name +" to .PDB finish!")

def get_angle(a1,b1,c1):
    a=np.array(a1)
    b=np.array(b1)
    c=np.array(c1)
    x=np.arccos((a.dot(b))/( np.sqrt (a.dot(a))*np.sqrt (b.dot(b)) ))*(180/np.pi)
    y=np.arccos((b.dot(c))/( np.sqrt (b.dot(b))*np.sqrt (c.dot(c)) ))*(180/np.pi)
    z=np.arccos((a.dot(c))/( np.sqrt (a.dot(a))*np.sqrt (c.dot(c)) ))*(180/np.pi)
    return [y, z, x ]



