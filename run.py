# Lucas Simpson
import AIController, LevelController, Player, Pygame, Camera, Maze, Vector, Graphics, Timer, math
camera = Camera.Camera (Vector.Vector ([0, 0, -20]), Vector.Vector ([0, 0, 1]), Vector.Vector ([0, -1, 0]), Vector.Vector ([0, 0, -5]))
pygame = Pygame.Pygame ()
maze = Maze.Maze ()
world = Graphics.World (camera)
player = Player.Player (maze, 'player')
AI = AIController.AIController (maze, player)

levelController = LevelController.LevelController (maze, player, AI, world)

# timer
timer = Timer.Timer ()
# level Loader
levelController.loadLevel (pygame)
def loop (frame):
    if levelController.playingLevel ():
        if player.alive and AI.notAllDead ():
            # get input, move all bodies and calculate hits
            timer.tick ()
            player.getInput (pygame)
            player.move ()
            player.rotateTurret ()
            AI.move ()
            maze.moveBullets ()
            timer.tock (0)

            # move camera appropriately
            timer.tick ()
            camera.setPosition (Vector.Vector ([player.position ().x (), player.position ().y (), - ((400) * math.cos (player.viewingAngle ()))]) - (400 * math.sin (player.viewingAngle ())) * Vector.Vector ([math.sin (player.angle ()), math.cos (player.angle ()), 0]))
            camera.setLookingDir (Vector.Vector (player.position ().toList () + [0]) + Vector.Vector ([5, 5, 0]) - camera.position ())
            camera.setUpDir (-Vector.Vector ([math.sin (player.angle ()), math.cos (player.angle ()), 0]))
            timer.tock (1)

            # render everything for that sexy 3D feel
            timer.tick ()
            maze.addBulletsToRender (world)
            AI.addRobotsToRender (world)
            pygame.rect (Vector.Vector ([0, 0]), Vector.Vector ([pygame.width, pygame.height]), pygame.color ("white"))
            world.render (pygame)
            timer.tock (2)

            pygame.update ()
            if pygame.keyboardInput () [271]: # numpad enter key to show timer stats
                print timer
        else:
            levelController.reset ()
            if player.alive == False:
                print "aaaaaahhhh you suck, GG Loser"
                print "go back to level 1 where the scrubs like you belong\n\n"
                levelController.setLevel (1)
                player.resetPlayer ()
            else:
                print "You win! ...this level. best of luck next level\n\n"
                levelController.setLevel (levelController.currentLevel () + 1)
                
    else:
        keys = pygame.keyboardInput ()
        print "Out of level"
        levelController.loadLevel (pygame)
        
pygame.MainLoop (loop)


##def loop (frame):
##    pygame.update ()
##    keys = pygame.keyboardInput ()
##    for a in range (len (keys)):
##        if keys [a] != 0 and a != 300:
##            print a
##pygame.MainLoop (loop)
