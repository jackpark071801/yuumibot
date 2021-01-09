import pyautogui
import time
import keyboard
import os
from PIL import Image
import cv2
import math
import numpy as np
import mouse
from PIL import ImageFilter
import random
pyautogui.FAILSAFE = False

#bot parameters
global elapsed
elapsed = 0
global iterations
iterations = 0

#game parameters
items = ["Spellthief\'s Edge", 'Faerie Charm', 'Faerie Charm', 'Null-Magic Mantle', 'Chalice of Harmony', 'Amplifying Tome', 'Fiendish Codex', "Athene\'s Unholy Grail", 'Faerie Charm', 'Faerie Charm', 'Forbidden Idol', 'Amplifying Tome', 'Aether Wisp', 'Ardent Censer', 'Needlessly Large Rod', 'Needlessly Large Rod', "Rabadon\'s Deathcap", 'Amplifying Tome', 'Fiendish Codex', 'Amplifying Tome', 'Aether Wisp', 'Twin Shadows', 'Amplifying Tome', 'Lost Chapter', "Luden\'s Echo"]
in_game_text = ['I have a great feeling about this game!', 'This is too easy with teammates like you!', 'Nice job!']
end_game_text = ['Good effort teammates was very fun playing with you! :)', "I don't care what anyone says, all of you are amazing!", 'Good job enemy team, you all played very well! ;)']
r_text_all_chat = ['Ha! Take this!', "Hey! That's not very nice :(", 'meOW! Stop that!', 'Stranger danger!', 'Pick on someone your own size']
r_text_team_chat = ["I'll save you!", "Why aren't they scared of a kitty like me?", "This is why I don't talk to strangers", "We've got this!", 'They can hurt us in game, but not in real life :)']
item_gold = [400, 125, 125, 450, 100, 435, 465, 400, 125, 125, 550, 435, 415, 650, 1250, 1250, 1100, 435, 465, 435, 415, 650, 435, 865, 1900]
ap = [21, 42, 42, 42, 42, 42, 62, 77, 102, 107, 112, 112, 132, 142, 172, 232, 292, 409, 437, 458, 486, 500, 507, 535, 563, 633]

#yuumi properties
global side
side = 0 # 0 is left     1 is right
global status
status = 0
#0 is unmounted, 1 is mounted, 2 is dead, 3 is other
global level
level = 0
global levelValue
levelValue = 0
levellist = ['e','q','e','w','e','r','e','w','e','w','r','w','q','q','q','r','q','q']
global healthfracs
healthfracs = [1,1,1,1]
global item
item = 0
global gold
gold = 500
global current_ap
current_ap = 0
global e_availability
e_availability = 1
global w_availability
w_availability = 1
global r_availability
r_availability = 0
#0 is other, 1 is available, 2 is oom
admaxhp = [641,730,819,908,997,1086,1175,1264,1353,1442,1530,1619,1708,1797,1886,1975,2064,2153]
global e_level
e_level = 0
global r_level
r_level = 0
global buying
buying = 1
global purchaseFailure
purchaseFailure = 0
global champsStatus
champsStatus = [1,1,1,1]
global attached
attached = 'f5'
global attaching
attaching = 0
#0 is not trying to attach and 1 is trying to attach
global rTeamChats
rTeamChats = [0,0,0,0,0]
global rAllChats
rAllChats = [0,0,0,0,0]
global last_e_ping
last_e_ping = 0
global last_r_ping
last_r_ping = 0
global ward
ward = 1
ward_spots = [(1867,1012),(1844,1020),(1867,968),(1830,982),(1762,930),(1788,923),(1750,890),(1731,897),(1733,941),(1812,988),(1878,1046)]
global mounted_frac
mounted_frac = 1


#Helper Functions

#Yuumi Functions
def level_up():
    global level
    global e_level
    global r_level
    keyboard.press_and_release('ctrl+'+levellist[level])
    if levellist[level]=='e':
        e_level+=1
    elif levellist[level]=='r':
        r_level+=1
    level+=1


def update_level(image):
        global levelValue
        pixel1 = image.getpixel((630,1050))
        pixel2 = image.getpixel((624,1056))
        pixel3 = image.getpixel((624,1044))
        pixel4 = image.getpixel((636,1056))
        pixel5 = image.getpixel((636,1044))
        templevelValue = sum(pixel1)*sum(pixel2)-sum(pixel3)*sum(pixel5)+sum(pixel4)
        if not templevelValue == levelValue:
            level_up()
            levelValue = templevelValue


def get_gold_digit(image, digit):
    #digit 0, 1, 2, 3 (from left to right)
    bucketCase = 0

    color = image.getpixel((1208+3+digit*15,1049))
    if color[0] == 233:
        return 3
    elif color[0] == 250:
        return 0
    elif color[0] == 197:
        return 7
    elif color[0] == 255:
        bucketCase = 1

    color = image.getpixel((1208+7+digit*15,1060))
    if color[0] == 255:
        return 1
    elif color[0] == 250:
        return 2
    elif color[0] == 151:
        return 4

    color = image.getpixel((1208+6+digit*15,1062))
    if color[0] == 218:
        return 6
    elif color[0] == 188:
        return 8

    color = image.getpixel((1208+13+digit*15,1049))
    if color[0] == 0:
        return 5

    if bucketCase:
        return 9
    else:
        return -1

def get_gold(image):
    tempgold = get_gold_digit(image, 0)

    digit = get_gold_digit(image, 1)
    if digit==-1:
        return tempgold

    tempgold = int(str(tempgold) + str(digit))

    digit = get_gold_digit(image, 2)
    if digit==-1:
        return tempgold

    tempgold = int(str(tempgold) + str(digit))

    digit = get_gold_digit(image, 3)
    if digit==-1:
        return tempgold

    tempgold = int(str(tempgold) + str(digit))

    return tempgold


def attach_to_champ(champ, wait):
    global attaching
    global attached
    global mounted_frac
    attaching = 1
    x = 1724 + 56*(int(champ[1])-2)
    pyautogui.moveTo(x,822)
    time.sleep(0.1)
    keyboard.press_and_release('w')
    pyautogui.moveTo(960, 540)
    if wait == -1:
        while(1==1):
            update_status(pyautogui.screenshot())
            update_champs_status(pyautogui.screenshot())
            time.sleep(1)
            if status == 1:
                attached = champ
                return 1
            elif status == 2:
                return 0
            elif not champsStatus[int(champ[1])-2]:
                return 0
    time.sleep(wait)
    update_status(pyautogui.screenshot())
    if status == 1:
        attached = champ
        mounted_frac = healthfracs[(int(champ[1])-2)]
        return 1
    else:
        return 0

def update_champs_status(image):
    global champsStatus
    champsStatus = [0,0,0,0]
    if(106<image.getpixel((1910,831))[0]<110):
        champsStatus[3] = 1
    if(111<image.getpixel((1770,831))[0]<115):
        champsStatus[1] = 1
    if(113<image.getpixel((1840,831))[0]<117):
        champsStatus[2] = 1
    if(131<image.getpixel((1700,831))[0]<135):
        champsStatus[0] = 1

def available_champ():
    if champsStatus[3] == 1:
        return 'f5'
    if champsStatus[1] == 1:
        return 'f3'
    if champsStatus[2] == 1:
        return 'f4'
    else:
        return 'f2'

def buy_items(image):
    global item
    global buying
    if(item>22):
        return
    global gold
    global ward
    gold = get_gold(image)
    if(gold >= item_gold[item]):
        time.sleep(.5)
        keyboard.press_and_release('p')
        time.sleep(.5)
        keyboard.press_and_release('ctrl+l')
        time.sleep(.5)
        keyboard.write(items[item])
        time.sleep(.5)
        keyboard.press('down')
        keyboard.press_and_release('enter')
        keyboard.release('down')
        time.sleep(.5)
        keyboard.press_and_release('esc')
        time.sleep(.5)
        pre_gold = gold
        gold = get_gold(pyautogui.screenshot())
        if(gold < pre_gold):
            item += 1
            buy_items(pyautogui.screenshot())
        else:
            buying = 0
    else:
        time.sleep(max(0,3-(elapsed/(1200))))
        buying = 0
def get_ap():
    global current_ap
    current_ap = ap[item]
    current_ap += (level - 1) * 7/3

def update_yuumi_properties(image):
    #e
    global e_availability
    ePixel = image.getpixel((900,985))
    if(ePixel == (33, 231, 99)):
        e_availability = 1
    elif(ePixel ==(16,171,189)):
        e_availability = 2
    else:
        e_availability = 0

    #status
    update_status(image)

    #w
    global w_availability
    wPixel = image.getpixel((799,940))
    w_availability = 1
    if wPixel[0]>200:
        w_availability = 0

    #r
    global r_availability
    r_availability = 0
    rPixel = image.getpixel((951,975))
    if rPixel[0]==229 and rPixel[1]==165 and rPixel[2]==189:
        r_availability = 1
    elif rPixel[0]==36 and rPixel[1]==172 and rPixel[2]==212:
        r_availability = 2

    #level
    update_level(pyautogui.screenshot())

    #champsstati
    update_champs_status(pyautogui.screenshot())

    #update healths
    update_hps(pyautogui.screenshot())
    global mounted_frac
    if mounted_frac < healthfracs[int(attached[1])-2]:
        mounted_frac = healthfracs[int(attached[1])-2]


    #update ward status
    wardPixel = image.getpixel((1286,959))
    if wardPixel[0]==163 and wardPixel[1]==146 and wardPixel[2]==23:
        ward = 1
    else:
        ward = 0


def findWhite(image):
    found = 0
    y = 836
    x = 1690
    try:
        while not found:
            y += 1
            if y==1080:
                y = 836
                x += 30
            if(image.getpixel((x,y))[0]>250):
                found = 1

        #try going left
        found = 0
        xprobe = x
        while not found:
            xprobe -= 1
            if(image.getpixel((xprobe,y))[0]<=250):
                found = 1
                x = xprobe + 1

        #check for horizontal
        xprobe = min(x+6,1920)
        found = 0
        if(image.getpixel((xprobe,y))[0]>250):
            found = 1

        if(found):
            #check for vertical line under
            found = 0
            yprobe = min(y + 6,1080)
            if(image.getpixel((x,yprobe))[0]>250):
                found = 1
            #return value if top left corner found
            if(found):
                return (x+32,y+19)

            #check for vertical line above
            yprobe = max(y - 6, 836)
            if(image.getpixel((x,yprobe))[0]>250):
                found = 1
            #return value if bottom left corner found
            if(found):
                return (x+32,y-19)

        #try going right
        found = 0
        xprobe = x
        while not found:
            xprobe += 1
            if(image.getpixel((xprobe,y))[0]<=250):
                found = 1
                x = xprobe-1

        #check horizontal
        xprobe = min(x-6,1920)
        found = 0
        if(image.getpixel((xprobe,y))[0]>250):
            found = 1

        if(found):
            #check for vertical line under
            found = 0
            yprobe = min(y + 6,1080)
            if(image.getpixel((x,yprobe))[0]>250):
                found = 1
            #return value if top right corner found
            if(found):
                return (x-33,y+19)

            #check for vertical line above
            yprobe = max(y-6, 836)
            if(image.getpixel((x,yprobe))[0]>250):
                found = 1

            if(found):
                return (x-33,y-19)
    except:
        print("white foundn't")


    return (0,0)

def e_healing():
    return 35*(e_level + 1) + 0.4 * current_ap

def update_status(image):
    global attaching
    global status
    wPixel = image.getpixel((800,985))
    if wPixel == (101, 12, 47):
        status = 0
    elif 165>wPixel[0]>150 and 110<wPixel[1]<125 and 45<wPixel[2]<65:
        status = 1
        attaching = 0
    elif wPixel == (51,22,34):
        status = 2
        attaching = 0
    else:
        status = 3
        attaching = 0

def actions(image):
    global buying
    global attached
    global last_e_ping
    global last_r_ping
    if ward:
        x,y = findWhite(pyautogui.screenshot())
        ward(x,y)
    if(status == 0):
        if champsStatus[int(attached[1])-2]==0: #dead

            if side==0:
                if attaching == 0:
                    pyautogui.moveTo(1690,1060)
                    pyautogui.mouseDown(button="right")
                    time.sleep(0.1)
                    pyautogui.mouseUp(button="right")
                    time.sleep(0.5)
            else:
                if attaching == 0:
                    pyautogui.moveTo(1900,855)
                    pyautogui.mouseDown(button="right")
                    time.sleep(0.1)
                    pyautogui.mouseUp(button="right")
                    time.sleep(0.5)
            if elapsed<10*60:
                time.sleep(4)
                keyboard.press_and_release('b')
                time.sleep(8)
                buying = 1
            else:
                buying = 0

        if buying:
            buy_items(pyautogui.screenshot())
        im = pyautogui.screenshot()
        x,y = findWhite(im)
        blue = blue_pct(x,y,im)
        if not buying:
            attach_to_champ(available_champ(),-1)


    elif(status == 1):
        buying = 1

        if side==0:
            if get_gold(pyautogui.screenshot()) >= item_gold[item] and findWhite(pyautogui.screenshot())[0] < 1705 and findWhite(pyautogui.screenshot())[1] > 1049:
                attach_to_champ(attached,0.1)
                buy_items(pyautogui.screenshot())
                attach_to_champ(available_champ(),-1)
        else:
            if get_gold(pyautogui.screenshot()) >= item_gold[item] and findWhite(pyautogui.screenshot())[0] > 1895 and findWhite(pyautogui.screenshot())[1] < 862:
                attach_to_champ(attached,0.1)
                buy_items(pyautogui.screenshot())
                attach_to_champ(available_champ(),-1)
        im = pyautogui.screenshot()
        x,y = findWhite(im)
        red = red_pct(x,y,im)
        blue = blue_pct(x,y,im)
        print("Red is : "+str(red))
        print("Blue is : "+str(blue))
        i = 0
        if elapsed>20*60 and w_availability:
            for i in range(4):
                if blue >= 2 and healthfracs[i]==0.6 and champsStatus[i]==1 and (int(attached[1])-2)!=i and healthfracs[(int(attached[1])-2)] >= 0.9:
                    previous = attached
                    attach_to_champ(attached,0.3)
                    attach_to_champ('f'+str(i+2),2)
                    if status == 0:
                        attach_to_champ(previous,-1)
                    i = 4

            if blue >= 2 and attached != available_champ() and champsStatus[int(available_champ()[1])-2] and healthfracs[int(attached[1])-2] >= 0.9:
                previous = attached
                attach_to_champ(attached,0.3)
                attach_to_champ(available_champ(),2)
                if status == 0:
                    attach_to_champ(previous,-1)
        update_yuumi_properties(pyautogui.screenshot())
        if w_availability:
            if blue >= 2 and attached != available_champ() and champsStatus[int(available_champ()[1])-2] and healthfracs[int(attached[1])-2] >= 0.9:
                previous = attached
                attach_to_champ(attached,0.3)
                attach_to_champ(available_champ(),2)
                if status == 0:
                    attach_to_champ(previous,-1)
        update_yuumi_properties(pyautogui.screenshot())
        if(e_availability==1):
            get_ap()
            heal = e_healing()
            missinghp = admaxhp[level-1]*(1-healthfracs[int(attached[1])-2])
            if heal <= missinghp:
                use_e()
            elif(healthfracs[int(attached[1])-2] <= 0.6):
                use_e()
        elif e_availability==2:
            before = last_e_ping
            after = time.perf_counter()
            if (after - before) > 10:
                pyautogui.moveTo(900,985)
                keyboard.press('k')
                time.sleep(0.1)
                keyboard.release('k')
                pyautogui.moveTo(500,500)
                last_e_ping = time.perf_counter()

        if red >= 1.75:
            if(r_availability==1):
                use_r(side)
            elif(r_availability==2):
                before = last_r_ping
                after = time.perf_counter()
                if (after - before) > 10:
                    pyautogui.moveTo(951,975)
                    keyboard.press('k')
                    time.sleep(0.1)
                    keyboard.release('k')
                    pyautogui.moveTo(500,500)
                    last_r_ping = time.perf_counter()
            

    elif status == 2:
        buying = 1
        buy_items(pyautogui.screenshot())

def update_hps(image):
    global healthfracs
    healthfracs = [1,1,1,1]



    #top laner
    offset = 1724
    if image.getpixel((offset,822))[1]<50:
        healthfracs[0] = 0.6
    elif image.getpixel((offset + 4,822))[1]<50:
        healthfracs[0] = 0.7
    elif image.getpixel((offset + 8,822))[1]<50:
        healthfracs[0] = 0.8
    elif image.getpixel((offset + 12,822))[1]<50:
        healthfracs[0] = 0.9

    #jg
    offset += 56
    if image.getpixel((offset,822))[1]<50:
        healthfracs[1] = 0.6
    elif image.getpixel((offset + 4,822))[1]<50:
        healthfracs[1] = 0.7
    elif image.getpixel((offset +8,822))[1]<50:
        healthfracs[1] = 0.8
    elif image.getpixel((offset + 12,822))[1]<50:
        healthfracs[1] = 0.9

    #mid
    offset += 56
    if image.getpixel((offset,822))[1]<50:
        healthfracs[2] = 0.6
    elif image.getpixel((offset + 4,822))[1]<50:
        healthfracs[2] = 0.7
    elif image.getpixel((offset +8,822))[1]<50:
        healthfracs[2] = 0.8
    elif image.getpixel((offset + 12,822))[1]<50:
        healthfracs[2] = 0.9

    #ad
    offset += 56
    if image.getpixel((offset,822))[1]<50:
        healthfracs[3] = 0.6
    elif image.getpixel((offset + 4,822))[1]<50:
        healthfracs[3] = 0.7
    elif image.getpixel((offset +8,822))[1]<50:
        healthfracs[3] = 0.8
    elif image.getpixel((offset + 12,822))[1]<50:
        healthfracs[3] = 0.9


def use_e():
    keyboard.press_and_release('e')
    pass

def use_r(side):
    global rAllChats
    global rTeamChats
    if side==0:
        pyautogui.moveTo(1900,100)
    else:
        pyautogui.moveTo(300,1060)
    keyboard.press_and_release('r')
    r_index = random.randint(0,4)
    AllorTeam = random.randint(0,1)
    if AllorTeam == 1:
        if rAllChats == [1,1,1,1,1]:
            rAllChats = [0,0,0,0,0]
        while rAllChats[r_index] == 1:
            r_index = random.randint(0,4)
        '''
        keyboard.press_and_release('shift+enter')
        time.sleep(0.1)
        keyboard.write(r_text_all_chat[r_index])
        time.sleep(0.1)
        keyboard.press_and_release('enter')
        time.sleep(0.1)
        rAllChats[r_index] = 1
        '''
    else:
        if rTeamChats == [1,1,1,1,1]:
            rTeamChats = [0,0,0,0,0]
        while rTeamChats[r_index] == 1:
            r_index = random.randint(0,4)
        '''
        keyboard.press_and_release('enter')
        time.sleep(0.1)
        keyboard.write(r_text_team_chat[r_index])
        time.sleep(0.1)
        keyboard.press_and_release('enter')
        time.sleep(0.1)
        rTeamChats[r_index] = 1
        '''

def ward(x,y):
    #not ward = (1854,1013)
    #ward = (1867,1012)
    #mouse on screen = (965,547)
    #mouse on ward = (1337,531)
    #scale 27.5
    #distance = 13
    x_diff = 0
    y_diff = 0
    for ward_spot in ward_spots:
        try:
            if math.sqrt((ward_spot[0]-x)^2+(ward_spot[1]-y)^2) < 13:
                print("Warding")
                pyautogui.moveTo(960,540)
                x_diff = (ward_spot[0]-x)*30
                y_diff = (ward_spot[1]-y)*30
                pyautogui.moveTo(960+x_diff,540+y_diff)
                keyboard.press_and_release('4')
                break
        except:
            print("No ward spots here")

def blue_pct(center_x, center_y, image):
    starting_x = center_x - 33
    starting_y = center_y - 19
    max_x = min(starting_x + 67,1919)
    max_y = min(starting_y + 39,1079)
    blues = 0
    pixels = 0
    while starting_x <= max_x:
        while starting_y <= max_y:
            pixel = image.getpixel((starting_x, starting_y))
            if pixel[0] > 75 and pixel[0] < 95 and pixel[1] > 135 and pixel[1] < 165 and pixel[2] > 185 and pixel[2] < 235: 
                blues += 1
            pixels += 1
            starting_y += 1
        starting_y = max_y - 39
        starting_x += 1
    blue = blues/pixels*100
    return blue

def red_pct(center_x, center_y, image):
    starting_x = center_x - 33
    starting_y = center_y - 19
    max_x = min(starting_x + 67,1919)
    max_y = min(starting_y + 39,1079)
    reds = 0
    pixels = 0
    while starting_x <= max_x:
        while starting_y <= max_y:
            pixel = image.getpixel((starting_x, starting_y))
            if pixel[0] > 210 and pixel[0] < 235 and pixel[1] > 55 and pixel[1] < 65 and pixel[2] > 45 and pixel[2] < 55:
                reds += 1 
            pixels += 1
            starting_y += 1
        starting_y = max_y - 39
        starting_x += 1
    red = reds/pixels*100
    return red


#Yuumi Loop

#game start
time.sleep(3)
screen = pyautogui.screenshot()
side = findWhite(screen)[1]<=958
print("The side is: "+str(side))


while(1==1):
    before = time.perf_counter()

    update_yuumi_properties(pyautogui.screenshot())
    actions(pyautogui.screenshot())
    iterations += 1

    time.sleep(0.1)
    now = time.perf_counter()

    elapsed += now-before
