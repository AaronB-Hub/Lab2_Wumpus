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
    print("Known Map")
    print(self.agent.knowledge)
    print("Predicted Map")
    print(self.agent.prediction)
    print()

  # Agent inner class
  class agent:

     # Constructor of inner class
    def __init__(self, WWSolver):
        truemap = copy.deepcopy(WWSolver.worldmap)
        #print("LENGTH WorldMap" + str(len(truemap)))
        self.last_moves = {}
        self.predicted_moves = {}
        self.knowledge = {}
        self.prediction = {}
        self.best_moves = {}
        for j in range(len(truemap)):
            for i in range(len(truemap[j])):
                self.position = [int(j), int(i)] #The position of the cell is defined here.
                self.predict = ''
                self.right = True
                self.left = True
                self.up = True
                self.down = True
                self.gold = False
                self.length_map = len(copy.deepcopy(WWSolver.worldmap))
                print("Start!")
                self.checkSquare(WWSolver.world)
        print("Predicted Moves: \n" + str(self.predicted_moves))
        print("Best Moves: \n" + str(self.best_moves))        

    # Methods of inner class
    def checkSquare(self, world):
        x = self.position[0]
        y = self.position[1]
        key = (x,y)
        print(key)
        if key in world:
            features = world[(self.position[0],self.position[1])]
            if features == 'E':
                print("The agent's current position is at " + str(x) + "," + str(y))
                self.knowledge[(x,y)] = features
                self.prediction[(x,y)] = features
                #solver = WWSolver.printAgentMaps(self.WWSolver.worldmap)
                
                if x == 0 and y == 0:
                    self.last_moves[(x,y)] = features
                    self.predicted_moves[(x,y)] = features
                    if (self.right):
                        self.position[0] += 1
                        self.start_moving(self.position[0], self.position[1], self.length_map, world)
                    if (self.down):
                        self.position[1] += 1
                        self.start_moving(self.position[0], self.position[1], self.length_map, world)
                elif x < self.length_map and y < self.length_map:
                    self.start_moving(self.position[0], self.position[1], self.length_map, world)
                        
                #print("Predicted Moves: \n" + str(self.predicted_moves))
                #print("Best Moves: \n" + str(self.best_moves))
                    #print("last moves " + str(self.last_moves))    
                        
                    #elif features == 'P':
                        
                    #elif features == 'B/S':
                        
                    #elif features == 'W':
                        
                    #elif features == 'G/B':

            else:
                self.knowledge[(x,y)] = features
                self.prediction[(x,y)] = features
                #solver = WWSolver.printAgentMaps(self.WWSolver.worldmap)
                
                if x == 0 and y == 0:
                    self.last_moves[(x,y)] = features
                    self.predicted_moves[(x,y)] = features
                    if (self.right):
                        self.position[0] += 1
                        self.start_moving(self.position[0], self.position[1], self.length_map, world)
                    if (self.down):
                        self.position[1] += 1
                        self.start_moving(self.position[0], self.position[1], self.length_map, world)
                elif x < self.length_map and y < self.length_map:
                    self.start_moving(self.position[0], self.position[1], self.length_map, world)
                        
                
                print("Features at " + str(x) + "," + str(y) + " are: " + features)
                self.knowledge[(x,y)] = features
                self.prediction[(x,y)] = features
        else:
            print("No features at " + str(x) + "," + str(y))

    def shoot(self, world, direction):
      match direction:
        case "U":
          #Shoot up - look for Wumpus (+) to self.position[1]
        case "D":
          #Shoot down - look for Wumpus (-) to self.position[1]
        case "R":
          #Shoot right - look for Wumpus (+) to self.position[0]
        case "L":
          #Shoot left - look for Wumpus (-) to self.position[0]

    def moveRight(self, world):
        self.right = False
        self.position[0] += 1
        #self.checkSquare(world)
    
    def moveLeft(self, world):
        self.left = False
        self.position[0] -= 1
        #self.checkSquare(world)
    
    def moveUp(self, world):
        self.up = False
        self.position[1] += 1
        #self.checkSquare(world)
    
    def moveDown(self, world):
        self.down = False
        self.position[1] -= 1
        #self.checkSquare(world)
        
    def move(self, world):
        if(self.right==False):
            self.right = True
            self.moveLeft(world)
        elif(self.left==False):
            self.left = True
            self.moveRight(world)
        elif(self.up==False):
            self.up = True
            self.MoveDown(world)
        elif(self.down==False):
            self.down = True
            self.moveUp(world)
            
            
    def start_moving(self, pos0, pos1, length_map, world):
        key = (pos0, pos1)
        if key in world:
            features = world[(pos0,pos1)]
            temp_xR = pos0 + 1# Right => +1
            temp_xD = pos1 + 1# Down => +1
            temp_xU = pos1 - 1# Up => -1
            temp_xL = pos0 - 1# Left => -1
            if features == '':
                self.best_moves[(pos0,pos1)] = features
            elif features == 'B':
                self.predicted_moves[(pos0,pos1)] = features
                self.best_moves[(pos0,pos1)] = features
                if temp_xR < length_map and temp_xR >= 0:
                    pos0 += 1
                    temp_xR -= 1
                    key = (pos0, pos1)
                    if key in world:
                        features = world[(pos0, pos1)]
                    else:
                        features = ''
                    predict = 'P'
                    if features == predict:
                        pos0 -= 1
                        self.predicted_moves[(pos0,pos1)] = predict
                        self.move(world)
                    elif features == '':
                        self.best_moves[(pos0,pos1)] = features 
                if temp_xD < length_map and temp_xD >= 0:
                    pos1 += 1
                    temp_xD -= 1
                    key = (pos0, pos1)
                    if key in world:
                        features = world[(pos0, pos1)]
                    else:
                        features = ''
                    predict = 'P'
                    if features == predict:
                        pos1 -= 1
                        self.predicted_moves[(pos0,pos1)] = predict
                        self.move(world)
                    elif features == '':
                        self.best_moves[(pos0,pos1)] = features
                if temp_xU < length_map and temp_xU >= 0:
                    pos1 -= 1
                    temp_xU -= 1
                    key = (pos0, pos1)
                    if key in world:
                        features = world[(pos0, pos1)]
                    else:
                        features = ''
                    predict = 'P'
                    if features == predict:
                        pos1 += 1
                        self.predicted_moves[(pos0,pos1)] = predict
                        self.move(world)
                    elif features == '':
                        self.best_moves[(pos0,pos1)] = features
                if temp_xL < length_map and temp_xL >= 0:
                    pos0 -= 1
                    key = (pos0, pos1)
                    if key in world:
                        features = world[(pos0, pos1)]
                    else:
                        features = ''
                    predict = 'P'
                    if features == predict:
                        pos0 += 1
                        self.predicted_moves[(pos0,pos1)] = predict
                        self.move(world)
                    elif features == '':
                        self.best_moves[(pos0,pos1)] = features
            elif features == 'S' or features == 'B/S':
                self.predicted_moves[(pos0,pos1)] = features
                self.best_moves[(pos0,pos1)] = features
                if temp_xR < length_map and temp_xR >= 0:
                    pos0 += 1
                    temp_xR -= 1
                    key = (pos0, pos1)
                    if key in world:
                        features = world[(pos0, pos1)]
                    else:
                        features = ''
                    predict = 'W'
                    if features == predict:
                        pos0 -= 1
                        self.predicted_moves[(pos0,pos1)] = predict
                        self.move(world)
                    elif features != predict and features == 'P':
                        pos0 -= 1
                        self.predicted_moves[(pos0,pos1)] = predict
                        self.move(world)
                    elif features != predict and 'G' in features:
                        self.best_moves[(pos0,pos1)] = features
                        self.predicted_moves[(pos0,pos1)] = features
                        self.gold = True
                    elif features == '':
                        self.best_moves[(pos0,pos1)] = features
                if temp_xD < length_map and temp_xD >= 0:
                    pos1 += 1
                    temp_xD -= 1
                    key = (pos0, pos1)
                    if key in world:
                        features = world[(pos0, pos1)]
                    else:
                        features = ''
                    predict = 'W'
                    if features == predict:
                        pos1 -= 1
                        self.predicted_moves[(pos0,pos1)] = predict
                        self.move(world)
                    elif features != predict and features == 'P':
                        pos1 -= 1
                        self.predicted_moves[(pos0,pos1)] = predict
                        self.move(world)
                    elif features != predict and 'G' in features:
                        self.best_moves[(pos0,pos1)] = features
                        self.predicted_moves[(pos0,pos1)] = features
                        self.gold = True
                    elif features == '':
                        self.best_moves[(pos0,pos1)] = features
                if temp_xU < length_map and temp_xU >= 0:
                    pos1 -= 1
                    temp_xU -= 1
                    key = (pos0, pos1)
                    if key in world:
                        features = world[(pos0, pos1)]
                    else:
                        features = ''
                    predict = 'W'
                    if features == predict:
                        pos1 -= 1
                        self.predicted_moves[(pos0,pos1)] = predict
                        self.move(world)
                    elif features != predict and features == 'P':
                        pos1 -= 1
                        self.predicted_moves[(pos0,pos1)] = predict
                        self.move(world)
                    elif features != predict and 'G' in features:
                        self.best_moves[(pos0,pos1)] = features
                        self.predicted_moves[(pos0,pos1)] = features
                        self.gold = True
                    elif features == '':
                        self.best_moves[(pos0,pos1)] = features
                if temp_xL < length_map and temp_xL >= 0:
                    pos0 -= 1
                    key = (pos0, pos1)
                    if key in world:
                        features = world[(pos0, pos1)]
                    else:
                        features = ''
                    predict = 'W'
                    if features == predict:
                        pos0 += 1
                        self.predicted_moves[(pos0,pos1)] = predict
                        self.move(world)
                    elif features != predict and features == 'P':
                        pos0 += 1
                        self.predicted_moves[(pos0,pos1)] = predict
                        self.move(world)
                    elif features != predict and 'G' in features:
                        self.best_moves[(pos0,pos1)] = features
                        self.predicted_moves[(pos0,pos1)] = features
                        self.gold = True
                    elif features == '':
                        self.best_moves[(pos0,pos1)] = features
        else:
            features = ''
            self.best_moves[(pos0,pos1)] = features
                    
