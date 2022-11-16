import WWSolver
import os

# Create an instance of the solver
solver = WWSolver.WWSolver()

# Load test world
file_path = "test_input.txt"
 
#check if file is present
if os.path.isfile(file_path):
  #open text file in read mode
  text_file = open(file_path, "r")

  #read whole file to a string
  world_text = text_file.read()
  solver.loadWorld(world_text)

  #close file
  text_file.close()

solver.solve()
solver.checkPrint()