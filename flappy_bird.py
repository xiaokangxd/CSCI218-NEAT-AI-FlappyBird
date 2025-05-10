
import pygame
import neat
import time
import os
import random
pygame.font.init()


# Constant values for win and lose
WIN_WIDTH = 600
WIN_HEIGHT = 800

# Image paths (use full directory path)
BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("C:/Users/surya/Desktop/flappyBird_baseGame/bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("C:/Users/surya/Desktop/flappyBird_baseGame/bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("C:/Users/surya/Desktop/flappyBird_baseGame/bird3.png")))
]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("C:/Users/surya/Desktop/flappyBird_baseGame/pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("C:/Users/surya/Desktop/flappyBird_baseGame/base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("C:/Users/surya/Desktop/flappyBird_baseGame/bg.png")))


STAT_FONT = pygame.font.SysFont("comicsans", 50) # setting the font to display the score

class Bird:
  IMGS = BIRD_IMGS
  MAX_ROTATION = 25  # Tilt of the bird during altitude change 
  ROTATION_VEL = 20  # Rotation on each frame
  ANIMATION_TIME = 5  # Speed at which the bird is animated (wing flapping speed)

  def __init__(self, x, y):
    # initializing some parameters for the bird
    self.x = x
    self.y = y
    self.tilt = 0  # tilt of the birs when jumping up or falling down
    self.tick_count = 0  
    self.vel = 0   #velocity of the bird
    self.height = self.y
    self.image_count = 0
    self.img = self.IMGS[0]

  def jump(self):
    self.vel = -10.5
    self.tick_count = 0  #keep count of when the bird last jumped
    self.height = self.y  #keep track of where the bird jumped from

  #defining the frames to move the bird
  def move(self):
    self.tick_count += 1

    # calculating displacement - number of pixels moved up or down
    # tells us how much the bird moves up or down based on the current velocity
    d = self.vel*self.tick_count + 1.5*self.tick_count**2 
    
    # Moving down more than 16 pixels
    if d >= 16:
      d = 16

    if d < 0:
      d -= 2
    #chaning y position based on the displacement
    self.y = self.y + d

    if d < 0 or self.y < self.height + 50:  # tilt up
      if self.tilt < self.MAX_ROTATION:
        self.tilt = self.MAX_ROTATION

    else:  # tilt down
      if self.tilt > -90:
        self.tilt -= self.ROTATION_VEL

  def draw(self, win):
    self.image_count += 1 # keep track of how many times the frame loop happened

    # Setting bird image to show based on the animation count(gradually resetting bird back to initial position after flapping up)

    if self.image_count < self.ANIMATION_TIME:
      self.img = self.IMGS[0]
    elif self.image_count < self.ANIMATION_TIME*2:
      self.img = self.IMGS[1]
    elif self.image_count < self.ANIMATION_TIME*3:
      self.img = self.IMGS[2]
    elif self.image_count < self.ANIMATION_TIME*4:
      self.img = self.IMGS[1]
    elif self.image_count == self.ANIMATION_TIME*4 + 1:
      self.img = self.IMGS[0]
      self.image_count = 0
    
    if self.tilt <= -80:
      self.img = self.IMGS[1] # displaying img[1] when the bird is going downward
      self.image_count = self.ANIMATION_TIME*2

    # rotating the image around the center
    rotated_image = pygame.transform.rotate(self.img, self.tilt)
    new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center)
    win.blit(rotated_image, new_rect.topleft) 

  def get_mask(self):
    # mask -
    return pygame.mask.from_surface(self.img)

class Pipe:
  # Setting gap between pipes and how fast pipes are moving (because the bakground itself does not move but the objects on the screen are actually moving)
  GAP = 200
  VEL = 5

  def __init__(self, x):
    #initializing the height of the bird
    self.x = x
    self.height = 0

    self.top = 0
    self.bottom = 0
    self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
    self.PIPE_BOTTOM = PIPE_IMG

    self.passed = False
    self.set_height()

  def set_height(self):
    # settting the hieght randomly
    self.height = random.randrange(50, 450)
    # Setting the top of the pipe by calculating the height of the pipe subtracted by the top which would be off screen
    self.top = self.height - self.PIPE_TOP.get_height()
    # Setting the bottom
    self.bottom = self.height + self.GAP

  def move(self):
    # changing x position based on the velocity
    self.x -= self.VEL

  def draw(self, win):
    # Drawing the top and bottom pipes
    win.blit(self.PIPE_TOP, (self.x, self.top))
    win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

  # Defining the collision function using masks instead of hitboxes to detect the necessary pixels in the hitbox
  def collide(self, bird):
    bird_mask = bird.get_mask() # getting the mask for the bird
    #creating the masks for the top and bottom pipes
    top_mask = pygame.mask.from_surface(self.PIPE_TOP)
    bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

    top_offset = (self.x - bird.x, self.top - round(bird.y))
    bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

    #point of collision - returns none if there is no collision
    b_point = bird_mask.overlap(bottom_mask, bottom_offset) 
    t_point = bird_mask.overlap(top_mask, top_offset)

    # Collision checking condition
    if t_point or b_point:
      return True
    return False

# Base image requires a class since the position needs to be reset when the image is pushed out of the screen
class Base():
  VEL = 5
  WIDTH = BASE_IMG.get_width() 
  IMG = BASE_IMG

  def __init__(self, y):
    self.y = y
    self.x1 = 0
    self.x2 = self.WIDTH

  def move(self):
    self.x1 -= self.VEL
    self.x2 -= self.VEL

  def draw(self, win):
    win.blit(self.IMG, (self.x1, self.y))
    win.blit(self.IMG, (self.x2, self.y))

    # Designing the movement of the base using 2 images placed side by side and moving both images simultaneously to look like one continuous image until the first image is moved completely off screen and cycled back as the off screen image on the right
    if self.x1 + self.WIDTH < 0:
      self.x1 = self.x2 + self.WIDTH

    if self.x2 + self.WIDTH < 0:
      self.x2 = self.x1 + self.WIDTH


# Draw background image and bird on top of it 
def draw_window(win, birds, pipes, base, score):
  win.blit(BG_IMG, (0,0))  
  for pipe in pipes:
    # drawing all the pipes
    pipe.draw(win)
    
  text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
  win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

  base.draw(win)
  for  bird in birds:
     bird.draw(win)  # calling the draw method defined in the bird class to draw the bird
  
  pygame.display.update()

# defining the main function for the game
def main(genomes, config):
  nets = []
  ge = []
  birds =  []
  
  for _, g in genomes:
    net = neat.nn.FeedForwardNetwork.create(g, config)
    nets.append(net)
    birds.append(Bird(230,350))
    g.fitness = 0
    ge.append(g)
  
  base = Base(730)
  pipes = [Pipe(600)]
  win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
  clock = pygame.time.Clock()
  score = 0

  run = True
  while run:
    clock.tick(30)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
        pygame.quit()
        quit()

        
    pipe_ind =0
    if len(birds) > 0:
      if len(pipes) > 1 and birds[0].x  > pipes[0].x + pipes[0].PIPE_TOP.get_width():
        pipe_ind = 1
    else:
      run = False
      break
    for x, bird in enumerate(birds):
      ge[x].fitness += 0.1
      bird.move()
      
      output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
      
      if output[0] > 0.5:
        bird.jump()   
    add_pipe = False
    rem = [] 

    for pipe in pipes:
      pipe.move()
      for x, bird in enumerate(birds): # End the run if the bird collides with a pipe
        if pipe.collide(bird):
            ge[x].fitness -= 1
            birds.pop(x)
            nets.pop(x)
            ge.pop(x)
          
          # condition to check if bird passed the pipe to generate a new pipe
        if not pipe.passed and pipe.x < bird.x:
          pipe.passed = True
          add_pipe = True
      
      if pipe.x + pipe.PIPE_TOP.get_width() < 0:
           #pipes.pop(pipes.index(pipe))
        rem.append(pipe)
      pipe.move()

    if add_pipe:
      score += 1
      for g in ge:
        g.fitness += 5
      # creating the new pipe
      pipes.append(Pipe(600))

    # removing the pipes in the remove list
    for r in rem:
      pipes.remove(r)
      
      for x, bird in enumerate(birds):
        # Condition for bird hitting the top of the screen
        if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
          birds.pop(x)
          nets.pop(x)
          ge.pop(x)
  
  
    base.move()
    draw_window(win, birds, pipes, base, score) 

  


def run (config_path):
  config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, 
                        neat.DefaultSpeciesSet, neat.DefaultStagnation, 
                        config_path)
  
  p = neat. Population(config)
  
  p.add_reporter(neat.StdOutReporter(True))
  stats = neat.StatisticsReporter()
  p.add_reporter(stats)
  
  winner = p.run(main,50)

if __name__ == "__main__":
  local_dir = os.path.dirname(__file__)
  config_path = os.path.join(local_dir, "config_file.txt")
  run(config_path)

