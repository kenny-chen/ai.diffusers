# ai.diffusers

只支援CUDA10.1顥示卡。

1. 下載項目
```
mkdir PycharmProject
cd PycharmProjects
git clone https://github.com/kenny-chen/ai.diffusers
mv ai.diffusers diffusers
```

2. 建立鏡像
```
sudo docker build -t ~/PycharmProjects/diffusers/cuda/v3:10.2-cudnn8-runtime-ubuntu18.04 .
```

3. 執行鏡像
```
cd ~/diffusers
mkdir log
sudo docker run --name diffusers.002 --rm --gpus all -t -v ~/PycharmProjects/diffusers/app:/app -p 82:82 diffusers/cuda/v3:10.2-cudnn8-runtime-ubuntu18.04 python3 /app/main.py >> ~/PycharmProjects/diffusers/log/diffusers_001_`date +\%Y\%m\%d_\%H\%M\%S`.log 2>&1
```

4. 進入主頁
![screenshot](https://raw.githubusercontent.com/kenny-chen/ai.diffusers/main/screenshot/screenshot_20230126_a.png "screenshot")
進入127.0.0.1:82


### 參數設置
|選項|描述|
| :------------ | :------------ |
|Model ID|runwayml/stable-diffusion-v1-5<br />Linaqruf/anything-v3.0<br />hakurei/waifu-diffusion|
|Size (px / ratio / total px)|尺寸 / 長寬比 / 總像素|
|No. Image|每次生成多少張照片|
|Step|模型步數|
|Prompt|txt2img|
|Negative Prompt|txt2img|
