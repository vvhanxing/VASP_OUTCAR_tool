import os
import matplotlib.pyplot as plt

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
            energy_without_entropy = []   
        
            #line_cont = 0
            for line in outcar_file.readlines() :

            

                if "energy  without entropy" in line :
                    print("energy  without entropy=  " , line[30:45])
                    energy_without_entropy.append( float (line[30:45]))
                
                
                
            
                if "General timing" in line :
                    print("YES,General timing")

                outcar_info["energy_without_entropy"] = energy_without_entropy
                outcar_dir[file_name] = outcar_info
            
            outcar_file.close()
        
            print()

#print(outcar_dir)
    print("-------------------------------------------------------")
    print()
    outcar_dir_key = [] 
    for key in outcar_dir:
    
        print (   key  ,"energy_without_entropy =", outcar_dir[key]["energy_without_entropy"][-1]   )
    
        outcar_dir_key.append(key)


    print("\n\n\n"+"Analysis",outcar_dir_key,"completed !")
    #input()
    

#------------------------------------------------------------------

def PlotConvergenceLine(OutcarName):
    x1=range(0,len(outcar_dir[OutcarName]["energy_without_entropy"]))
    y1=outcar_dir[OutcarName]["energy_without_entropy"]
    plt.plot(x1,y1,label='Line',linewidth=2,color='r',marker='o',markerfacecolor='yellow',markersize=6)  
    plt.xlabel('Step') 
    plt.ylabel('Energy') 
    plt.title('Energy convergence steps = '+str(len(outcar_dir[OutcarName]["energy_without_entropy"]))) 
    plt.legend() 
    plt.show() 



