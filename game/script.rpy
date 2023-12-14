init python:
    import os, subprocess
    prompt = ""
    runmode = "/k"
    dialog={}
    prompts={}
    dio_count=0
    last_ch_num=None
    with open(r'C:\Users\KanKan\Desktop\Generative_Novell_project\game\dialog.txt',encoding='UTF-8') as text:
        for row in text:
            if 'ch*' in row or 'bg*' in row:
                prompts[dio_count]=('bg*' in row, 'ch*' in row, '*hide' in row)
            elif ']' in row:
                row=row.split(']')
                dialog[dio_count]=(row[0][1:], row[1])
                dio_count+=1

label start:
    camera at parallax
    $ subprocess.Popen(["start", "cmd", runmode, "python " + config.basedir + "/game/sdpyscript.py"], shell=True)
    python:
        renpy.show("white_bg")
        for num, row in dialog.items():
            need_change=prompts.get(num)
            if need_change:
                if need_change[0]:
                    while not os.path.isfile(f'C:\\Users\\KanKan\\Desktop\\Generative_Novell_project\\game\\done{num}bg.txt'):
                        renpy.say('',f'{num}'+'bg loading{w=0.5}{nw}')
                    os.remove(f'C:\\Users\\KanKan\\Desktop\\Generative_Novell_project\\game\\done{num}bg.txt')
                    renpy.scene()
                    renpy.show(f"bg {num}")
                    if last_ch_num:
                        renpy.show(f"ch {last_ch_num}")
                if need_change[1]:
                    while not os.path.isfile(f'C:\\Users\\KanKan\\Desktop\\Generative_Novell_project\\game\\done{num}ch.txt'):
                        renpy.say('',f'{num}'+'ch loading{w=0.5}{nw}')
                    os.remove(f'C:\\Users\\KanKan\\Desktop\\Generative_Novell_project\\game\\done{num}ch.txt')
                    renpy.show(f"ch {num}")
                    last_ch_num=num
                if need_change[2]:
                    renpy.hide(f"ch {last_ch_num}")
            renpy.say(row[0],row[1])
            