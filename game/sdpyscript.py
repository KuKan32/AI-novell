import ctypes
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)

import os, webuiapi
from PIL import Image

prompt = ""
prompts={}
dio_count=0
with open(r'C:\Users\KanKan\Desktop\Generative_Novell_project\game\dialog.txt',encoding='UTF-8') as text:
    for row in text:
        if 'ch*' in row or 'bg*' in row:
            prompts[dio_count]=row
        else:
            dio_count+=1
prepend = "/".join(os.path.abspath(__file__).split("\\")[:-1])
bg_model = "animerge_v210.safetensors" 
char_model = "animerge_v210.safetensors" 

pos_bg_prompt = ", <lora:cartoon[back]:0.5>, masterpiece, best resolution, detailed shading, vibrant colors, (background), ((no people))"
neg_bg_prompt = ", people, multiple people, ugly, lowres, text, error, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name"

char_pos_prompt = ", ((solo)), highres, best quality, best resolution, detailed skin"
char_neg_prompt = ", cropped, ugly, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name, nsfw"

address = "192.168.0.115" 
port = 7860
api = webuiapi.WebUIApi(host=address, port=port)
options = {}
options["sd_model_checkpoint"] = bg_model 
api.set_options(options)

def generate_img (prompt, ch_or_bg, num, keyword=""):
	if ch_or_bg=='bg':
		wid=1280
		hei=720
		prompt+=pos_bg_prompt
		unit1 = webuiapi.ControlNetUnit(input_image=None, module='none', model='control_openpose-fp16 [9ca67cc5]')
		neg_prompt=neg_bg_prompt
		options["sd_model_checkpoint"] = bg_model
	else:
		wid=720
		hei=720
		if 'pose' in prompt:
			pos_num=prompt[prompt.index('pose')+4:]
			pose=Image.open(prepend + f"/poses/pose{pos_num}.png")
			unit1 = webuiapi.ControlNetUnit(input_image=pose, module='openpose', model='control_openpose-fp16 [9ca67cc5]')
		else:
			unit1 = webuiapi.ControlNetUnit(input_image=None, module='none', model='control_openpose-fp16 [9ca67cc5]')
		prompt+=char_pos_prompt
		options["sd_model_checkpoint"] = char_model
		neg_prompt=char_neg_prompt
	api.set_options(options)
	r1 = api.txt2img(prompt=f'{keyword}, {prompt}',
					negative_prompt=neg_prompt,
					sampler_index="DPM++ 2M Karras",
					width=wid, 
					height=hei, 
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
			generate_img(p[3::],'bg',num)
		elif 'ch*' in p:
			generate_img(p[3::],'ch',num)