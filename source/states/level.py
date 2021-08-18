from ..components import info
import pygame
from ..import tools,setup
from .. import constants as C
from .. components import player
from .. components import player,stuff,brick,box,enemy
import os
import json

class Level:
    def start(self,game_info):
        self.game_info=game_info
        self.finished=False
        self.next='game_over'
        self.info=info.Info('level',self.game_info)
        self.load_map_data()
        self.setup_background()
        self.setup_start_position()
        self.setup_player()
        self.setup_ground_items()
        self.setup_bricks_and_boxes()
        self.setup_enemies()




    def load_map_data(self):
        file_name='level_1.json'
        file_path=os.path.join('source/data/maps',file_name)
        with open(file_path)as f:
            self.map_data=json.load(f)


    def setup_background(self):
        self.image_name=self.map_data['image_name']
        self.background=setup.GRAPHICS[self.image_name]
        rect=self.background.get_rect()
        self.background=pygame.transform.scale(self.background,(int(rect.width*C.BG_MULTI),
                                                       int(rect.height*C.BG_MULTI)))
        self.background_rect=self.background.get_rect()
        self.game_window=setup.SCREEN.get_rect()
        self.game_ground=pygame.Surface((self.background_rect.width,self.background_rect.height))

    def setup_start_position(self):
        self.position=[]
        for data in self.map_data['maps']:
            self.position.append((data['start_x'],data['end_x'],data['player_x'],data['player_y']))
        self.start_x,self.end_x,self.player_x,self.player_y=self.position[0]


    def setup_player(self):
        self.player=player.Player('mario')
        self.player.rect.x=self.game_window.x+self.player_x
        self.player.rect.bottom=self.player_y

    def setup_ground_items(self):
        self.ground_items_group=pygame.sprite.Group()
        for name in ['ground','pipe','step']:
            for item in self.map_data[name]:
                self.ground_items_group.add(stuff.Item(item['x'],item['y'],item['width'],item['height'],name))

    def setup_bricks_and_boxes(self):
        self.brick_group=pygame.sprite.Group()
        self.box_group=pygame.sprite.Group()
        if 'brick' in self.map_data:
            for brick_data in self.map_data['brick']:
                x,y=brick_data['x'],brick_data['y']
                brick_type=brick_data['type']
                if 'brick_num'in brick_data:
                    #TODO batch bricks
                    pass
                else:
                    self.brick_group.add(brick.Brick(x,y,brick_type))

        if 'box' in self.map_data:
            for box_data in self.map_data['box']:
                x,y=box_data['x'],box_data['y']
                box_type=box_data['type']

                self.box_group.add(box.Box(x,y,box_type))


    def setup_enemies(self):
        self.enemy_group_dict={}
        for enemy_group_data in self.map_data['enemy']:
            group=pygame.sprite.Group()
            for enemy_group_id,enemy_list in enemy_group_data.items():
                for enemy_data in enemy_list:
                    group.add(enemy.create_enemy(enemy_data))
                self.enemy_group_dict[enemy_group_id]=group




    def update(self,surface,keys):
        self.current_time=pygame.time.get_ticks()
        self.player.update(keys)
        if self.player.dead:
            if self.current_time-self.player.death_timer>3000:
                self.finished=True
                self.update_game_info()
        else:
            self.update_player_position()
            self.check_if_go_die()
            self.update_game_window()
            self.info.update()
            self.brick_group.update()
            self.box_group.update()



        self.draw(surface)

    def update_player_position(self):
        #x direction
        self.player.rect.x+=self.player.x_vel
        if self.player.rect.x<self.start_x:
            self.player.rect.x=self.start_x
        elif self.player.rect.right>self.end_x:
            self.player.rect.right=self.end_x
        self.check_x_collisions()

        #y direction
        self.player.rect.y+=self.player.y_vel
        self.check_y_collisions()

    def check_x_collisions(self):
        check_group=pygame.sprite.Group(self.ground_items_group,self.brick_group,self.box_group)
        collided_sprite=pygame.sprite.spritecollideany(self.player,check_group)

        if collided_sprite:
            self.adjust_player_x(collided_sprite)


    def check_y_collisions(self):
        check_group = pygame.sprite.Group(self.ground_items_group, self.brick_group,self.box_group)
        collided_sprite = pygame.sprite.spritecollideany(self.player, check_group)
        if collided_sprite:
            self.adjust_player_y(collided_sprite)
        self.check_will_fall(self.player)

    def adjust_player_x(self,sprite):
        if self.player.rect.x<sprite.rect.x:
            self.player.rect.right=sprite.rect.left
        else:
            self.player.rect.left=sprite.rect.right
        self.player.x_vel=0

    def adjust_player_y(self,sprite):
        # downwards
        if self.player.rect.bottom<sprite.rect.bottom:
            self.player.y_vel=0
            self.player.rect.bottom=sprite.rect.top
            self.player.state='walk'
        # upwards
        else:
            self.player.y_vel=7
            self.player.rect.top=sprite.rect.bottom
            self.player.state='fall'

    def check_will_fall(self,sprite):
        sprite.rect.y+=1
        check_group=pygame.sprite.Group(self.ground_items_group,self.brick_group,self.box_group)
        collided_sprite=pygame.sprite.spritecollideany(sprite,check_group)
        if not collided_sprite and sprite.state!='jump':
            sprite.state='fall'
        sprite.rect.y-=1

    def update_game_window(self):
        third=self.game_window.x+self.game_window.width/3
        if self.player.x_vel>0 and self.player.rect.centerx>third:
            self.game_window.x+=self.player.x_vel
            self.start_x=self.game_window.x



    def draw(self,surface):
        self.game_ground.blit(self.background,self.game_window,self.game_window)
        self.game_ground.blit(self.player.image,self.player.rect)
        self.brick_group.draw(self.game_ground)
        self.box_group.draw(self.game_ground)
        for enemy_group in self.enemy_group_dict.values():
            enemy_group.draw(self.game_ground)


        surface.blit(self.game_ground,(0,0),self.game_window)
        self.info.draw(surface)

    def check_if_go_die(self):
        if self.player.rect.y>C.SCREEN_H:
            self.player.go_die()

    def update_game_info(self):
        if self.player.dead:
            self.game_info['lives']-=1
        if self.game_info['lives']==0:
            self.next='game_over'
        else:
            self.next='load_screen'


