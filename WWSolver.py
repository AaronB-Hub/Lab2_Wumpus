import copy


class WWSolver:
  
  # Attributes


  # Constructor
  def __init__(self):
    self.worldmap = []
    self.world = {}
    # Not yet creating agent object, as the world is empty
    #self.agent = self.agent(self)
 
  
  # Methods
  def loadWorld(self, text):
    #Parse text
    lines = text.splitlines()
    
    size_str = lines[0]
    size_X = int(size_str[-3])
    size_Y = int(size_str[-1])
    size_X += 1
    size_Y += 1
    self.worldmap = [["" for i in range(size_X)] for j in range(size_Y)]

    for i in range(1, len(lines)):
      line = lines[i].split(",")[:-1] if lines[i].split(",")[-1] == '' else lines[i].split(",")
      # NOTE: x and y are switched from normal convention in the provided example, so using that convention here
      x = int(line[1])
      y = int(line[0])
      features = "/".join(line[2::])

      self.world[(x,y)] = features


  def printWorldMap(self):
    print("World Map (True):")
    truemap = copy.deepcopy(self.worldmap)
    for j in range(len(truemap)):
      for i in range(len(truemap[j])):
        key = (i,j)
        if key in self.world:
          truemap[j][i] = self.world[key]
      print(truemap[j])
    print()


  def printAgentMaps(self):
    print("Agent Map (Known):")
    knowmap = copy.deepcopy(self.worldmap)
    for j in range(len(knowmap)):
      for i in range(len(knowmap[j])):
        key = (i,j)
        if key in self.agent.knowledge:
          knowmap[j][i] = self.agent.knowledge[key]
      print(knowmap[j])
    print()
    
    print("Agent Map (Predicted):")
    predmap = copy.deepcopy(self.worldmap)
    for j in range(len(predmap)):
      for i in range(len(predmap[j])):
        key = (i,j)
        if key in self.agent.prediction:
          predmap[j][i] = self.agent.prediction[key]
      print(predmap[j])
    print()


  def solve(self):
    # Create agent object with world details
    self.agent = self.agent(self)


  # This method is for checking and debugging while writing code
  def checkPrint(self):
    self.printWorldMap()
    print(self.world)
    print()
    self.printAgentMaps()
    print(self.agent.knowledge)
    print(self.agent.prediction)
    print()

  # Agent inner class
  class agent:

     # Constructor of inner class
    def __init__(self, WWSolver):
      self.position = [int(0), int(0)]
      self.knowledge = {}
      self.prediction = {}
      print("Start!")
      self.checkSquare(WWSolver.world)

    # Methods of inner class
    def checkSquare(self, world):
      x = self.position[0]
      y = self.position[1]
      key = (x,y)
      if key in world:
        features = world[(self.position[0],self.position[1])]
        print("Features at " + str(x) + "," + str(y) + " are: " + features)
        self.knowledge[(x,y)] = features
      else:
        print("No features at " + str(x) + "," + str(y))

    def moveRight(self, world):
      self.position[0] += 1
      self.checkSquare(world)

    def moveLeft(self, world):
      self.position[0] -= 1
      self.checkSquare(world)
    
    def moveUp(self, world):
      self.position[1] += 1
      self.checkSquare(world)

    def moveDown(self, world):
      self.position[1] -= 1
      self.checkSquare(world)