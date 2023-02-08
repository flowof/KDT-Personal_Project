import sys                 #os 임포트
from math import sqrt      #제곱근
from random import randint 
import threading
#from typing_extensions import runtime
import time
import datetime
import pygame
from pygame import surface
from pygame.constants import K_p, K_s
from pygame.locals import QUIT, KEYUP, KEYDOWN, K_LEFT, K_RIGHT, K_DOWN, K_SPACE, K_PAUSE
#from pygame.locals import QUIT,KEYDOWN,K_LEFT,K_RIGHT,K_DOWN, K_SPACE

BLOCK_DATA = (       # 3차원데이터(라서 괄호 3개). BLOCK_DATA[블록종류][블록방향][데이터번호]
    (
        (0, 0, 1, \
         1, 1, 1, \
         0, 0, 0),
        (0, 1, 0, \
         0, 1, 0, \
         0, 1, 1),
        (0, 0, 0, \
         1, 1, 1, \
         1, 0, 0),
        (1, 1, 0, \
         0, 1, 0, \
         0, 1, 0),
    ), (
        (2, 0, 0, \
         2, 2, 2, \
         0, 0, 0),
        (0, 2, 2, \
         0, 2, 0, \
         0, 2, 0),
        (0, 0, 0, \
         2, 2, 2, \
         0, 0, 2),
        (0, 2, 0, \
         0, 2, 0, \
         2, 2, 0)
    ), (
        (0, 3, 0, \
         3, 3, 3, \
         0, 0, 0),
        (0, 3, 0, \
         0,  3, 3, \
         0, 3, 0),
        (0, 0, 0, \
         3, 3, 3, \
         0, 3, 0),
        (0, 3, 0, \
         3, 3, 0, \
         0, 3, 0)
    ), (
        (4, 4, 0, \
         0, 4, 4, \
         0, 0, 0),
        (0, 0, 4, \
         0, 4, 4, \
         0, 4, 0),
        (0, 0, 0, \
         4, 4, 0, \
         0, 4, 4),
        (0, 4, 0, \
         4, 4, 0, \
         4, 0, 0)
    ), (
        (0, 5, 5, \
         5, 5, 0, \
         0, 0, 0),
        (0, 5, 0, \
         0, 5, 5, \
         0, 0, 5),
        (0, 0, 0, \
         0, 5, 5, \
         5, 5, 0),
        (5, 0, 0, \
         5, 5, 0, \
         0, 5, 0)
    ), (
        (6, 6, 6, 6), # 회전한 모습과 회전하지 않은 모습이 똑같은 모양
        (6, 6, 6, 6), # \로 칸 구분 안함
        (6, 6, 6, 6),
        (6, 6, 6, 6)
    ), (
        (0, 7, 0, 0, \
         0, 7, 0, 0, \
         0, 7, 0, 0, \
         0, 7, 0, 0),
        (0, 0, 0, 0, \
         7, 7, 7, 7, \
         0, 0, 0, 0, \
         0, 0, 0, 0),
        (0, 0, 7, 0, \
         0, 0, 7, 0, \
         0, 0, 7, 0, \
         0, 0, 7, 0),
        (0, 0, 0, 0, \
         0, 0, 0, 0, \
         7, 7, 7, 7, \
         0, 0, 0, 0)
    )
)

class Block:
    '''블록모양으로 낙하하는 모양의 객체'''    
    def __init__(self, count):
        '''
        <<randint(a, b)>>
        반환하는 x는  a, b를 포함한 범위 입니다. (a <= N <= b)
        x = random.randint(10, 20) # 10 <= x <= 20 사이의 랜덤한 정수(int)를 반환
        print(x)
        
        =>(동일동작) randrange(a, b+1)# 10 <= x < 20 사이의 랜덤한 int 반환
        '''
        self.turn = randint(0, 3) # 인덱스번호2번 | 회전블록의 방향(0~3)
        self.type = BLOCK_DATA[randint(0, 6)] #BLOCK_DATA 타입 7개 중 1 저장-1차원데이터:BLOCK_DATA[블록종류][][] | 블록(0~6) 2차원 데이터(4방향분)
        self.data = self.type[self.turn] # 인덱스번호3번 | 블록 1차원 데이터(현재의 방향만) 위의 속성을 이용해 data에 블록 배열을 설정
        self.size = int(sqrt(len(self.data))) # 데이터수를 제곱근 하면 3,2,4, len(self.data) 9개,4개,16개 | 가로와 세로는 같음
        self.xpos = randint(2, 8 - self.size) #(8 - 2 or 3 or 4)=6 or 5 or 4 | 양벽 2 제외,데이터가 내려오는 10개의 칸 중 위치가 정해짐 | 블록의 X좌표를 난수로 초기화
        self.ypos = 1 - self.size #블럭의 위치 중 가장 윗 부분 | 블록의 Y좌표 초기화(마지막  1줄부터 보이기 시작)
        self.fire = count + INTERVAL # 블럭 낙하하기 시작하는 시간 | 블록은 일정 간격(INTERVAL)로 낙하

    def update(self, count): # 블록의 낙하(이동)를 처리하는 메서드
        '''블록 상태 갱신(소거한 단의 수를 반환한다)'''
        # 아래로 충돌?
        erased = 0
        if is_overlapped(self.xpos, self.ypos + 1, self.turn): #is_overlapped는 블록이 겹치는지 여부를 반환하는 함수, Y좌표를 +1 한 상태에서 겹치는지 확인
            for y_offset in range(BLOCK.size):     #y_offset과 x_offset은 순환변수
                for x_offset in range(BLOCK.size): #just 위치 계산을 위해 순환되는 변수
                    if 0 <= self.xpos+x_offset < WIDTH and \
                        0 <= self.ypos+y_offset < HEIGHT:       # self.ypos_offset가 0부터 HEIGHT의 범위에 들어가
                        val = BLOCK.data[y_offset*BLOCK.size \
                                            + x_offset]
                        if val != 0: # BLOCK의 칸 val이 0이 아니라면
                            FIELD[self.ypos+y_offset]\
                                 [self.xpos+x_offset] = val # FIELD에 복사함

            erased = erase_line() # 행삭제
            go_next_block(count) #다음 블록으로 전환함

        if self.fire < count: # count는 현재시각, self.fire은 낙하시작시간이므로 낙하중이면
            self.fire = count + INTERVAL #다음 이동시각(낙하시작시간)을 count + INTERVAL로 설정
            self.ypos += 1 # 1단 아래로 이동함
        return erased

    def draw(self): #블록을 그리는 메서드
        '''블록을 그린다'''
        for index in range(len(self.data)): #블록데이터는 1차원이기 때문에 for문을 이용해서 0부터 배열의 길이까지 반복함
            xpos = index % self.size  # index를 나눈 나머지
            ypos = index // self.size # index를 나눈 몫(정수)
            val = self.data[index] #데이터 값 ???????????????????????????????????????????????????????????????????????????????????????????????????????????
            if 0 <= ypos + self.ypos < HEIGHT and \
               0 <= xpos + self.xpos < WIDTH and val != 0: #ypos + self.ypos와 xpos + self.xpos가 FIELD의 범위에 들어가고 val(데이터)가 0이 아니면 그 칸을 그림
                x_pos = 25 + (xpos + self.xpos) * 25
                y_pos = 25 + (ypos + self.ypos) * 25
                pygame.draw.rect(SURFACE, COLORS[val],
                                 (x_pos, y_pos, 24, 24)) #"""그리는 좌표는 (x_pos, y_pos)를 왼쪽으로 하는 (24,24)영역. 한칸은 25인데, 24*24만 그리므로 중간에 검정색 선이 표현됨. 색상은 COLORS[val]로 구함"""

def erase_line():
    
    erased = 0
    ypos = 20 # HEIGHT22, 아래벽1 제외 0~20으로 21줄? ypos를 20으로 초기화하고
    while ypos >= 0: # 아래줄부터 위방향으로 행을 조사해 나감
        
        '''
        all함수
        괄호 안의 모든 요소가 참이거나 혹은 괄호가 비어 있다면 True 를 반환하고, 그 외의 경우에는 False 를 반환하는 함수
        all([]) -> True
        출처: https://codepractice.tistory.com/87 [코딩 연습]

         
        '''
        if all(FIELD[ypos]): # all함수는 인수의 배열요소가 모두 True면 True 반환. FIELD[ypos]는 ypos번째 행의 배열. 그 요소가 0이 아니면, 즉 행 전부가 어떤 블록으로 가득차 있으면 True???????????????????????????????????????
            erased += 1 #if문이 성립하면 삭제한 행의 카운터 erased를 +1
            del FIELD[ypos]
            FIELD.insert(0, [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8]) #insert메서드 이용 -> 한 줄 추가(8은 양 벽)
        else: #all함수가 False라면
            ypos -= 1 # ypos의 값을 하나 줄이고 while문 계속 진행
    return erased

def is_game_over(): # 게임오버인지 판정하는 함수
    '''게임 오버인지 아닌지'''
    filled = 0
    for cell in FIELD[0]: # FIELD[0]은 0번째 행이므로 for문을 이용해서
        if cell != 0: # 가장 위의 행에 0이 아닌 칸을 셈
            filled += 1
    return filled > 2 # 2(좌우 벽)보다 크면 맨 위까지 쌓인 것으로 True를 반환함 

def go_next_block(count): # 낙하 중인 블록을 다음 블록으로 바꾸는 함수
    '''다음 블록으로 전환한다'''
    global BLOCK, NEXT_BLOCK # 전역변수 내용을 바꿔야 하므로 global 선언
    BLOCK = NEXT_BLOCK if NEXT_BLOCK != None else Block(count) #BLOCK값 갱신 | if NEXT_BLOCK != None 조건이 성립하면 NEXT_BLOCK, 그렇지 않으면 Block(count)로 새 블록을 만들고
    NEXT_BLOCK = Block(count) # 만든 새 블록을 대입함

def is_overlapped(xpos, ypos, turn): # 좌표 xpos, ypos에서 방향이 turn의 블록이 벽이나 다른 블록과 충돌하는지 여부를 반환하는 함수
    '''블록이 벽이나 땅의 블록과 출동하는지 아닌지'''
    data = BLOCK.type[turn] # 현재의 방향 데이터를 취득
    for y_offset in range(BLOCK.size):
        for x_offset in range(BLOCK.size):
            if 0 <= xpos+x_offset < WIDTH and \
                0 <= ypos+y_offset < HEIGHT:
                if data[y_offset*BLOCK.size + x_offset] != 0 and \
                    FIELD[ypos+y_offset][xpos+x_offset] != 0: # 블록에 숫자가 있고 그 자리에 숫자가 이미 있으면
                    return True # 충돌이라고 판정(BLOCK의 세로방향y_offset, 가로방향x_offset의 이중루프 사용)
    return False


# def startTimer():
#     timer = threading.Timer(5, startTimer)
#     timer.start()
 
# if __name__ == '__main__':
#     startTimer()

'''
전역변수
'''
pygame.init()
pygame.key.set_repeat(10, 10) # => set.repeat(지연시간, 간격)
SURFACE = pygame.display.set_mode([600, 600])
FPSCLOCK = pygame.time.Clock()
WIDTH = 12 # FIELD의 폭 | 양 벽 포함 x축
HEIGHT = 22 # FIELD의 높이
INTERVAL = 40 # 블록 낙하 간격
FIELD = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)] #벽과 겹쳐진 블록의 상태를 유지하는 2차원 배열 | FIELD는 현재 테트리스의 상태 = 블록이 쌓여 있는 상태

# => RGB로만 되어 있어 색깔 파악이 어렵다고 생각함 -> 변수 설정을 해주고, 색깔을 바꿔봄
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 102, 0)
SUNFLOWER = (255, 165, 0)
BLUE = (0, 51, 204)
lightBLUE = (0, 102, 255)
NEONBLUE = (0, 255, 255)
GREEN = (0, 128, 0) # LIGHTGREEN  = ( 20, 175,  20)
NEONGREEN = (0, 255, 0)
PINK = (255, 102, 255)
YELLOW = (255, 204, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
LIGHTGRAY = (185, 185, 185)
CHARCOALGRAY = (28, 28, 28)


COLORS = (BLACK, ORANGE, BLUE, NEONBLUE, GREEN, PINK, YELLOW, RED, GRAY)      
BLOCK = None # 현재 낙하중인 블록객체
NEXT_BLOCK = None # 다음에 낙하하는 블록객체

def get_key():
    key = None
    for event in pygame.event.get():                  
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:                    
            key = event.key
    return key



def main():
    
    global begin
    global INTERVAL #전역변수인 INTERVAL을 main에서 수정하기 위해 global선언
    count = 0 # 시간을 관리하는 카운터
    score = 0 # 점수
    game_over = False # 게임오버 여부의 프래그
    smallfont = pygame.font.SysFont(None, 24) # 점수표시
    mediumfont = pygame.font.SysFont(None, 34) #                => 일지정지표시
    largefont = pygame.font.SysFont(None, 72) # GAME OVER!! 표시
    message_over = largefont.render("GAME OVER!!", True, NEONBLUE)
    message_rect = message_over.get_rect()
    message_rect.center = (300, 300) # 메시지 초기화

  
    # => 일시정지 메시지 만들기
#    message_pause = mediumfont.render("PAUSE", True, lightBLUE)
#    message_rect1 = message_pause.get_rect()
#    message_rect1.center = (300, 300)

    go_next_block(INTERVAL) # 다음에 낙하하는 블록을 초기화

    for ypos in range(HEIGHT):
        for xpos in range(WIDTH): # 2차원 배열 초기화
            FIELD[ypos][xpos] = 8 if xpos == 0 or \
                xpos == WIDTH - 1 else 0 #이중루프로 좌우벽을 8로, 공백을 0으로 채움
    for index in range(WIDTH):
        FIELD[HEIGHT-1][index] = 8 # 바닥벽을 8로 채움

    while True: # 메인루프
        key = None
        for event in pygame.event.get(): #키보드나 마우스 입력값(이벤트) 체크해 주는 것
            if event.type == QUIT: # 윈도우 닫기 버튼 눌렸을 때 프로그램 종료하도록 처리
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                key = event.key
#            elif event.type == KEYUP:
#                SURFACE.fill(BLACK)
#                showTextScreen('Paused')

               
        # runtime = "runtime:{}".format(result)
        # message_time = smallfont.render(runtime, True, SUNFLOWER)
        # SURFACE.blit(message_time, (370, 50))               

        game_over = is_game_over() # 게임오버인지 판정하는 함수
        if not game_over: #게임오버 아니면
            count += 5 # 카운트 5씩 늘림
            if count % 1000 == 0: #카운트가 1000의 배수가 되면
                INTERVAL = max(1, INTERVAL - 2) #1 넘지 않되(max), INTERVAL 2씩 감소하여 블록 낙하속도가 점점 빨라짐
            erased = BLOCK.update(count) # BLOCK.update로 블록을 이동하고, 삭제한 행수가 반환됨

            if erased > 0:
                score += (2 ** erased) * 100 # 삭제한 행수를 바탕으로 점수를 더함. 1행을 지우면 2^1=2, 2행을 지우면 2^2=4, 3행을 지우면 2^3승으로 8(**은 거듭제곱)
        # else: # 게임오버 되면
        #     return(game_over_time)
            
            # 키 이벤트 처리
            next_x, next_y, next_t = \
                BLOCK.xpos, BLOCK.ypos, BLOCK.turn # 현재의 X좌표, Y좌표, 방향을 대입함
            if key == K_SPACE:
                pygame.key.set_repeat() # 입력된 키에 따라서 각각의 변수값을 생성
                next_t = (next_t + 1) % 4
            elif key == K_RIGHT:
                next_x += 1
            elif key == K_LEFT:
                next_x -= 1
            elif key == K_DOWN: # 아래쪽 화살표를 계속 누르면 빠르게 하강 => 꾹 눌러도 빨리 내려가게 하고 싶어!!!!!
                next_y += 1
                
            elif key == K_s:
                while get_key() != K_s:
                    pass
                '''
                while문을 만들어서 일시정지가 되게끔 만든 def k_s로 보냄
                while 문 안에 get_key() 로 접근해 일시정지가 되게끔 만들고 다시 진행을 원하면 s를 눌러 while문을 pass하도록 만듬.
                
                        
                '''

            if not is_overlapped(next_x, next_y, next_t): # 키 조작한 결과가 겹치지 않는다면
                BLOCK.xpos = next_x # 키 조작을 유효로 하고
                BLOCK.ypos = next_y 
                BLOCK.turn = next_t # 속성?특성? 갱신
                BLOCK.data = BLOCK.type[BLOCK.turn] # 충돌하면 키처리를 안함

        # 전체&낙하 중인 블록 그리기
        SURFACE.fill(CHARCOALGRAY) # 전체 검은색으로 칠함  => 선이 보이도록 배경색 변경
        for ypos in range(HEIGHT):
            for xpos in range(WIDTH):
                val = FIELD[ypos][xpos]
                '''
                메소드 : pygame.draw.rect -> pygame.draw.rect(Surface, color, Rect, Width=0)
                도형 : 사각형
                설명 : 화면에 사각형을 그려줌

                출처: https://kkamikoon.tistory.com/120 [컴퓨터를 다루다]
                '''
                pygame.draw.rect(SURFACE, COLORS[val],
                                 (xpos*25 + 25, ypos*25 + 30, 24, 24)) # FIELD를 그림  => 게임보드?가 너무 왼쪽으로 치우친 것 같아 오른쪽으로, 아래쪽으로 조정함
        BLOCK.draw() # 낙하 중인 블록 그림

        # 다음 블록 그리기
        for ypos in range(NEXT_BLOCK.size):
            for xpos in range(NEXT_BLOCK.size):
                val = NEXT_BLOCK.data[xpos + ypos*NEXT_BLOCK.size]
                pygame.draw.rect(SURFACE, COLORS[val],
                                 (xpos*25 + 430, ypos*25 + 80, 24, 24)) # 24로 설정한건 검은색 선 나타내려고. 다음블록의 위치!! => 위치 옮김

        '''
        플레이어가 키를 누를 때까지 화면 중간에 커다란 글씨를 보여줌
        def showTextScreen(text):
            # 이 함수는 플레이어가 키를 누를때 까지 화면 중간에 커다란 글씨를 그려서 보여준다.

            # 텍스트의 그림자 효과를 그린다.
            titleSurf, titleRect = makeTextObjs(text,BIGFONT,TEXTSHADOWCOLOR)
            titleRect.center = (int(WINDOWWIDTH/2),int(WINDOWHEIGHT/2))
            DISPLAYSURF.blit(titleSurf,titleRect)

            # drawing text
            titleSurf,titleRect = makeTextObjs(text,BIGFONT,TEXTCOLOR)
            titleRect.center = (int(WINDOWWIDTH/2)-3,int(WINDOWHEIGHT/2)-3)
            DISPLAYSURF.blit(titleSurf,titleRect)

            # drawing "Press a Key to Play"
            pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play',BASICFONT,TEXTCOLOR)
            pressKeyRect.center = (int(WINDOWWIDTH/2),int(WINDOWHEIGHT)+100)
            DISPLAYSURF.blit(pressKeySurf,pressKeyRect)

            while checkForKeyPress() == None:
                pygame.display.update()
                FPSCLOCK.tick()
            '''
        # => 시간 나타내기
        # begin = time.time() # 타이머 시작점
        # game_over_time = time.time()- begin # 타이머 종료점
        # result1 = time.strftime("%H:%M:%S", time.gmtime(game_over_time))
        
        # print(type(begin))
        # print(type(end))
                      
        # time1 = datetime.strptime('00:00:00',"%H:%M:%S" )
        # time2 = datetime.strptime(game_over,"%H:%M:%S" )
               
        # time_interval = time2 - time1
        
        
        begin = time.time() #begin = str(begin)
        end = time.time()-begin
        sec = end - begin
        result = datetime.timedelta(seconds=sec) 
        
        runtime = "runtime:{}".format(result)
        message_time = smallfont.render(runtime, True, SUNFLOWER)
        SURFACE.blit(message_time, (340, 50))
        
        
        # 점수 나타내기
        '''
        숫자 출력 시 앞에 0 붙여주고 싶을 때
        방법1) zfill()
        방법2) rjust(width, [fillchar]) 
        '''
        score_str = str(score).rjust(6, "0") # => rjust 함수 사용해 봄, 결과는 똑같음 type은 str
        nowscore_str = "NOW SCORE:{}".format(score_str)
        score_image = smallfont.render(nowscore_str, True, SUNFLOWER) # => 색깔 바꿈
        SURFACE.blit(score_image, (340, 30)) # 점수 표시 # 다음 블록 그림 # 점수 위치 NEXT_BLOCK 보다 위쪽 오른쪽에 표시됨 => 위치 글씨까지 나옥게 위치 조정
        if game_over:
            
            # end = time.time()
            # result = end - begin
            # result = round(result,3)
            # result = str(result)
            # message_time = smallfont.render(result, True, SUNFLOWER)
            # SURFACE.blit(message_time, (370, 50))
            
            
            
            SURFACE.blit(message_over, message_rect) # 게임오버 시 메시지 표시

        pygame.display.update() # 그린 내용을 화면에 반영하고
        FPSCLOCK.tick(15) # 프레임레이트 조정

if __name__ == '__main__':
    main()


# 시간 나타내기
# 일시정지하기 ------ 이건 넘모 어려웡..
# 다운키 꾹 누르면 더 빠르게 내려가기 ----- '꾹'을 어떻게 인식시켜줘야 하는지 모르게씀..