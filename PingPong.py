import pygame as pg

MAX_SCORE = 3
WIDTH = 800
HEIGHT = 600
TITLE = "PingPong!"
FPS_LIMIT = 75
RESTART_KEYS = (pg.K_LCTRL,pg.K_RCTRL)
MUSIC_VOLUME = 60 #%
SOUNDS_VOLUME = 60 #%
BOUNCE_SOUND = "Bounce.MP3"
BG_MUSIC = "8bitMusicGame.MP3"
BACKGROUND = "PPBackground.png"

class GSprite(pg.sprite.Sprite): #GameSprite
	def __init__(self, image:str,speed:int, pos:tuple,size:tuple):
		super().__init__()
		self.image = pg.transform.scale(pg.image.load(image),(size[0],size[1]))
		self.rect = self.image.get_rect()
		self.size = size
		self.rect.x = pos[0]
		self.rect.y = pos[1]
		self.speed = speed
		self.mask = pg.mask.from_surface(self.image)

	def show(self, surface):
		surface.blit(self.image, (self.rect.x, self.rect.y))

class Player(GSprite):
	def __init__(self, image:str,speed:int, pos:tuple,size:tuple,keyUp, keyDown, keyRestart):
		super().__init__(image, speed, pos, size)

		self.keyUp = pg.K_w
		self.keyDown = pg.K_s
		self.keyRestart = pg.K_r

		self.keyUp = keyUp
		self.keyDown = keyDown
		self.keyRestart = keyRestart

	def update(self):
		keys = pg.key.get_pressed()
		if keys[self.keyUp] and self.rect.y > 0:
			self.rect.y -= self.speed
		if keys[self.keyDown] and self.rect.y+self.rect.height < HEIGHT:
			self.rect.y += self.speed

class Ball(GSprite):
	def __init__(self,image:str,speed:int, pos:tuple,size:tuple, speedy:int):
		super().__init__(image,speed,pos,size)
		self.speedy = speedy

	def update(self):
		self.rect.x += self.speed
		self.rect.y += self.speedy
		if self.rect.y > HEIGHT-self.rect.height or self.rect.y < 0:
			self.speedy *= -1
			bounce_sound.play()
		colliding = pg.sprite.spritecollide(ball,players,False, pg.sprite.collide_mask)
		if colliding:
			self.speed *= -1
			if colliding[0].rect.centerx > WIDTH/2:
				self.rect.x = colliding[0].rect.left - self.rect.width
			else:
				self.rect.x = colliding[0].rect.right
			bounce_sound.play()
		if self.rect.x < -self.rect.width:
			self.rect.x = (WIDTH/2)+(self.rect.width/2)
			self.rect.y = (HEIGHT/2)+(self.rect.height/2)
			players_score[0] += 1
		elif self.rect.x > WIDTH:
			self.rect.x = (WIDTH/2)+(self.rect.width/2)
			self.rect.y = (HEIGHT/2)+(self.rect.height/2)
			players_score[1] += 1
			bounce_sound.play()

pg.init()
window = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption(TITLE)
bg_image = pg.transform.scale(pg.image.load(BACKGROUND),(800,600))
pg.mixer.music.load(BG_MUSIC)
pg.mixer.music.set_volume(MUSIC_VOLUME/100)
bounce_sound = pg.mixer.Sound(BOUNCE_SOUND)
bounce_sound.set_volume(SOUNDS_VOLUME/100)
# pg.mixer.music.
pg.mixer.music.play(-1)
#Examples
player1 = Player("Player.png", 4, (50,(HEIGHT/2)-((80*1.5)/2)), (16*2,80*1.5),pg.K_w,pg.K_s,pg.K_r)
player2 = Player("Player.png", 4, (WIDTH-82,(HEIGHT/2)-((80*1.5)/2)), (16*2,80*1.5),pg.K_UP,pg.K_DOWN,pg.K_SLASH)
ball = Ball("Ball.png", 3, (WIDTH/2,HEIGHT/2), (32,32),3)
players = pg.sprite.Group()
players.add(player1,player2)
players_score = [0,0]
font = pg.font.SysFont("Bahschrift",42)
restart_font = pg.font.SysFont("Bahschrift",34)
win = font.render("Winner", True, (255,255,150,255))
lose = font.render("Lose", True, (255,100,100,255))
win_lose_position = ((150,10),
					 (WIDTH-200,10))
score_position = ((10,10),
				  (WIDTH-40,10))
p1 = font.render(str(players_score[0]),True,(200,200,200,255))
p2 = font.render(str(players_score[1]),True,(200,200,200,255))
restart_text = restart_font.render("To restart press: LCtrl and RCtrl", True, (200,200,200,255))

clock = pg.time.Clock()

match = 1
run = 1
while run:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			run = 0
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_ESCAPE:
				run = 0
	if pg.key.get_pressed()[RESTART_KEYS[0]] and pg.key.get_pressed()[RESTART_KEYS[1]]:
		players_score = [0,0]
		ball.rect.x = (WIDTH/2)+(ball.rect.width/2)
		ball.rect.y = (HEIGHT/2)+(ball.rect.height/2)
		player1.rect.y = (HEIGHT/2)-(player1.rect.height/2)
		player2.rect.y = (HEIGHT/2)-(player2.rect.height/2)
		match = 1

	if match:
		window.blit(bg_image, (0,0))
		players.update()
		players.draw(window)
		ball.update()
		ball.show(window)

		p1 = font.render(str(players_score[0]),True,(200,200,200,255))
		p2 = font.render(str(players_score[1]),True,(200,200,200,255))
		window.blit(p1,score_position[0])
		window.blit(p2,score_position[1])

		for score in players_score:
			if score >= MAX_SCORE:
				if players_score[0] >= MAX_SCORE:
					window.blit(win, win_lose_position[1])
					window.blit(lose, win_lose_position[0])
				else:
					window.blit(win, win_lose_position[0])
					window.blit(lose, win_lose_position[1])
				match = 0
	else:
		window.blit(restart_text,(WIDTH/2-170,HEIGHT/4*3))

	clock.tick(FPS_LIMIT)
	pg.display.update()