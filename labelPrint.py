import os
import glob
import PySimpleGUI as sg
from PIL import Image, ImageDraw, ImageFont

layout = [
    [sg.Text('от: ', font='Any 14'), sg.InputText('2000', size=(20,1)), sg.Text('кол-во: ', font='Any 14'), sg.InputText('10', size=(20,1))],
    [sg.Text('Размер этикетки:', size=(40,1))],
    [sg.InputText('56', size=(5,1)), sg.Text('x'), sg.InputText('40', size=(5,1)), sg.Checkbox('пустые')],
    [sg.Text('Размер шрифта:')],
    [sg.InputText('28', size=(5,1))],
    [sg.Text('Позиционирование:')],
    [sg.Radio('влево', 'positionX'), sg.Radio('середина', 'positionX', default=True), sg.Radio('вправо', 'positionX')],
    [sg.Radio('вверх', 'positionY'), sg.Radio('середина', 'positionY', default=True), sg.Radio('вниз', 'positionY')],
    [sg.Multiline(size=(88,10), key='-ML-', autoscroll=True, reroute_stdout=True, write_only=True, reroute_cprint=True)],
    [sg.Submit('Печать'), sg.Cancel()]
]
window = sg.Window('Печать этикеток', layout)
while True:                             # The Event Loop
    event, values = window.read()
    # print(event, values) #debug
    if event in (None, 'Exit', 'Cancel'):
        break
    if event == 'Печать':
        startNum = cycleNum = isitago = 0
        imagespath = './images'
        if not os.path.exists(imagespath):
            os.makedirs(imagespath)     

        if values[0] and values[1]:
            startNum = values[0]
            cycleNum = values[1]
            isitago = 1
            if not startNum and startNum is not None:
                print('Введите число, с которого начинать печать')
                isitago = 0
            elif not cycleNum and cycleNum is not None:
                print('Введите последнее число печати')
                isitago = 0
            elif isitago == 1:
                isitago = 0
                mm_to_px = 11.811;
                font_size = int(values[5]) * 10 + 1

                startNum = int(startNum)
                cycleNum = startNum + int(cycleNum) + 1

                files = glob.glob(imagespath + '/d-*')
                for f in files:
                    os.remove(f)

                for x in range(startNum, cycleNum):
                    #os.startfile(123123, "print")
                    
                    w = int(int(values[2]) * mm_to_px)
                    h = int(int(values[3]) * mm_to_px)
                    img = Image.new('RGBA', (w, h), 'white')
                    idraw = ImageDraw.Draw(img)
                    
                    text = str(x)
                    if values[4] == True:
                        text += "-ПУСТО"

                    print('Печатаем этикетку:', text)

                    font = ImageFont.truetype("fonts/Arial.ttf", size=font_size)
                    wi, hi = idraw.textsize(text, font=font)

                    hi += int(font_size/4)

                    if values[7] == True:
                        wn = int((w - wi)/2)
                    elif values[8] == True:
                        wn = int(w - wi - 2)
                    else:
                        wn = 0
                    
                    if values[10] == True:
                        hn = int((h - hi)/2)
                    elif values[11] == True:
                        hn = int(h - hi - 2)
                    else:
                        hn = 0

                    if wn < 0: wn = 0
                    #if hn < 0: hn = 0
                    idraw.text((wn, hn), text, font=font, fill=(0,0,0,255))

                    #idraw.rectangle((10, 10, 100, 100), fill='blue')
                    img.save(imagespath + '/d-' + str(x) + '.png', dpi=(300, 300))
                    #os.startfile('images/rectangle.png', "print")
        else:
            sg.cprint('Введите числа для печати этикеток')
        
        path="./images"
        path=os.path.realpath(path)
        os.startfile(path)

window.close()
