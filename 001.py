import pygame, math, sys
from pygame.font import SysFont
import random
from pygame.locals import *
from sprites import *

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

pygame.init()

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


class Game(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        #load sprites from sheet
        self.loadTiles()
        self.textBuffer = []

        self.clock = pygame.time.Clock()
        self.direction = 0
        self.position = (PLAYER_START_X, PLAYER_START_Y)

        self.map = Map()
        self.map.map[PLAYER_START_X][PLAYER_START_Y] = BLOCK_FLOOR
        self.redraw_map_tiles()
        self.draw_PlayerTile()

        self.init_text()
        self.run()

    def redraw_map_tiles(self):
        print self.map.map.__len__()
        for row in range(TILES_ACROSS + 1):
            for col in range(TILES_DOWN + 1):
                if self.map.map[row][col] == BLOCK_DARKNESS:
                    pygame.draw.rect(self.screen, BLACK, (row * TILE_W, col * TILE_H, TILE_W, TILE_H))
                if self.map.map[row][col] == BLOCK_FLOOR:
                    self.screen.blit(self.tileFloor, Map.convertTileToCoords( (row, col) ) )
                if self.map.map[row][col] == BLOCK_TRAP:
                    self.screen.blit(self.tileTrap, Map.convertTileToCoords( (row, col) ) )
                if self.map.map[row][col] == BLOCK_WALL:
                    self.screen.blit(self.tileWall, Map.convertTileToCoords( (row, col) ) )


    def draw_PlayerTile(self):
        self.screen.blit(self.player, Map.convertTileToCoords( self.position) )
        #print "Drawing player at %s, %s" % (self.position)
        pygame.display.flip()

    def move(self, hor, vert):
        x, y = self.position

        x = x + hor
        y = y + vert

        if x > TILES_ACROSS  or x < 0 or y > TILES_DOWN  or y < 0:
            return

        self.map.generateRoomsAroundCoords( (x, y) )
        if self.map.isTraversable((x,y)):
            self.position = (x, y)
            self.screen.blit(self.bg, (0, 0))

        self.redraw_map_tiles()
        #TRANSPARENCY IS SOMEWHERE AROUND
        self.draw_PlayerTile()

    def run(self):
        while 1:
            self.clock.tick(30)
            hor = 0
            vert = 0
            for event in pygame.event.get():
                if not hasattr(event, 'key'): continue
                if event.key == K_ESCAPE: sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == K_LEFT: hor = -1
                    if event.key == K_RIGHT: hor = 1
                    if event.key == K_UP: vert = -1
                    if event.key == K_DOWN: vert = 1
                    #TODO: sync text display with player movement
                    self.draw_Text(
                        self.textBuffer,
                        (300,300)
                    )
                    self.move(hor, vert)
                    #self.map.print_ascii_map()

    def init_text(self):
        self.myfont = pygame.font.Font(None,15)

    #TODO: add text wrapper
    def draw_Text(self,text, coords):
        x, y = coords

        text = ""
        for textString in self.textBuffer:
            text += textString + ". "

        label = self.myfont.render(text, 1, (255,255,255))

        emptySurface =  pygame.Surface( (200,200) )
        emptySurface.fill((0,0,0))
        self.screen.blit(emptySurface, (x, y))
        self.screen.blit(label, (x, y))
        self.textBuffer = []

    def loadTiles(self):
        self.spriteSheet = spritesheet(spritePath)
        #self.player = self.spriteSheet.image_at((424, 818, TILE_W , TILE_H ), colorkey=-1)
        self.player = self.spriteSheet.image_at((13*TILE_W + 8, 25*TILE_H+16 , TILE_W, TILE_H ),colorkey=-1)
        self.player.convert_alpha()

        self.bg = self.spriteSheet.image_at((0, 0, TILE_W , TILE_H ))

        self.tileFloor = self.spriteSheet.image_at((13*TILE_W+8, 22*TILE_H+16, TILE_W, TILE_H ))
        self.tileWall  = self.spriteSheet.image_at((13*TILE_W+8, 21*TILE_H+16, TILE_W, TILE_H ))

        self.tileTrap  = self.spriteSheet.image_at((15*TILE_W+8, 22*TILE_H+16, TILE_W, TILE_H ))


def main():
    while 1:
        game = Game()


if __name__ == "__main__":
    main()
