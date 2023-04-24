# ai.diffusers

support CUDA10.1 & CUDA11.7

1. Download project
```
mkdir PycharmProject
cd PycharmProjects
git clone https://github.com/kenny-chen/ai.diffusers
mv ai.diffusers diffusers
```

2. Build docker image
```
sudo docker build -t ~/PycharmProjects/diffusers/cuda/v3:10.2-cudnn8-runtime-ubuntu18.04 .
```

3. Run docker container
```
cd ~/diffusers
mkdir log
sudo docker run --name diffusers.002 --rm --gpus all -t -v ~/PycharmProjects/diffusers/app:/app -p 82:82 diffusers/cuda/v3:10.2-cudnn8-runtime-ubuntu18.04 python3 /app/main.py >> ~/PycharmProjects/diffusers/log/diffusers_001_`date +\%Y\%m\%d_\%H\%M\%S`.log 2>&1
```

4. Go to index
![screenshot](https://raw.githubusercontent.com/kenny-chen/ai.diffusers/main/screenshot/screenshot_20230424_a "screenshot")
Go 127.0.0.1:82


### Setting params
|Params|Description|
| :------------ | :------------ |
|Model ID|runwayml/stable-diffusion-v1-5<br />gsdf/Counterfeit-V2.5<br />andite/anything-v4.0<br />Lykon/DreamShaper<br />wavymulder/portraitplus<br />dreamlike-art/dreamlike-photoreal-2.0<br />Linaqruf/anything-v3.0<br />hakurei/waifu-diffusion<br />ogkalu/Comic-Diffusion<br />Envvi/Inkpunk-Diffusion<br />|
|Size (px / ratio / total px)|size / width height ratio / total pixel|
|No. Image|how many images will be generated of each time|
|Step|model step|
|Mode|**normal**: no specific prompt<br /> **shot & frame**: <br /> a. shots: extreme wide shot, wide shot, medium shot, close up shot, close up shot, extreme close-up shot <br /> b. angles: high angle shot, POV shot, shoulder level shot, knee level shot, low angle shot, dutch angle shot|
|Prompt|txt2img|
|Negative Prompt|txt2img|

### Install guideline
[Detailed install guideline (cnblogs)](https://www.cnblogs.com/chenkuang/p/17048888.html "Detailed install guideline")
[Detailed Upgrade CUDA (cnblogs)](https://www.cnblogs.com/chenkuang/p/17333447.html "Detailed upgrade guideline")