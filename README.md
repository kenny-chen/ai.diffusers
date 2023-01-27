# ai.diffusers

只支援CUDA10.1颢示卡。

1. 下载项目
```
mkdir PycharmProject
cd PycharmProjects
git clone https://github.com/kenny-chen/ai.diffusers
mv ai.diffusers diffusers
```

2. 建立镜像
```
sudo docker build -t ~/PycharmProjects/diffusers/cuda/v3:10.2-cudnn8-runtime-ubuntu18.04 .
```

3. 执行镜像
```
cd ~/diffusers
mkdir log
sudo docker run --name diffusers.002 --rm --gpus all -t -v ~/PycharmProjects/diffusers/app:/app -p 82:82 diffusers/cuda/v3:10.2-cudnn8-runtime-ubuntu18.04 python3 /app/main.py >> ~/PycharmProjects/diffusers/log/diffusers_001_`date +\%Y\%m\%d_\%H\%M\%S`.log 2>&1
```

4. 进入主页
![screenshot](https://raw.githubusercontent.com/kenny-chen/ai.diffusers/main/screenshot/screenshot_20230126_a.png "screenshot")
进入127.0.0.1:82


### 参数设置
|选项|描述|
| :------------ | :------------ |
|Model ID|runwayml/stable-diffusion-v1-5<br />Linaqruf/anything-v3.0<br />hakurei/waifu-diffusion|
|Size (px / ratio / total px)|尺寸 / 长宽比 / 总像素|
|No. Image|每次生成多少张照片|
|Step|模型步数|
|Prompt|txt2img|
|Negative Prompt|txt2img|

### 安装教程
[安装详细教程(博客园)](https://www.cnblogs.com/chenkuang/p/17048888.html "安装详细教程")