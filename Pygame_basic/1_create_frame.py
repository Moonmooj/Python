import pygame #임포트실행

pygame.init() #초기화 하는 작업(필수요소)

#화면 크기 설정
screen_width = 480 #가로크기
screen_height = 640 #세로크기
screen = pygame.display.set_mode((screen_width, screen_height))

#화면 타이틀 설정
pygame.display.set_caption('Nado Game') #게임 이름

# 이벤트 루프 ( 창이 꺼지지 않게하기위해 )
running = True # 게임이 진행중인지 확인
while running:
    for event in pygame.event.get(): # 어떤 이벤트가 발생했는지 확인
        if event.type == pygame.QUIT: # 창이 닫히는 이벤트가 발생했는지 확인
            running = False # 게임이 진행중이 아님 

# pygame 종료
pygame.quit()