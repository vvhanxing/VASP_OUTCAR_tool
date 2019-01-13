import OutcarFinder3 as OutcarFinder


OutcarFinder.StartFinder()                #you must first have this line to initialization

for key in  OutcarFinder.outcar_dir:
    
    OutcarFinder.PlotConvergenceLine(key)
    OutcarFinder.OUT2XYZ(key)

#print(OutcarFinder.outcar_dir)




