import pygame
from random import randint ,choice
#If your game closes due to an error in line 112, you'll have to restart the game
#I think I solved the issue, but it was so persistent that I can't be sure
#I stopped getting the error myself, but I don't know for certain that I completely solved the issue
#It's caused by some issue with a monsters path reset and having a coin in the way

#NOTE: THIS GAME HAS AN OPTIONAL EASY MODE.
#TO TURN IT ON, CHANGE THE LAST LINE OF CODE TO "Escape(True)"
#IT TOGGLES ON THE VISIBLE PATHS OF THE MONSTERS

class Escape:
    def __init__(self,easy_mode:bool):
        pygame.init()
        self.easy_mode=easy_mode
        #additional information that's tracked
        self.total_points=0
        self.restarts=-1
        
        self.load_images()
        self.new_game()

        self.height=len(self.map)
        self.width=len(self.map[0])
        self.scale=90
        
        window_height=self.scale * self.height
        window_width=self.scale * self.width
        self.window=pygame.display.set_mode((window_width,window_height+self.scale))

        pygame.display.set_caption("Monster escape")
        self.game_font=pygame.font.SysFont("Calibri",24)

        self.main_loop()
    
    def load_images(self):
        self.images=[]
        for name in ["coin","door","monster","robot"]:
            self.images.append(pygame.image.load(name + ".png"))
    
    def new_coin(self):
        #the position of each new coin is randomised until a space that is free is generated
        while True:
            newcoin_y=randint(0,8)
            newcoin_x=randint(0,13)
            if self.map[newcoin_y][newcoin_x] ==4:
                self.map[newcoin_y][newcoin_x]= 0
                break
    
    def find_robot(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] == 3:
                    return (y,x)
    
    def new_monsters(self):
        #each of the 6 monsters has a path, they move along each list respectively. The tuples are coordinates as (y,x)
        self.monstermoves=[ [(3,4),(3,5),(2,5),(2,6),(1,6),(0,6),(0,5),(1,5),(1,4),(1,3),(1,2),(0,2),(0,1),(1,1),(1,0),(2,0),(2,1),(2,2),(2,3),(3,3)],
                            [(4,1),(4,2),(4,3),(4,4),(4,5),(5,5),(6,5),(6,4),(6,3),(6,2),(6,1),(6,0),(5,0),(4,0)],
                            [(7,3),(7,4),(7,5),(7,6),(6,6),(6,7),(6,8),(7,8),(8,8),(8,7),(8,6),(8,5),(8,4),(8,3),(8,2),(8,1),(7,1),(7,2)],
                            [(5,12),(5,11),(5,10),(5,9),(6,9),(6,10),(6,11),(7,11),(8,11),(8,12),(8,13),(7,13),(6,13),(5,13)],
                            [(1,11),(2,11),(3,11),(3,10),(4,10),(4,11),(4,12),(3,12),(2,12),(2,13),(1,13),(0,13),(0,12),(0,11)],
                            [(1,8),(2,8),(2,9),(2,10),(1,10),(0,10),(0,9),(0,8)]]
        self.monsters=[]
        #randomising the initial positions of the monsters: 
        #The monster's positions are stored in self.monsters in the form of the index of that coordinate on their respective path in self.monstermoves
        for i in range(len(self.monstermoves)):
            test=choice(self.monstermoves[i])
            ind=self.monstermoves[i].index(test)
            self.monsters.append(ind)
            self.map[test[0]][test[1]]=2
        


    def new_game(self):
        #Initialising all the information that's tracked on a per-run basis
        self.moves=0
        self.restarts+=1
        self.endgame=False
        self.fail=False
        self.win=False
        self.points=0
        #resetting the map and randomising the starting positions of the monsters and first coin
        self.map= [[4, 4, 4, 4, 4, 4, 4, 5, 4, 4, 4, 4, 4, 4],
                   [4, 4, 4, 4, 4, 4, 4, 5, 4, 4, 4, 4, 4, 4],
                   [4, 4, 4, 4, 4, 4, 4, 5, 4, 4, 4, 4, 4, 4],
                   [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                   [4, 4, 4, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 4],
                   [4, 4, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                   [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                   [4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 4, 4, 4],
                   [4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 4, 4, 4]]
        self.new_monsters()
        self.new_coin()
    
    def movemonster(self):
        #each monster moves one at a time.
        #if the square they are moving to has a coin on it, they jump over the coin
        i=0
        #here: monster is the index of that position in self.monstermoves            
        for monster in self.monsters:
            #first removing the current place of the monster from the map
            self.map[self.monstermoves[i][monster][0]][self.monstermoves[i][monster][1]]=4
            #checking if the index (monster) is at the end of the path
            if monster>=len(self.monstermoves[i])-1:
                #if so, then the variables are set to -1 to reset the index
                #-1 because at the end of each movement +1 is added
                self.monsters[i]=-1
                monster=-1
            
            #testing if the next square has a coin. if so, the index will increase by 1, meaning the monster will skip that square
            if self.map[self.monstermoves[i][monster+1][0]][self.monstermoves[i][monster+1][1]]==0:
                self.monsters[i]+=1
                monster+=1
            self.monsters[i]+=1


            #finding the next square the monster will land on
            newx=self.monstermoves[i][self.monsters[i]][1]
            newy=self.monstermoves[i][self.monsters[i]][0]

            #placing the monster on the new square and updating its index accordingly
            self.map[newy][newx]=2

            
            i+=1
    
    def exit(self):
        #this makes the exit appear and stops coins from spawning
        self.endgame=True
        #set number of squares where monsters will not go on
        options=[(0,0),(0,3),(0,4),(1,9),(1,12),(2,4),(3,0),(3,1),(3,2),(3,13),(4,13),(5,1),(6,12),(7,0),(7,7),(7,12),(8,0)]
        #randomly selecting one of these until the one chosen is not currently occupied
        while True:
            exit=choice(options)
            if self.map[exit[0]][exit[1]]==4:
                self.map[exit[0]][exit[1]]=1
                break

    def move(self, y_move, x_move):
        if self.win or self.fail:
            return
        #if you step on a square that a monster is on
        if self.find_robot()==None:
            self.fail=True
            return
        robot_old_y, robot_old_x =self.find_robot()
        robot_new_y=robot_old_y+ y_move
        robot_new_x=robot_old_x+x_move

        #checking if hit wall:
        try:
            if self.map[robot_new_y][robot_new_x] == 5:
                return
            if robot_new_x <0 or robot_new_y<0:
                return
        except IndexError:
            return

        
        #checking if collect coin
        if self.map[robot_new_y][robot_new_x]==0:
            self.points+=1
            self.total_points+=1
            #new coins are spawned only when you have less than 10
            if self.points!=10:
                self.new_coin()
        
        #if you exit you win
        if self.map[robot_new_y][robot_new_x]==1:
            self.win=True
            
        self.map[robot_new_y][robot_new_x]=3
        self.map[robot_old_y][robot_old_x]=4
        self.movemonster()
        if self.map[robot_new_y][robot_new_x]== 2:
            self.fail=True
        #right after the 10th coin is collected, the exit is spawned and no more coins will spawn
        if self.points==10 and not self.endgame:
            self.exit()
        self.moves+=1

    def main_loop(self):
        while True:
            self.check_events()
            self.draw_window()

    def check_events(self):
        for event in pygame.event.get():
            #both wasd and arrow keys work
            if event.type == pygame.KEYDOWN:
                if event.key ==pygame.K_LEFT or event.key==pygame.K_a:
                    self.move(0, -1)
                if event.key ==pygame.K_RIGHT or event.key==pygame.K_d:
                    self.move(0, 1)
                if event.key == pygame.K_UP or event.key ==pygame.K_w:
                    self.move(-1,0)
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.move(1,0)
                if event.key == pygame.K_F2:
                    self.new_game()
                if event.key == pygame.K_ESCAPE:
                    exit()

            if event.type == pygame.QUIT:
                exit()

    def draw_window(self):
        self.window.fill((160,160,160))

        #drawing the 3 walls
        pygame.draw.rect(self.window,(0, 0, 0), (630,0,90,270))
        pygame.draw.rect(self.window,(0, 0, 0), (180,450,270,90))
        pygame.draw.rect(self.window,(0, 0, 0), (810,630,180,180))


        #text at bottom of screen:
        info_text=self.game_font.render("You're in a doorless room full of monsters. You find a note that reads 'A door costs ten points'",True,(0,0,0))
        info_text2=self.game_font.render("Find 10 coins and get to the exit, but make sure to avoid the monsters", True, (0,0,0))
        control_text=self.game_font.render("Coins: "+ str(self.points)+   "            F2 = new game           Esc = exit game          WASD or arrow keys = move", True,(0,0,0))
        self.window.blit(control_text,(self.width*self.scale/2 -(control_text.get_width()/2), self.height*self.scale + 10))
        self.window.blit(info_text, (self.width*self.scale/2 -(info_text.get_width()/2), self.height*self.scale +35))
        self.window.blit(info_text2,(self.width*self.scale/2 -(info_text2.get_width()/2), self.height*self.scale + 60))

        #the optional guidetracks for the monsters:
        if self.easy_mode:
            pygame.draw.rect(self.window, (255,0,0), (765,45,180,180), width=3)

            pygame.draw.rect(self.window, (255,0,0),(45,405,450,180),3)

            pygame.draw.line(self.window, (255,0,0),(45,135),(45,225),3)
            pygame.draw.line(self.window,(255,0,0), (45,135),(135,135),3)
            pygame.draw.line(self.window,(255,0,0), (135,135),(135,45),3)
            pygame.draw.line(self.window,(255,0,0),(135,45),(225,45),3)
            pygame.draw.line(self.window,(255,0,0), (225,45),(225,135),3)
            pygame.draw.line(self.window,(255,0,0), (225,135),(495,135),3)
            pygame.draw.line(self.window,(255,0,0),(495,135),(495,45),3)
            pygame.draw.line(self.window,(255,0,0), (495,45),(585,45),3)
            pygame.draw.line(self.window,(255,0,0),(585,45),(585,225),3)
            pygame.draw.line(self.window,(255,0,0),(585,225),(495,225),3)
            pygame.draw.line(self.window,(255,0,0),(495,225),(495,315),3)
            pygame.draw.line(self.window,(255,0,0),(495,315),(315,315),3)
            pygame.draw.line(self.window,(255,0,0),(315,315),(315,225),3)
            pygame.draw.line(self.window,(255,0,0),(315,225),(45,225),3)

            pygame.draw.line(self.window,(255,0,0),(135,675),(585,675),3)
            pygame.draw.line(self.window,(255,0,0),(585,675),(585,585),3)
            pygame.draw.line(self.window,(255,0,0),(585,585),(765,585),3)
            pygame.draw.line(self.window,(255,0,0),(765,585),(765,765),3)
            pygame.draw.line(self.window,(255,0,0),(765,765),(135,765),3)
            pygame.draw.line(self.window,(255,0,0),(135,765),(135,675),3)
            
            pygame.draw.line(self.window,(255,0,0),(855,585),(855,495),3)
            pygame.draw.line(self.window,(255,0,0),(855,585),(1035,585),3)
            pygame.draw.line(self.window,(255,0,0),(1035,585),(1035,765),3)
            pygame.draw.line(self.window,(255,0,0),(1035,765),(1215,765),3)
            pygame.draw.line(self.window,(255,0,0),(1215,765),(1215,495),3)
            pygame.draw.line(self.window,(255,0,0),(1215,495),(855,495),3)

            pygame.draw.line(self.window,(255,0,0),(945,405),(1125,405),3)
            pygame.draw.line(self.window,(255,0,0),(1125,405),(1125,225),3)
            pygame.draw.line(self.window,(255,0,0),(1125,225),(1215,225),3)
            pygame.draw.line(self.window,(255,0,0),(1215,225),(1215,45),3)
            pygame.draw.line(self.window,(255,0,0),(1215,45),(1035,45),3)
            pygame.draw.line(self.window,(255,0,0),(1035,45),(1035,315),3)
            pygame.draw.line(self.window,(255,0,0),(1035,315),(945,315),3)
            pygame.draw.line(self.window,(255,0,0),(945,315),(945,405),3)


        #draw the grid:
        for x in range(0, self.width*self.scale,self.scale):
            for y in range(0,self.height*self.scale,self.scale):
                rect=pygame.Rect(x,y,self.scale,self.scale)
                pygame.draw.rect(self.window,(0, 0, 0),rect,1)


        for y in range(self.height):
            for x in range(self.width):
                square=self.map[y][x]
                #centering each sprite based on their size
                if square ==0:
                    self.window.blit(self.images[square],(x*self.scale+25,y*self.scale+25))
                if square ==1:
                    self.window.blit(self.images[square],(x*self.scale + 20,y*self.scale+10))
                if square ==2:
                    self.window.blit(self.images[square],(x*self.scale + 20,y*self.scale+10))
                if square ==3:
                    self.window.blit(self.images[square],(x*self.scale+20,y*self.scale+2))
        
        #failscreen
        if self.fail or self.find_robot()==None:
            lose=self.game_font.render("You lose: Retry = F2",True,(255,255,255))
            game_text=self.game_font.render("The robot got eaten by a monster somehow :(",True,(255,255,255))
            xgtext=self.scale*self.width/2 -game_text.get_width()/2
            ygtext=self.scale*self.height/2 -game_text.get_height()/2+lose.get_height()+5
            xtext=self.scale*self.width/2 -lose.get_width()/2
            ytext=self.scale*self.height/2-lose.get_height()/2
            pygame.draw.rect(self.window, (255,255,255), (xgtext-10,ytext-10,game_text.get_width()+20,game_text.get_height()+lose.get_height()+25))
            pygame.draw.rect(self.window, (0,0,0), (xgtext-5,ytext-5,game_text.get_width()+10,game_text.get_height()+lose.get_height()+15))
            self.window.blit(lose,(xtext,ytext))
            self.window.blit(game_text,(xgtext,ygtext))

        #winscreen
        if self.win:
            game_text=self.game_font.render("Congratulations, you managed to escape!",True,(255,255,255))
            if self.restarts==1:
                data_text=self.game_font.render(f"you restarted 1 time, collecting {self.total_points} coins overall", True,(255,255,255))
            else:
                data_text=self.game_font.render(f"You restarted {self.restarts} times, collecting {self.total_points} coins overall",True,(255,255,255))            
            game_text_x=self.scale*self.width/2 -game_text.get_width()/2
            game_text_y=self.scale*self.height/2 -game_text.get_height()/2+data_text.get_height()+5

            xtext=self.scale*self.width/2 -data_text.get_width()/2
            ytext=self.scale*self.height/2 +data_text.get_height()+20
            pygame.draw.rect(self.window, (255,255,255), (xtext-10,game_text_y-10,data_text.get_width()+20,game_text.get_height()+data_text.get_height()+25))
            pygame.draw.rect(self.window, (0,0,0), (xtext-5,game_text_y-5,data_text.get_width()+10,game_text.get_height()+data_text.get_height()+15))
            self.window.blit(game_text,(game_text_x,game_text_y))
            self.window.blit(data_text,(xtext,ytext))

        pygame.display.flip()


if __name__=="__main__":
    Escape(False)
