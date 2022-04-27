import sys  # exit함수 사용위해 임포트
from math import sqrt, ceil  # 제곱근 , 올림
import random
import ctypes # 해상도

import pygame  # pygame 임포트
from pygame.locals import QUIT, KEYDOWN, K_UP, K_LEFT, K_RIGHT, K_DOWN, K_SPACE, K_ESCAPE  # pygame의 locals에 정의된 상수(이벤트 입력된값과 비교하는데 사용)를 사용하게위해 임포트트

class Block:  # 필드와는 별개로 사용자입력을 받아야하고, 각각 회전하기도해야함 따라서 class로 만들어 객체활용
    def __init__(self, name):
        self.turn = 0
        self.type = BLOCKS[name]
        self.data = self.type[self.turn]
        self.size = int(sqrt(len(self.data)))
        self.xpos = (WIDTH - self.size) // 2
        self.ypos = 0
        self.stop = 0  # 빨리 떨어지지 않도록

    def update(self):
        global BLOCK
        erased = 0
        if is_overlapped(self.xpos, self.ypos + 1, self.turn):  # 만약 아래로 한칸내렸을때 충돌이 일어나면 블록데이터를 필드로 복사하고 새로운 블록 생성코드
            for y_offset in range(self.size):
                for x_offset in range(self.size):
                    if ((0 <= self.xpos + x_offset < WIDTH) and (0 <= self.ypos + y_offset < HEIGHT)):
                        val = self.data[y_offset * self.size + x_offset]
                        if val != 'B':
                            FIELD[self.ypos + y_offset][self.xpos + x_offset] = val
            BLOCK = get_block()
            erased = erase_line()
            sound_fall.play()
        else:  # 시간이 지남에 따라 블록을 한칸씩 아래로 내리는 코드
            self.stop = self.stop + 1
            if self.stop > FPS / DIFFICULT:
                self.stop = 0
                self.ypos = self.ypos + 1
        return erased

    def draw(self):
        for index in range(len(self.data)):
            xpos = index % self.size
            ypos = index // self.size
            val = self.data[index]
            if ((0 <= ypos + self.ypos < HEIGHT) and (0 <= xpos + self.xpos < WIDTH) and (val != 'B')):
                x_pos = 25 + (xpos + self.xpos) * 25
                y_pos = 25 + (ypos + self.ypos) * 25
                pygame.draw.rect(SURFACE, COLORS[val], (x_pos, y_pos, 24, 24))

    def left(self):
        if not is_overlapped(self.xpos - 1, self.ypos, self.turn):  # 충돌확인
            self.xpos = self.xpos - 1

    def right(self):
        if not is_overlapped(self.xpos + 1, self.ypos, self.turn):  # 충돌확인
            self.xpos = self.xpos + 1

    def down(self):
        if not is_overlapped(self.xpos, self.ypos + 1, self.turn):  # 충돌확인
            self.ypos = self.ypos + 1

    def up(self):
        if not is_overlapped(self.xpos, self.ypos, (self.turn + 1) % 4):  # 충돌확인
            self.turn = (self.turn + 1) % 4
            self.data = self.type[self.turn]

    def hard_drop(self):
        ypos = self.ypos
        while not is_overlapped(self.xpos, ypos + 1, self.turn):
            ypos = ypos + 1
        self.ypos = ypos


def get_block():
    global BLOCK_QUEUE
    # 모든 블록이 한번씩 무작위로 순회
    while len(BLOCK_QUEUE) < len(BLOCKS.keys()) + 1:
        new_blocks = list()
        for name in BLOCKS.keys():
            new_blocks.append(Block(name))
        random.shuffle(new_blocks)
        BLOCK_QUEUE.extend(new_blocks)
    return BLOCK_QUEUE.pop(0)


def is_overlapped(xpos, ypos, turn):
    data = BLOCK.type[turn]
    for y_offset in range(BLOCK.size):  # 블록데이터 전체를 순회하기위한 코드
        for x_offset in range(BLOCK.size):  # 블록데이터 전체를 순회하기위한 코드
            if ((0 <= xpos + x_offset < WIDTH) and (0 <= ypos + y_offset < HEIGHT)):  # 블록이 필드내부에 있게하기위한 방어코드
                if ((data[y_offset * BLOCK.size + x_offset] != 'B') and (
                        FIELD[ypos + y_offset][xpos + x_offset] != 'B')):  # 충돌방지코드/ 같은위치의 필드데이터와 블록데이터가 빈칸인지 확인
                    return True
    return False


def is_game_over():
    filled = 0
    for cell in FIELD[0]:
        if cell != 'B':
            filled += 1
    return filled > 2  # 필드 최상단검사/ 마지막에 두개제외하는 이유는 양옆 벽때문임


def erase_line():  # 새로운 줄 추가할때 양쪽 벽 추가생성!
    erased = 0  # 지울 줄 수 변수
    ypos = HEIGHT - 1
    while ypos >= 0:
        if FIELD[ypos].count('B') == 0 and FIELD[ypos].count('W') == 2:
            erased = erased + 1
            del FIELD[ypos]
            new_line = ['B'] * (WIDTH - 2)
            new_line.insert(0, 'W')
            new_line.append('W')
            FIELD.insert(0, new_line)
            sound_line.play()
        else:
            ypos = ypos - 1
    return erased  # 지운 줄개수에 비례하여 점수를 줘야하기때문에 지운 줄 수 반환


# 전역변수 설정
pygame.init()  # 컴퓨터에게 우리가 pygame을 사용하겠다고 알려줌
pygame.display.set_caption('명주가 만든 테트리스게임')  # 게임 제목설정
pygame.key.set_repeat(30, 30)  # 키보드를 누르고있으면 반복해서 같은키가 눌리도록
pygame.mixer.init()
pygame.mixer.music.load('sound/tetris.mp3')
pygame.mixer.music.play(-1, 0)  # 무한반복
sound_line = pygame.mixer.Sound('sound/fall.mp3')
sound_fall = pygame.mixer.Sound('sound/drop.mp3')
image_bg = pygame.image.load('image/space.jpg')
SURFACE = pygame.display.set_mode([600, 600])  # 게임 창크기설정 (x,y)
FPSCLOCK = pygame.time.Clock()  # 시간객체 설정
WIDTH = 10 + 2  # 필드를 저장할 이차원 배열 선언 너비
HEIGHT = 20 + 1  # 필드를 저장할 이차원 배열 선언 높이
FIELD = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]  # 필드값설정
BLOCK = None  # 사용자가 움직이는 블록을 저장하기 위한 블록전역변수 선언
BLOCK_QUEUE = list()
FPS = 15
DIFFICULT = 1  # 난도 표현 변수

# 블럭종류 설정 ( B는 빈칸 )
BLOCKS = {'J': [('B', 'B', 'J',
                 'J', 'J', 'J',
                 'B', 'B', 'B'),
                ('B', 'J', 'B',
                 'B', 'J', 'B',
                 'B', 'J', 'J'),
                ('B', 'B', 'B',
                 'J', 'J', 'J',
                 'J', 'B', 'B'),
                ('J', 'J', 'B',
                 'B', 'J', 'B',
                 'B', 'J', 'B')],
          'L': [('L', 'B', 'B',
                 'L', 'L', 'L',
                 'B', 'B', 'B'),
                ('B', 'L', 'L',
                 'B', 'L', 'B',
                 'B', 'L', 'B'),
                ('B', 'B', 'B',
                 'L', 'L', 'L',
                 'B', 'B', 'L'),
                ('B', 'L', 'B',
                 'B', 'L', 'B',
                 'L', 'L', 'B')],
          'T': [('B', 'T', 'B',
                 'T', 'T', 'T',
                 'B', 'B', 'B'),
                ('B', 'T', 'B',
                 'B', 'T', 'T',
                 'B', 'T', 'B'),
                ('B', 'B', 'B',
                 'T', 'T', 'T',
                 'B', 'T', 'B'),
                ('B', 'T', 'B',
                 'T', 'T', 'B',
                 'B', 'T', 'B')],
          'Z': [('Z', 'Z', 'B',
                 'B', 'Z', 'Z',
                 'B', 'B', 'B'),
                ('B', 'B', 'Z',
                 'B', 'Z', 'Z',
                 'B', 'Z', 'B'),
                ('B', 'B', 'B',
                 'Z', 'Z', 'B',
                 'B', 'Z', 'Z'),
                ('B', 'Z', 'B',
                 'Z', 'Z', 'B',
                 'Z', 'B', 'B')],
          'S': [('B', 'S', 'S',
                 'S', 'S', 'B',
                 'B', 'B', 'B'),
                ('B', 'S', 'B',
                 'B', 'S', 'S',
                 'B', 'B', 'S'),
                ('B', 'B', 'B',
                 'B', 'S', 'S',
                 'S', 'S', 'B'),
                ('S', 'B', 'B',
                 'S', 'S', 'B',
                 'B', 'S', 'B')],
          'O': [('O', 'O',
                 'O', 'O'),
                ('O', 'O',
                 'O', 'O'),
                ('O', 'O',
                 'O', 'O'),
                ('O', 'O',
                 'O', 'O')],
          'I': [('B', 'I', 'B', 'B',
                 'B', 'I', 'B', 'B',
                 'B', 'I', 'B', 'B',
                 'B', 'I', 'B', 'B'),
                ('B', 'B', 'B', 'B',
                 'I', 'I', 'I', 'I',
                 'B', 'B', 'B', 'B',
                 'B', 'B', 'B', 'B'),
                ('B', 'B', 'I', 'B',
                 'B', 'B', 'I', 'B',
                 'B', 'B', 'I', 'B',
                 'B', 'B', 'I', 'B'),
                ('B', 'B', 'B', 'B',
                 'B', 'B', 'B', 'B',
                 'I', 'I', 'I', 'I',
                 'B', 'B', 'B', 'B')]
          }

# 색깔 변수 설정
COLORS = {'J': (239, 160, 0),
          'L': (1, 1, 240),
          'T': (160, 0, 241),
          'Z': (240, 1, 0),
          'S': (0, 240, 0),
          'O': (239, 240, 5),
          'I': (1, 240, 241),
          'B': (0, 0, 0),
          'W': (127, 127, 127)}


def main():  # 메인함수- 프로그램이 실행된 후 가장 먼저 수행하는 함수/ 게임 무한 루프
    global BLOCK
    Fullscreen = 'Press f, you can play Fullscreen'
    score = 0  # 점수용 변수 선언
    if BLOCK is None:
        BLOCK = get_block()

    smallfont = pygame.font.SysFont(None, 36)  # 점수 변수 그릴 폰트 불러오기  (메시지)
    largefont = pygame.font.SysFont(None, 72)  # 게임오버글씨
    message_over = largefont.render('GAME OVER!!', True, (255, 255, 255))
    message_rect = message_over.get_rect()
    message_rect.center = (300, 300)

    for ypos in range(HEIGHT):
        for xpos in range(WIDTH):
            FIELD[ypos][xpos] = 'W' if xpos == 0 or xpos == WIDTH - 1 else 'B'
    for index in range(WIDTH):
        FIELD[HEIGHT - 1][index] = 'W'

    while True:  # 무한반복/이벤트루프확인
        key = None
        for event in pygame.event.get():
            if event.type == QUIT:  # 게임 종료(종료버튼누른 이벤트)시 발생하는 이벤트
                pygame.quit()  # pygame 프로그램을 종료하려면 꼭 2가지 함수모두 호출해야함(pygame종료, 윈도우창종료)
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == ord('f'):  # 키보드 f를 눌렀을때
                    user32 = ctypes.windll.user32
                    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)  # 해상도 구하기
                    surface = pygame.display.set_mode((600, 600), pygame.FULLSCREEN)  # 600*600 픽셀 풀스크린조절
                key = event.key
                if key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # 게임오버 확인
        if is_game_over():
            SURFACE.blit(message_over, message_rect)
            pygame.mixer.music.stop()  # 음악 중지
        else:  # 게임오버가 아님/ 움직임 처리
            if key == K_UP:
                BLOCK.up()
            elif key == K_RIGHT:
                BLOCK.right()
            elif key == K_LEFT:
                BLOCK.left()
            elif key == K_DOWN:
                BLOCK.down()
            elif key == K_SPACE:
                BLOCK.hard_drop()

            # 필드그리기
            SURFACE.fill((0, 0, 0))
            SURFACE.blit(image_bg, (0, 0))
            for ypos in range(HEIGHT):
                for xpos in range(WIDTH):
                    value = FIELD[ypos][xpos]
                    pygame.draw.rect(SURFACE, COLORS[value],
                                     (xpos * 25 + 25, ypos * 25 + 25, 24, 24))

            erased = BLOCK.update()
            if erased > 0:
                score = score + 2 ** erased
                DIFFICULT = min(ceil(score / 10), 15)  # 10점 쌓일때마다 난도 상승/ 최대난도 15
            BLOCK.draw()

            # 블록 대기열 표현
            ymargin = 0
            for next_block in BLOCK_QUEUE[0:7]:
                ymargin = ymargin + 1
                for ypos in range(next_block.size):
                    for xpos in range(next_block.size):
                        value = next_block.data[xpos + ypos * next_block.size]
                        pygame.draw.rect(SURFACE, COLORS[value], (xpos * 15 + 460, ypos * 15 + 75 * ymargin, 15, 15))

            # 점수나타내기/ 필드를 먼저그리고 그 후에 점수를 나타내야함 /안그러면 필드를 그리기전에 초기화 하는 함수로인해 지워짐
            score_str = str(score).zfill(6)  # 앞숫자 0으로 6개채우는 함수
            score_image = smallfont.render(score_str,
                                           True, (180, 180, 180))
            SURFACE.blit(score_image, (500, 30))

            Fullscreen_image = smallfont.render(Fullscreen, True, (100, 50, 100))
            SURFACE.blit(Fullscreen_image, (20, 570))

        pygame.display.update()  # 변경된 화면 그리기(업데이트)
        FPSCLOCK.tick(FPS)  # 1초에 FPS변수만큼 while 루프가 실행되도록 적절한 휴식시간 생성


if __name__ == '__main__':  #해당소스파일이 메인프로그램인지 확인 /메인이면 main()실행
    main()
