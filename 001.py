import pygame, math, sys
from pygame.font import SysFont
import random
from pygame.locals import *
from sprites import *

from singleton import Singleton

SCREEN_H = 1024
SCREEN_W = 768

spritePath = '225842_hyptosis_sprites-and-tiles-for-you.png'
TILE_W = TILE_H = 32

clock = pygame.time.Clock()
k_up = k_down = k_left = k_right = 0
direction = 0

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TILES_ACROSS = 5 - 1
TILES_DOWN = 5 - 1

PLAYER_START_X = PLAYER_START_Y = 1

BLOCK_DARKNESS = 0
BLOCK_PLAYER = 1
BLOCK_FLOOR = 2
BLOCK_WALL = 3
BLOCK_TRAP = 4


@Singleton
class DisplayDevice:
    def setScreen(self, screen):
        self.screen = screen

    def getScreen(self):
        return self.screen

class Scene(object):
    def __init__(self):
        pass

    def eraseScreen(self, screen):
        screen.fill( (0,0,0) )
        pass
    def render(self, screen):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def handle_events(self, events):
        raise NotImplementedError

class SceneMananger(object):
    def __init__(self):
        self.go_to(TitleScene())

    def go_to(self, scene):
        self.scene = scene
        self.scene.manager = self

class BattleScene(Scene):
    def __init__(self, entities):
        super(BattleScene, self).__init__()
        self.entities = entities

        self.fontPlayer = pygame.font.SysFont("Arial",13)

        self.screen = DisplayDevice.Instance().getScreen()
        self.eraseScreen(self.screen)


        self.totalPlayers = 0
        self.totalEnemies = 0

        self.buildInitiativeSequence()
        self.activeCharacterIndex = 0


    def buildInitiativeSequence(self):
        self.sequence = []
        index = 0
        for e in self.entities:
            if e['type'] == 'player':
                self.totalPlayers = self.totalPlayers + 1
            if e['type'] == 'enemy':
                self.totalEnemies = self.totalEnemies + 1
            self.sequence.append( { "index": index, "initiative": e['initiative'] } )
            index = index + 1

        self.sequence = sorted(self.sequence, key = lambda k: k['initiative'], reverse=True)


    def drawSequence(self, screen):
        startX = 30
        startY = 200
        offsetX = 10
        playerBoxWidth = 60
        playerBoxHeight = 30
        idx = 0

        color = (50, 100, 100)
        activeColor = (200, 10, 10)

        for seq in self.sequence:
            useColor = color

            if idx == self.activeCharacterIndex:
                useColor = activeColor
            xLeft, yLeft = (startX + playerBoxWidth * idx + offsetX * idx, startY)
            pygame.draw.rect(screen, useColor,
                             pygame.Rect(
                                 xLeft, yLeft,
                                 playerBoxWidth, playerBoxHeight),
                             1)
            # draw active player border
            text = self.fontPlayer.render( self.entities[seq['index']]['name'], True, (255, 255, 255))
            screen.blit(text, (xLeft + 1, yLeft + playerBoxHeight * .8))
            idx = idx + 1


    def getActiveCharacter(self):
        return self.entities[ self.sequence[self.activeCharacterIndex]['index'] ]

    def getPrevActiveCharacter(self):
        self.activeCharacterIndex = self.activeCharacterIndex - 1
        if self.activeCharacterIndex <  0:
            self.activeCharacterIndex = (self.totalPlayers + self.totalEnemies) - 1
        return self.sequence[self.activeCharacterIndex]

    def getNextActiveCharacter(self):
        self.activeCharacterIndex = self.activeCharacterIndex + 1
        if self.activeCharacterIndex >=  (self.totalPlayers + self.totalEnemies):
            self.activeCharacterIndex = 0
        return self.sequence[self.activeCharacterIndex]

    def drawPlayer(self, screen, obj):
        startX = 30
        startY = 300
        offsetX = 10
        playerBoxWidth = 50
        playerBoxHeight = 80
        idx = 0

        color = (50, 100, 100)
        activeColor = (200, 10, 10)

        for o in obj:
            useColor = color
            if o == self.getActiveCharacter():
                useColor = activeColor
            xLeft, yLeft = (startX + playerBoxWidth * idx + offsetX * idx, startY)
            pygame.draw.rect(screen, useColor,
                             pygame.Rect(
                                 xLeft, yLeft,
                                 playerBoxWidth, playerBoxHeight),
                             1)
            # draw active player border
            text = self.fontPlayer.render(o['name'], True, (255, 255, 255))
            screen.blit(text, (xLeft + 1, yLeft + playerBoxHeight * .8))
            idx = idx + 1
        # draw players name

    def drawEnemy(self, screen, obj):
        startX = 330
        startY = 300
        offsetX = 10
        playerBoxWidth = 50
        playerBoxHeight = 80
        idx = 0

        color = (50, 100, 100)
        activeColor = (200, 10, 10)

        for o in obj:
            useColor = color
            if o == self.getActiveCharacter():
                useColor = activeColor
            xLeft, yLeft = (startX + playerBoxWidth * idx + offsetX * idx, startY)
            pygame.draw.rect(screen, useColor,
                             pygame.Rect(
                                 xLeft, yLeft,
                                 playerBoxWidth, playerBoxHeight),
                             1)
            # draw active player border

            text = self.fontPlayer.render(o['name'], True, (255, 255, 255))
            screen.blit(text, (xLeft + 1, yLeft + playerBoxHeight * .8))

            idx = idx + 1

    #draw intiative sequence
    def drawInterface(self, screen):
        return
        idx = 0
        for i in self.sequence:
            if self.getActiveCharacter() == i:
                print "ACTIVE:",
            print self.entities[i['index']]['name'],
            idx = idx + 1
        print "\n"

    def handle_events(self, events):
        #wait for combat actions
        for event in events:
            if not hasattr(event, 'key'): continue

            if event.type == pygame.KEYDOWN:
                if event.key == K_LEFT: self.getPrevActiveCharacter()
                if event.key == K_RIGHT: self.getNextActiveCharacter()
                if event.key == K_UP: continue
                if event.key == K_DOWN: continue
        pass

    def update(self):
        pass

    def render(self, screen):
        enemies = players = []
        for e in self.entities:
            if e['type'] == 'player':
                players.append(e)
            if e['type'] == 'enemy':
                enemies.append(e)

        self.drawPlayer(screen, players)
        self.drawPlayer(screen, enemies)

        self.drawInterface(screen)
        self.drawSequence(screen)

        print self.getActiveCharacter()

        pygame.draw.rect(screen, (10,10,250),
                          pygame.Rect(
                                 30, 500,
                                 500, 100),
                             )
        text = self.fontPlayer.render("Current active is %s" % self.getActiveCharacter()['name'], True, (255, 255, 255))
        screen.blit(text, (30, 500))
        #Render player
        #Render enemy
        #Render combat interface
        pass


class DungeonScene(Scene):
    def __init__(self, levelId):
        super(DungeonScene, self).__init__()
        self.screen = DisplayDevice.Instance().getScreen()
        #load sprites from sheet
        self.loadTiles()
        self.textBuffer = []

        self.clock = pygame.time.Clock()
        self.direction = 0
        self.position = (PLAYER_START_X, PLAYER_START_Y)

        self.map = Map()
        self.map.map[PLAYER_START_X][PLAYER_START_Y] = BLOCK_FLOOR
        self.init_text()

    def move(self, hor, vert):
        x, y = self.position

        x = x + hor
        y = y + vert

        if x > TILES_ACROSS  or x < 0 or y > TILES_DOWN  or y < 0:
            return

        self.map.generateRoomIfNotGenerated( (x,y) )
        if self.map.isTraversable((x,y)):
            self.map.generateRoomsAroundCoords( (x, y) )
            self.position = (x, y)
            self.screen.blit(self.bg, (0, 0))

    def handle_events(self, events):
        hor = 0
        vert = 0
        for event in events:
            if not hasattr(event, 'key'): continue

            if event.type == pygame.KEYDOWN:
                if event.key == K_LEFT: hor = -1
                if event.key == K_RIGHT: hor = 1
                if event.key == K_UP: vert = -1
                if event.key == K_DOWN: vert = 1
                # TODO: sync text display with player movement
                self.move(hor, vert)
                # self.map.print_ascii_map()

    def init_text(self):
        self.myfont = pygame.font.Font(None,15)


    def loadTiles(self):
        self.spriteSheet = spritesheet(spritePath)
        #self.player = self.spriteSheet.image_at((424, 818, TILE_W , TILE_H ), colorkey=-1)
        self.player = self.spriteSheet.image_at((13*TILE_W + 8, 25*TILE_H+16 , TILE_W, TILE_H ),colorkey=-1)
        self.player.convert_alpha()

        self.bg = self.spriteSheet.image_at((0, 0, TILE_W , TILE_H ))

        self.tileFloor = self.spriteSheet.image_at((13*TILE_W+8, 22*TILE_H+16, TILE_W, TILE_H ))
        self.tileWall  = self.spriteSheet.image_at((13*TILE_W+8, 21*TILE_H+16, TILE_W, TILE_H ))

        self.tileTrap  = self.spriteSheet.image_at((15*TILE_W+8, 22*TILE_H+16, TILE_W, TILE_H ))

    def update(self):
        pass

    def render(self, screen):
        self.draw_Text(
            self.textBuffer,
            (300, 300),
            screen
        )

        self.redraw_map_tiles(screen)
        #TRANSPARENCY IS SOMEWHERE AROUND
        self.draw_PlayerTile(screen)

    ''' Render part '''
    def redraw_map_tiles(self, screen):
        print self.map.map.__len__()
        for row in range(TILES_ACROSS + 1):
            for col in range(TILES_DOWN + 1):
                if self.map.map[row][col] == BLOCK_DARKNESS:
                    pygame.draw.rect(screen, BLACK, (row * TILE_W, col * TILE_H, TILE_W, TILE_H))
                if self.map.map[row][col] == BLOCK_FLOOR:
                    screen.blit(self.tileFloor, Map.convertTileToCoords( (row, col) ) )
                if self.map.map[row][col] == BLOCK_TRAP:
                    screen.blit(self.tileTrap, Map.convertTileToCoords( (row, col) ) )
                if self.map.map[row][col] == BLOCK_WALL:
                    screen.blit(self.tileWall, Map.convertTileToCoords( (row, col) ) )


    def draw_PlayerTile(self, screen):
        screen.blit(self.player, Map.convertTileToCoords( self.position) )
        #print "Drawing player at %s, %s" % (self.position)

    #TODO: add text wrapper
    def draw_Text(self,text, coords, screen):
        x, y = coords

        text = ""
        for textString in self.textBuffer:
            text += textString + ". "

        label = self.myfont.render(text, 1, (255,255,255))

        emptySurface =  pygame.Surface( (200,200) )
        emptySurface.fill((0,0,0))
        screen.blit(emptySurface, (x, y))
        screen.blit(label, (x, y))
        self.textBuffer = []



class TitleScene(object):
    def __init__(self):
        super(TitleScene, self).__init__()
        self.font = pygame.font.SysFont('Arial', 56)
        self.sfont = pygame.font.SysFont('Arial', 32)
        print "TitleScreen"

    def render(self, screen):
        screen.fill((10, 10, 10))
        text1 = self.font.render('> press space to start <', True, (255, 255, 255))
        screen.blit(text1, (200, 50))

    def update(self):
        pass

    def handle_events(self, events):
        for e in events:
            if e.type == KEYDOWN and e.key == K_SPACE:
                self.manager.go_to(DungeonScene(0))

class Map(object):
    def __init__(self):
        self.map = []
        for i in range(TILES_ACROSS + 1):
            row = []
            for j in range(TILES_DOWN + 1):
                row.append(0)
            self.map.append(row)

    #Sets block enabled for redraw
    def clear_block(self, position):
        #column, row = self.convertTileToCoords(position)
        column, row = position
        print "Column %s, Row %s" % (str(column), str(row))
        self.map[column][row] = 0

    def set_block(self, position, block_id):
        column, row = position
        print "Column %s, Row %s" % (str(column), str(row))
        self.map[column][row] = block_id

    def print_ascii_map(self):
        for row in self.map:
            print row

    @staticmethod
    def convertTileToCoords(coords):
        tileX, tileY = coords
        return (tileX * TILE_W, tileY * TILE_H)

    def generateRoomIfNotGenerated(self, position):
        col, row = position
        if self.map[col][row] == BLOCK_DARKNESS:
            self.map[col][row] = int (random.choice("234"))

    def generateRoomsAroundCoords(self, position):
        x,y = position
        possiblePos = ( (x-1,y), (x+1,y), (x,y-1), (x,y+1) )
        print possiblePos
        for side in possiblePos:
            x,y = side

            if x >= 0 and x < len(self.map) \
                    and y >= 0 and y < len(self.map[x]):
                print "make a tile for %s:%s" % (x, y)
                self.generateRoomIfNotGenerated( (x, y) )


    def isTraversable(self, position):
        x, y = position
        if self.map[x][y] == BLOCK_WALL:
            return False
        return True


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    DisplayDevice.Instance().setScreen(screen)
    running = True

    manager = SceneMananger()

    while running:
        if pygame.event.get(QUIT):
            running = False
            return
        events = pygame.event.get()

        manager.scene.handle_events(events)
        manager.scene.update()
        manager.scene.render(screen)
        pygame.display.flip()

        for event in events:
            print "Running...", events
            if not hasattr(event, 'key'): continue
            if event.key == K_ESCAPE:
                print "ESC pressed"
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    manager.go_to(TitleScene())
                if event.key == pygame.K_F2:
                    manager.go_to(DungeonScene(0))
                if event.key == pygame.K_F3:
                    manager.go_to(BattleScene(
                        [
                        {'type': 'player', 'name':'TankTwo', 'position' : 2, 'initiative': 6},
                        {'type': 'player', 'name':'TankOne', 'position' : 1, 'initiative': 2},
                        {'type': 'player', 'name':'HealOne', 'position' : 3, 'initiative': 4},
                        {'type': 'enemy','name':'EnemyOne', 'position' : 1, 'initiative': 5},
                        {'type': 'enemy', 'name':'EnemyTwo', 'position' : 2, 'initiative': 3}
                        ]
                    ))

if __name__ == "__main__":
    main()
