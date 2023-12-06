init python:
    import os, subprocess, json, re, requests
    from datetime import datetime
    import shutil
    prompt = ""
    good=True
    runmode = "/k"
    str_count=0
    dialog={}
    prompts={}
    dio_count=0
    last_ch_num=None
    with open(r'C:\Users\KanKan\Desktop\ren_test\game\dialog.txt',encoding='UTF-8') as text:
        for row in text:
            if 'ch*' in row or 'bg*' in row:
                prompts[dio_count]=('bg*' in row, 'ch*' in row)
            else:
                dialog[dio_count]=row
                dio_count+=1


define char = Character("Рин Рин")

define player = Character('Я')

label start:
    
    $ subprocess.Popen(["start", "cmd", runmode, "python " + config.basedir + "/game/sdpyscript.py"], shell=True)
    

    python:
        for num, row in dialog.items():
            need_change=prompts.get(num)
            if need_change:
                if need_change[0]:
                    while not os.path.isfile(f'C:\\Users\\KanKan\\Desktop\\ren_test\\game\\done{num}bg.txt'):
                        renpy.say(player,f'{num}'+'bgPlease wait{w=0.5}{nw}')
                    os.remove(f'C:\\Users\\KanKan\\Desktop\\ren_test\\game\\done{num}bg.txt')
                    renpy.scene()
                    renpy.show(f"bg {num}")
                    if last_ch_num:
                        renpy.show(f"ch {last_ch_num}")
                if need_change[1]:
                    while not os.path.isfile(f'C:\\Users\\KanKan\\Desktop\\ren_test\\game\\done{num}ch.txt'):
                        renpy.say(player,f'{num}'+'chPlease wait{w=0.5}{nw}')
                    os.remove(f'C:\\Users\\KanKan\\Desktop\\ren_test\\game\\done{num}ch.txt')
                    renpy.show(f"ch {num}")
                    last_ch_num=num
            renpy.say(char,row)
            