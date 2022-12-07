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


  def killWumpus(self):
    world = self.world
    # This method is called if the Wumpus is shot
    # Removes Wumpus and all stench from world
    WS_locs = []
    for key,val in world.items():
        if any(("W" in feature) or ("S" in feature) for feature in val):
          WS_locs.append(key)

    for key in WS_locs:
      if len(world[key]) == 1:
        del world[key]
      elif len(world[key]) == 3:
        val = world[key]
        val = val.replace("S", "")
        val = val.replace("W", "")
        val = val.replace("/", "")
        if len(val) == 0:
          del world[key]
        else:
          world[key] = val
      else:
        val = world[key]
        val = val.replace("/S", "")
        val = val.replace("S/", "")
        val = val.replace("/W", "")
        val = val.replace("W/", "")
        world[key] = val

    # Need to also remove Wumpus and Stench from Agent knowledge and predictions
    #self.agent.???

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
        self.WWSolver = WWSolver
        #truemap = WWSolver.worldmap
        #print("LENGTH WorldMap" + str(len(truemap)))
        self.last_moves = {}
        self.predicted_moves = {}
        self.knowledge = {}
        self.prediction = {}
        self.best_moves = {}
        for j in range(len(WWSolver.worldmap)):
            for i in range(len(WWSolver.worldmap[j])):
                self.position = [int(j), int(i)] #The position of the cell is defined here.
                self.predict = ''
                self.right = True
                self.left = True
                self.up = True
                self.down = True
                self.gold = False
                self.length_map = len(WWSolver.worldmap)
                print("Start!")
                self.checkSquare()
        print("Predicted Moves: \n" + str(self.predicted_moves))
        print("Best Moves: \n" + str(self.best_moves)) 
        self.make_move(self.best_moves)       

    # Methods of inner class
    def make_move(self, best_moves):
        world = self.WWSolver.world
        for key,val in best_moves:
            self.position[0] = key
            self.position[1] = val
            print("Agent's new position is on :" + str(key) + ", " + str(val))
            check_key = (key, val)
            if check_key in world:
                feature = world[(key, val)]
                self.shoot(key, val)
                self.knowledge[(key,val)] = feature
                self.prediction[(key,val)] = feature
                if('G' in feature):
                    print("Gold taken")
                    break;

            


    def checkSquare(self):
        world = self.WWSolver.world
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
                        self.start_moving(self.position[0], self.position[1], self.length_map)
                    if (self.down):
                        self.position[1] += 1
                        self.start_moving(self.position[0], self.position[1], self.length_map)
                elif x < self.length_map and y < self.length_map:
                    self.start_moving(self.position[0], self.position[1], self.length_map)
                        
            else:
                self.knowledge[(x,y)] = features
                self.prediction[(x,y)] = features
                #solver = WWSolver.printAgentMaps(self.WWSolver.worldmap)
                
                if x == 0 and y == 0:
                    self.last_moves[(x,y)] = features
                    self.predicted_moves[(x,y)] = features
                    if (self.right):
                        self.position[0] += 1
                        self.start_moving(self.position[0], self.position[1], self.length_map)
                    if (self.down):
                        self.position[1] += 1
                        self.start_moving(self.position[0], self.position[1], self.length_map)
                elif x < self.length_map and y < self.length_map:
                    self.start_moving(self.position[0], self.position[1], self.length_map)
                        
                
                print("Features at " + str(x) + "," + str(y) + " are: " + features)
                self.knowledge[(x,y)] = features
                self.prediction[(x,y)] = features
        else:
            print("No features at " + str(x) + "," + str(y))

    def shoot(self, pos_x, pos_y):
        world = self.WWSolver.world

        # Get agent position
        x = pos_x
        y = pos_y
        W_loc_x = -1
        W_loc_y = -1

        # Get Wumpus position
        for key,val in world.items():
            if any("W" in feature for feature in val):
                W_loc_x = key[0]
                W_loc_y = key[1]

      # Check if Wumpus is shot
      # If so, remove it and all stench from board
        if W_loc_x > 0 and W_loc_y > 0:
            hit = False
            if x == W_loc_x and y > W_loc_y:
                # direction = 'Up'
                hit = True
            elif x == W_loc_x and y < W_loc_y:
                hit = True
                # direction = 'Down'
            elif x > W_loc_x and y == W_loc_y:
                hit = True
                # direction = 'Left'
            elif x < W_loc_x and y == W_loc_y:
                hit = True
                # direction = 'Right'

            if hit:
                self.WWSolver.killWumpus()
                print("Shot the Wumpus")
            else:
                print("You missed your shot!")
        else:
            print("Wumpus has already been shot!!!")

    def moveRight(self):
      #world = self.WWSolver.world
      self.right = False
      self.position[0] += 1
      #self.checkSquare(world)
    
    def moveLeft(self):
      #world = self.WWSolver.world
      self.left = False
      self.position[0] -= 1
      #self.checkSquare(world)
    
    def moveUp(self):
      #world = self.WWSolver.world
      self.up = False
      self.position[1] += 1
      #self.checkSquare(world)
    
    def moveDown(self):
      #world = self.WWSolver.world
      self.down = False
      self.position[1] -= 1
      #self.checkSquare(world)
        
    def move(self):
      #world = self.WWSolver.world
        if(self.right==False):
            self.right = True
            self.moveLeft()
        elif(self.left==False):
            self.left = True
            self.moveRight()
        elif(self.up==False):
            self.up = True
            self.MoveDown()
        elif(self.down==False):
            self.down = True
            self.moveUp()
            
            
    def start_moving(self, pos0, pos1, length_map):
        world = self.WWSolver.world
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
                        self.move()
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
                        self.move()
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
                        self.move()
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
                        self.move()
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
                        self.move()
                    elif features != predict and features == 'P':
                        pos0 -= 1
                        self.predicted_moves[(pos0,pos1)] = predict
                        self.move()
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
                        self.move()
                    elif features != predict and features == 'P':
                        pos1 -= 1
                        self.predicted_moves[(pos0,pos1)] = predict
                        self.move()
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
                        self.move()
                    elif features != predict and features == 'P':
                        pos1 -= 1
                        self.predicted_moves[(pos0,pos1)] = predict
                        self.move()
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
                        self.move()
                    elif features != predict and features == 'P':
                        pos0 += 1
                        self.predicted_moves[(pos0,pos1)] = predict
                        self.move()
                    elif features != predict and 'G' in features:
                        self.best_moves[(pos0,pos1)] = features
                        self.predicted_moves[(pos0,pos1)] = features
                        self.gold = True
                    elif features == '':
                        self.best_moves[(pos0,pos1)] = features
        else:
            features = ''
            self.best_moves[(pos0,pos1)] = features
                    
