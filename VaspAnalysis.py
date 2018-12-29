import OutcarFinder

OutcarFinder.StartFinder()                #you must first have this line to initialization

print(OutcarFinder.outcar_dir)

OutcarFinder.PlotConvergenceLine("OUTCAR")

OutcarFinder.PlotConvergenceLine("OUTCAR_C")


