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
# sprites
menuScreen = Pygame.Sprite (0, 0, 600, 600, 'MainScreen.png', pygame)
helpScreen = Pygame.Sprite (0, 0, 600, 600, 'HelpScreen.png', pygame)
upgradeScreen = Pygame.Sprite (0, 0, 600, 600, 'UpgradeScreen.png', pygame)

# buttons
bPlay = Pygame.Button (160, 227, 250, 284)
bHelp = Pygame.Button (349, 227, 450, 283)
bBack = Pygame.Button (492, 548, 600, 600)
bMovementSpeed = Pygame.Button (84, 18, 524, 81)
bTurnSpeed = Pygame.Button (119, 131, 469, 193)
bTurretSpeed = Pygame.Button (74, 235, 555, 301)
bCooldown = Pygame.Button (142, 347, 464, 408)
bBulletSpeed = Pygame.Button (55, 456, 562, 513)

# screen controller
screen = Pygame.Screen ('MainMenu')

for a in range (14):
   screen.addInsult () 

def loop (frame):
    if screen.currentScreen () == 'MainMenu':
        menuScreen.draw ()
        screen.drawInsults (pygame)
        if bPlay.clicked ():
            screen.setScreen ('Game')
            levelController.setLevel (1)
            levelController.loadLevel (pygame)
        elif bHelp.clicked ():
            screen.setScreen ('Help')
    elif screen.currentScreen () == 'Game':
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
            pygame.rect (Vector.Vector ([0, 0]), Vector.Vector ([pygame.width, pygame.height]), pygame.colorRGB (242, 242, 242))
            world.render (pygame)
            timer.tock (2)

            if pygame.keyboardInput () [271]: # numpad enter key to show timer stats
                print timer
        else:
            levelController.reset ()
            if player.alive == False:
                print "aaaaaahhhh you died on level " + str (levelController.currentLevel ()) + "???\n"
                print screen.randomInsult ()
                print "GG Loser"
                print "go back to level 1 where the scrubs like you belong\n\n"
                screen.addInsult ()
                player.resetPlayer ()
                screen.setScreen ('MainMenu')
            else:
                print "You win! ...this level. best of luck next level\n\n"
                screen.setNumUpgrades (levelController.currentLevel ())
                levelController.setLevel (levelController.currentLevel () + 1)
                screen.setScreen ('Upgrade')
    elif screen.currentScreen () == 'Upgrade':
        pygame.textSystem.addText ("Number of upgrades left: " + str (screen.numberOfUpgrades ()), 10, 550)
        upgradeScreen.draw ()
        if bMovementSpeed.clicked ():
            player.movementSpeed *= 1.25
            screen.setNumUpgrades (screen.numberOfUpgrades () - 1)
        elif bTurnSpeed.clicked ():
            player.rotspeed *= 1.25
            screen.setNumUpgrades (screen.numberOfUpgrades () - 1)
        elif bTurretSpeed.clicked ():
            player.turretrotspeed *= 1.25
            screen.setNumUpgrades (screen.numberOfUpgrades () - 1)
        elif bCooldown.clicked ():
            player.cooldown = int (player.cooldown * 0.75 + 1)
            screen.setNumUpgrades (screen.numberOfUpgrades () - 1)
        elif bBulletSpeed.clicked ():
            player.bulletSpeed *= 1.25
            screen.setNumUpgrades (screen.numberOfUpgrades () - 1)
        if screen.numberOfUpgrades () == 0:
            levelController.loadLevel (pygame)
            screen.setScreen ('Game')
            
    elif screen.currentScreen () == 'Help':
        helpScreen.draw ()
        if bBack.clicked ():
            screen.setScreen ('MainMenu')
    else:
        print 'problem', screen.currentScreen ()

        
pygame.MainLoop (loop)


##def loop (frame):
##    pygame.update ()
##    keys = pygame.keyboardInput ()
##    for a in range (len (keys)):
##        if keys [a] != 0 and a != 300:
##            print a
##pygame.MainLoop (loop)
