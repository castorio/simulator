import random
import math
import pygame
import sys


width = 480
height = 560
totWidth = int(width/5)
totHeight = int(height/5)
startingspecies=5
mutationchance=0.0005
topStrength = 0
minStrength = 0
topLifeLength = 0
minLifeLength = 0
topChildLength = 0
minChildLength = 0
topAging = 0
minAging = 0
topTakeover = 0
minTakeover = 0
topDifference = 0
minDifference = 0
topLifeDifference = 0
minLifeDifference = 0
takeover = 0.08 #hoger nummer, minder takeovers.. 0: elke takeover werkt. max: 0.5/difference + 0.1
difference = 50 #hoger nummer, kleiner verschil in mutaties!
framerate = 15
lifeDifference = 5
lifeLength = 100
childLength = 20
aging = 0.8
strength = 0
debugging=0
nChildren = 0

if debugging:
  framerate=5
  startingspecies=2
  width=120
  height=240
  totWidth=12
  totHeight=24

def r():
  return random.randint(0,255)
    
class Species(object):
  changed=0
  life=0
  dead=0
  killed=0
  def __init__(self, strength, lengthOfLife, aging, childLength, takeover, difference, lifeDifference, color=(0,0,0), noMutation=0, dead=0, child=-1):
    if noMutation:
      self.color=color
      self.strength = strength
      self.lengthOfLife=lengthOfLife
      self.aging = aging
      self.takeover = takeover
      self.difference = difference
      self.lifeDifference = lifeDifference
      self.dead=dead
      if child >-1 and self.killed==0:
        self.child=childLength
      else:
        self.child=-1
      self.childLength=childLength
      self.killed=0
    else:
      self.color=(r(),r(),r())
      self.difference = difference+int((random.random()-0.5)*5)
      self.lifeDifference = lifeDifference+int((random.random()-0.5)*(self.difference/10))
      self.strength = strength-((random.random()-0.5)/self.difference)
      self.lengthOfLife = lengthOfLife+int((random.random()-0.5)*self.lifeDifference)
      self.aging = aging-((random.random()-0.5)/self.difference*4)
      self.takeover = takeover-((random.random()-0.5)/(self.difference*400))
      self.childLength = childLength+int((random.random()-0.5)*(self.lifeDifference/2))
      if child>-1 and self.killed==0:
        self.child=self.childLength
      else:
        self.child=-1
      self.killed=0
  def stronger(self):
    self.strength = self.strength + (random.random()/self.difference)
    self.color = (r(),r(),r())
    self.dead=0
  def tick(self):
    if self.life > self.lengthOfLife:
      self.dead=1
      self.color=(0,0,0)
    if random.random()<self.aging and self.child<0:
      self.life += 1
    elif random.random()<self.aging and self.child>=0:
      self.child -= 1
  def kill(self, byOtherSpecies=0):
    if self.child>-1:
      self.child=-1
    if byOtherSpecies:
      self.killed=1
    self.dead=1
    self.color=(0,0,0)
    changed=1

class Grid(object):
  matrix = []
  global topRate
  def __init__(self):
    self.matrix=[]
    for y in range(0,totHeight):
      self.matrix.append([])
      for x in range(0,totWidth):
        self.matrix[y].append(Species(strength, lifeLength,aging,childLength,takeover, difference, lifeDifference, (0,0,0),1,1))
    for i in range(0,totWidth*totHeight):
      if random.random()<(float(startingspecies)/float(totWidth*totHeight)):
        self.matrix[int(i/totHeight)][i % totWidth].stronger()
        

  def getXY(self, x, y):
    if x==-1 or x==totWidth or y==-1 or y==totHeight:
      return None
    return self.matrix[y][x]

  def setXY(self, x, y, new):
    if self.matrix[y][x].child != -1:
      self.matrix[y][x].kill()
    if random.random()<mutationchance:
      self.matrix[y][x]=Species(new.strength, new.lengthOfLife, new.aging, new.childLength, new.takeover, new.difference, new.lifeDifference,)
    else:
      self.matrix[y][x]=Species(new.strength, new.lengthOfLife, new.aging, new.childLength, new.takeover, new.difference, new.lifeDifference, new.color, 1)
  
  def mutate(self, x, y, divider=200):
    if random.random()<mutationchance/divider:
      if self.matrix[y][x].child != -1:
        self.matrix[y][x].kill()
      self.matrix[y][x]=Species(self.matrix[y][x].strength, self.matrix[y][x].lengthOfLife, self.matrix[y][x].aging, self.matrix[y][x].childLength, self.matrix[y][x].takeover, self.matrix[y][x].difference, self.matrix[y][x].lifeDifference)

  def birth(self, x, y):
    if random.random()<mutationchance/1:
      self.matrix[y][x]=Species(self.matrix[y][x].strength, self.matrix[y][x].lengthOfLife, self.matrix[y][x].aging, self.matrix[y][x].childLength, self.matrix[y][x].takeover, self.matrix[y][x].difference, self.matrix[y][x].lifeDifference,(0,0,0), 0,0,1)
    else:
      self.matrix[y][x]=Species(self.matrix[y][x].strength, self.matrix[y][x].lengthOfLife, self.matrix[y][x].aging, self.matrix[y][x].childLength, self.matrix[y][x].takeover, self.matrix[y][x].difference, self.matrix[y][x].lifeDifference,self.matrix[y][x].color, 1,0,1)
    
    
mainGrid = Grid()
def Tick():
  global topStrength
  global topChildLength
  global topLifeLength
  global topAging
  global topTakeover
  global topDifference
  global topLifeDifference
  global minStrength
  global minChildLength
  global minLifeLength
  global minAging
  global minDifference
  global minLifeDifference
  global minTakeover
  global nChildren
  tmpS = mainGrid.getXY(0,0).strength
  tmpC = mainGrid.getXY(0,0).childLength
  tmpL = mainGrid.getXY(0,0).lengthOfLife
  tmpA = mainGrid.getXY(0,0).aging
  tmpT=mainGrid.getXY(0,0).takeover
  tmpD=mainGrid.getXY(0,0).difference
  tmpLD=mainGrid.getXY(0,0).lifeDifference
  tmpmS = mainGrid.getXY(0,0).strength
  tmpmC = mainGrid.getXY(0,0).childLength
  tmpmL = mainGrid.getXY(0,0).lengthOfLife
  tmpmA=mainGrid.getXY(0,0).aging
  tmpmT=mainGrid.getXY(0,0).takeover
  tmpmD=mainGrid.getXY(0,0).difference
  tmpmLD=mainGrid.getXY(0,0).lifeDifference
  nChildren = 0
  for y in range(0,totHeight):
    for x in range(0,totWidth):
      d=mainGrid.getXY(x,y)
      d1=mainGrid.getXY(x+1,y)
      d2=mainGrid.getXY(x,y-1)
      d3=mainGrid.getXY(x-1,y)
      d4=mainGrid.getXY(x,y+1)
      if d.strength > tmpS:
        tmpS=d.strength
      if d.childLength < tmpC:
        tmpC=d.childLength
      if d.lengthOfLife > tmpL:
        tmpL=d.lengthOfLife
      if d.aging < tmpA:
        tmpA=d.aging
      if d.takeover > tmpT:
        tmpT=d.takeover
      if d.difference > tmpD:
        tmpD=d.difference
      if d.lifeDifference > tmpLD:
        tmpLD=d.lifeDifference
        
      if d.strength < tmpmS:
        tmpmS=d.strength
      if d.childLength > tmpmC:
        tmpmC=d.childLength
      if d.lengthOfLife < tmpmL:
        tmpmL=d.lengthOfLife
      if d.aging > tmpmA:
        tmpmA=d.aging
      if d.difference < tmpmD:
        tmpmD=d.difference
      if d.takeover < tmpmT:
        tmpmT=d.takeover
      if d.lifeDifference < tmpmLD:
        tmpmLD=d.lifeDifference
      if d.child != -1:
        nChildren += 1
      d.tick()
      for dirc in range(1,5):
        if d.changed==0:
          if random.random() < 0.25:
            if dirc==1:
              
              if x==totWidth-1:
                break
              elif d.dead and d1.dead==0 and (d.strength != d1.strength or d.killed == 0):
                if d.strength==d1.strength and d.killed==0:
                  mainGrid.setXY(x,y,d1)
                  mainGrid.birth(x,y)
                else:
                  mainGrid.setXY(x,y,d1)
              elif d.dead==0 and d1.dead and (d.strength != d1.strength or d1.killed == 0):
                if d.strength==d1.strength and d.killed==0:
                  mainGrid.setXY(x+1,y,d)
                  mainGrid.birth(x+1,y)
                else:
                  mainGrid.setXY(x+1,y,d)
              elif d.child == -1 and d1.child != -1 and d.color != d1.color and d.strength != d1.strength:
                d1.kill(1)
              elif d1.child == -1 and d.child != -1 and d.color != d1.color and d.strength != d1.strength:
                d.kill(1)
              elif d.strength > d1.strength and d.color != d1.color and d.strength != d1.strength:
                if ((random.random()/10)+(d.strength-d1.strength))>d.takeover:
                  d1.kill(1)
              elif d.strength < d1.strength and d.color != d1.color and d.strength != d1.strength:
                if ((random.random()/10)+(d1.strength-d.strength))>d1.takeover:
                  d.kill(1)
              
            elif dirc==2:
              if y==0:
                break
              elif d.dead and d2.dead==0 and (d.strength != d2.strength or d.killed == 0):
                if d.strength==d2.strength and d.killed==0:
                  mainGrid.setXY(x,y,d2)
                  mainGrid.birth(x,y)
                else:
                  mainGrid.setXY(x,y,d2)
              elif d.dead==0 and d2.dead and (d.strength != d2.strength or d2.killed == 0):
                if d.strength==d2.strength and d.killed==0:
                  mainGrid.setXY(x,y-1,d)
                  mainGrid.birth(x,y-1)
                else:
                  mainGrid.setXY(x,y-1,d)  
              elif d.child == -1 and d2.child != -1 and d.color != d2.color and d.strength != d2.strength:
                d2.kill(1)
              elif d2.child == -1 and d.child != -1 and d.color != d2.color and d.strength != d2.strength:
                d.kill(1)
              elif d.strength > d2.strength and d.color != d2.color and d.strength != d2.strength:
                if ((random.random()/10)+(d.strength-d2.strength))>d.takeover:
                  d2.kill(1)
              elif d.strength < d2.strength and d.color != d2.color and d.strength != d2.strength:
                if ((random.random()/10)+(d2.strength-d.strength))>d2.takeover:
                  d.kill(1)
            
            elif dirc==3:
              if x==0:
                break
              elif d.dead and d3.dead==0 and (d.strength != d3.strength or d.killed == 0):
                if d.strength==d3.strength and d.killed==0:
                  mainGrid.setXY(x,y,d3)
                  mainGrid.birth(x,y)
                else:
                  mainGrid.setXY(x,y,d3)
              elif d.dead==0 and d3.dead and (d.strength != d3.strength or d3.killed == 0):
                if d.strength==d3.strength and d.killed==0:
                  mainGrid.setXY(x-1,y,d)
                  mainGrid.birth(x-1,y)
                else:
                  mainGrid.setXY(x-1,y,d)
              elif d.child == -1 and d3.child != -1 and d.color != d3.color and d.strength != d3.strength:
                d3.kill(1)
              elif d3.child == -1 and d.child != -1 and d.color != d3.color and d.strength != d3.strength:
                d.kill(1)
              elif d.strength > d3.strength and d.color != d3.color and d.strength != d3.strength:
                if ((random.random()/10)+(d.strength-d3.strength))>d.takeover:
                  d3.kill(1)
              elif d.strength < d3.strength and d.color != d3.color and d.strength != d3.strength:
                if ((random.random()/10)+(d3.strength-d.strength))>d3.takeover:
                  d.kill(1)
            
            else:
              if y==totHeight-1:
                break
              elif d.dead and d4.dead==0 and (d.strength != d4.strength or d.killed == 0):
                if d.strength==d4.strength and d.killed==0:
                  mainGrid.setXY(x,y,d4)
                  mainGrid.birth(x,y)
                else:
                  mainGrid.setXY(x,y,d4)
              elif d.dead==0 and d4.dead and (d.strength != d4.strength or d4.killed == 0):
                if d.strength==d4.strength and d.killed==0:
                  mainGrid.setXY(x,y+1,d)
                  mainGrid.birth(x,y+1)
                else:
                  mainGrid.setXY(x,y+1,d)
              elif d.child == -1 and d4.child != -1 and d.color != d4.color and d.strength != d4.strength:
                d4.kill(1)
              elif d4.child == -1 and d.child != -1 and d.color != d4.color and d.strength != d4.strength:
                d.kill(1)
              elif d.strength > d4.strength and d.color != d4.color and d.strength != d4.strength:
                if ((random.random()/10)+(d.strength-d4.strength))>d.takeover:
                  d4.kill(1)
              elif d.strength < d4.strength and d.color != d4.color and d.strength != d4.strength:
                if ((random.random()/10)+(d4.strength-d.strength))>d4.takeover:
                  d.kill(1)
        else:        
          d.changed=0
      if d.dead==0:
        mainGrid.mutate(x,y)
  topStrength=tmpS
  topChildLength=tmpC
  topLifeLength=tmpL
  topAging=tmpA
  topTakeover=tmpT
  topDifference=tmpD
  topLifeDifference=tmpLD
  minStrength=tmpmS
  minChildLength=tmpmC
  minLifeLength=tmpmL
  minAging=tmpmA
  minTakeover=tmpmT
  minDifference=tmpmD
  minLifeDifference=tmpmLD
class Text:
  
  def __init__(self, text):
    self.text=text
    self.color=(0,0,0)

class PyMain:
  
  
  text = []
  def __init__(self, width=1040, height=780):
    pygame.init()
    self.width=width
    self.height=height
    self.screen=pygame.display.set_mode((self.width, self.height))
    self.font=pygame.font.SysFont("monospace",15)
    
    
  def mainLoop(self):
    unpaused=1
    global mutationchance
    global takeover
    global difference
    global lifeDifference
    clock = pygame.time.Clock()
    selected = 10
    while 1:
      self.text = []
      pretext = [
        "Best strength: {0}".format(topStrength),
        "Worst strength: {0}".format(minStrength),
        "Longest life length: {0}".format(topLifeLength),
        "Shortest life length: {0}".format(minLifeLength),
        "Shortest child length: {0}".format(topChildLength),
        "Longest child length: {0}".format(minChildLength),
        "Smallest aging chance: {0}".format(topAging),
        "Largest aging chance: {0}".format(minAging),
        "top takover: {0}".format(topTakeover),
        "min takeover: {0}".format(minTakeover),
        "top difference {0}".format(topDifference),
        "min difference: {0}".format(minDifference),
        "top life difference {0}".format(topLifeDifference),
        "min life difference {0}".format(minLifeDifference),
        "mutationchance = {0}".format(mutationchance),
        ""
      ]
      for string in pretext:
        self.text.append(Text(string))
        if pretext.index(string)==selected:
          self.text[pretext.index(string)].color=(0,0,255)
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          sys.exit()
      pressed = pygame.key.get_pressed()
      if pressed[pygame.K_p] and unpaused==1:
        unpaused=0
      elif pressed[pygame.K_p]:
        unpaused=1
      if unpaused:
        Tick()
      if pressed[pygame.K_UP]:
        if selected !=0:
          self.text[selected].color=(0,0,0)
          self.text[selected-1].color=(0,0,255)
          selected= selected-1
      if pressed[pygame.K_DOWN]:
        if selected != len(main.text)-1:
          self.text[selected].color=(0,0,0)
          self.text[selected+1].color=(0,0,255)
          selected=selected+1
      if pressed[pygame.K_r]:
        mainGrid.__init__()
      Cpressed=0
      Vpressed=0
      if pressed[pygame.K_c]:
        Cpressed=1
      if pressed[pygame.K_v]:
        Vpressed=1
      render(Cpressed,Vpressed)
      clock.tick(framerate)
        
def getStats():
  coor = pygame.mouse.get_pos()
  x= coor[0]
  y= coor[1]
  if x<width and y<height:
    blockX = x/(width/totWidth)
    blockY = y/(height/totHeight)
    return mainGrid.getXY(int(blockX), int(blockY))
  else:
    return None
          
def render(showChildren=0, showGrandpas=0):
  pygame.draw.rect(main.screen, (255,255,255),(0,0,main.width, main.height), 0)
  for y in range(0,totHeight):
    for x in range(0,totWidth):
      screenX = (width/totWidth) * x
      screenY = (height/totHeight) * y
      pygame.draw.rect(main.screen, mainGrid.getXY(x,y).color,(screenX-1,screenY-1,width/totWidth, height/totHeight), 0)
  if showChildren:
    for y in range(0,totHeight):
      for x in range(0,totWidth):
        screenX = (width/totWidth) * x
        screenY = (height/totHeight) * y
        if mainGrid.getXY(x,y).child != -1:
          pygame.draw.rect(main.screen, (255,255,255),(screenX-1,screenY-1,width/totWidth, height/totHeight), 0)
  if showGrandpas:
    for y in range(0,totHeight):
      for x in range(0,totWidth):
        screenX = (width/totWidth) * x
        screenY = (height/totHeight) * y
        if mainGrid.getXY(x,y).life+15 > mainGrid.getXY(x,y).lengthOfLife:
          pygame.draw.rect(main.screen, (255,0,0),(screenX-1,screenY-1,width/totWidth, height/totHeight), 0)
  for string in main.text:
    label = main.font.render(string.text, 1,string.color)
    main.screen.blit(label, (width+10,10+20*main.text.index(string)))
  statBlock = getStats()
  if statBlock != None:
    statText = [
      "Strength: {0}".format(statBlock.strength),
      "lengthOfLife: {0}".format(statBlock.lengthOfLife),
      "Aging: {0}".format(statBlock.aging),
      "childlength: {0}".format(statBlock.childLength),
      "difference: {0}".format(statBlock.difference),
      "lifeDifference: {0}".format(statBlock.lifeDifference),
      "takeover: {0}".format(statBlock.takeover),
      "child: {0}".format(statBlock.child),
      "life: {0}".format(statBlock.life)
    ]
    for string in statText:
      label = main.font.render(string, 1,(0,0,0))
      main.screen.blit(label, (width+10,10+len(main.text)*20+20*statText.index(string)))
    pygame.draw.rect(main.screen, statBlock.color,(main.height-50,main.width-50, 50,50),0)
    
    
  pygame.display.update()
   
main = PyMain(width+400, height)
      
main.mainLoop()

