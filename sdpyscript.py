import ctypes
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)

import json, os, requests, random, webuiapi
from time import sleep
from datetime import datetime
from PIL import Image

prompt = ""
prompts={}
dio_count=0
with open(r'C:\Users\KanKan\Desktop\ren_test\game\dialog.txt',encoding='UTF-8') as text:
    for row in text:
        if 'ch*' in row or 'bg*' in row:
            prompts[dio_count]=row
        else:
            dio_count+=1
prepend = "/".join(os.path.abspath(__file__).split("\\")[:-1])
bg_model = "animerge_v210.safetensors" 
char_model = "animerge_v210.safetensors" 

pos_bg_prompt = ", masterpiece, best resolution, detailed shading, vibrant colors, (background), ((no people))"
neg_bg_prompt = ", people, multiple people, ugly, lowres, text, error, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name"

char_pos_prompt = ", ((solo)), highres, best quality, best resolution, detailed skin"
char_neg_prompt = ", cropped, ugly, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name, cum on face"

address = "192.168.0.115" 
port = 7860
api = webuiapi.WebUIApi(host=address, port=port)
options = {}
options["sd_model_checkpoint"] = bg_model 
api.set_options(options)

def generate_img (prompt, ch_or_bg, num, keyword=""):
	if ch_or_bg=='bg':
		prompt+=pos_bg_prompt
		unit1 = webuiapi.ControlNetUnit(input_image=None, module='none', model='control_openpose-fp16 [9ca67cc5]')
		neg_prompt=neg_bg_prompt
		options["sd_model_checkpoint"] = bg_model
	else:
		pose=Image.open(prepend + "/poses/" + random.choice(os.listdir(prepend + "/poses")))
		unit1 = webuiapi.ControlNetUnit(input_image=pose, module='openpose', model='control_openpose-fp16 [9ca67cc5]')
		prompt+=char_pos_prompt
		options["sd_model_checkpoint"] = char_model
		neg_prompt=char_neg_prompt
	api.set_options(options)
	r1 = api.txt2img(prompt=f'{keyword}, {prompt}',
					negative_prompt=neg_prompt,
					sampler_index="Euler",
					width=1280, 
					height=768, 
                    steps=20,
					cfg_scale=7.5,
					controlnet_units=[unit1],
					)
	if ch_or_bg=='ch':
		rembg=webuiapi.RemBGInterface(api)
		r1=rembg.rembg(input_image=r1.image, model="isnet-anime", return_mask=False)
		r1.image.save(prepend + f'/images/{ch_or_bg} {num}.png')
	else:
		r1.image.save(prepend + f'/images/{ch_or_bg} {num}.jpg')
	with open(prepend + f"/done{num}{ch_or_bg}.txt", "w") as f: pass
		

for num,prompt in prompts.items():
	for p in prompt.split():
		if 'bg*' in p:
			generate_img(p[3::].replace('_',','),'bg',num, '<lora:cartoon[back]:0.5>')
		else:
			generate_img(p[3::].replace('_',','),'ch',num,'<lora:leto:0.2>')