# ai.diffusers

Only support CUDA10.1

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
![screenshot](https://raw.githubusercontent.com/kenny-chen/ai.diffusers/main/screenshot/screenshot_20230126_a.png "screenshot")
Go 127.0.0.1:82


### Setting params
|Params|Description|
| :------------ | :------------ |
|Model ID|runwayml/stable-diffusion-v1-5<br />Linaqruf/anything-v3.0<br />hakurei/waifu-diffusion|
|Size (px / ratio / total px)|size / width height ratio / total pixel|
|No. Image|how many images will be generated of each time|
|Step|model step|
|Prompt|txt2img|
|Negative Prompt|txt2img|

### Install guideline
[Detailed install guideline(cnblogs)](https://www.cnblogs.com/chenkuang/p/17048888.html "Detailed install guideline")