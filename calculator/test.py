import tkinter as tk
from xml.etree.ElementTree import Comment #tkinter 임포트하는데 tk로 이름바꾸기

disValue = 0 #결과값 변수만들기
operator = {'+':1, '-':2, '/':3, '*':4, 'C':5, '=':6}
stoValue = 0
opPre = 0

def number_click(value):
    #print('숫자',value)
    global disValue
    disValue = (disValue*10) + value
    str_value.set(disValue)

def clear():
    global disValue, stoValue, opPre
    stoValue = 0
    opPre = 0
    disValue = 0
    str_value.set(disValue)

def operator_click(value):
    #print('명령',value)
    global disValue, operator, stoValue, opPre
    op = operator[value]
    if op == 5: # C
        clear()
    elif disValue == 0:
        opPre = 0
    elif opPre == 0:
        opPre = op
        stoValue = disValue
        disValue = 0
        str_value.set(str(disValue))
    elif op ==6: #'=
        if opPre == 1:
            disValue = stoValue + disValue
        if opPre == 2:
            disValue = stoValue - disValue
        if opPre == 3:
            disValue = stoValue / disValue
        if opPre == 4:
            disValue = stoValue * disValue            

        str_value.set(str(disValue))   
        disValue = 0
        stoValue = 0
        opPre = 0
    else:
        clear()


def button_click(value):
    #print(value)
    try:
        value = int(value)
        number_click(value)
    except:
        operator_click(value)


win = tk.Tk() #Tk 함수만들기
win.title('계산기') #타이틀넣기

str_value = tk.StringVar()
str_value.set(str(disValue)) # 문자로 변환하여 set
dis = tk.Entry(win, textvariable=str_value, justify='right', bg ='white', fg='red') #에디트창에 값 자동으로 업데이트
dis.grid(column=0, row=0, columnspan=4, ipadx=80, ipady=30)

calItem =  [['1','2','3','4'],
            ['5','6','7','8'],
            ['9','0','+','-'],
            ['/','*','C','=']]
for i,items in enumerate(calItem):
    for k,item in enumerate(items):

        try:
            color = int(item)
            color = 'black'  
        except:
            color = 'pink'   


        bt = tk.Button(win, 
            text=item, 
            width=10, 
            height=5,
            bg = color,
            fg = 'white',
            command = lambda cmd=item: button_click(cmd)
            )
        bt.grid(column=k, row=(i+1))       



win.mainloop() #생성한 윈도우 내부에서 수행되는 마우스 클릭 같은 이벤트들이 발생하게끔 유지해주는 함수
