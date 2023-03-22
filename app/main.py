import os
import json
import datetime
import torch
import gc
import time
import threading
from pathlib import Path
from PIL import Image
from diffusers import StableDiffusionPipeline
from flask import Flask, request, render_template
from operator import itemgetter

# 1.0
root = os.path.dirname(os.path.abspath(__file__))
Path(os.path.join(root, "outputs")).mkdir(parents=True, exist_ok=True)
Path(os.path.join(root, "outputs_horizontal")).mkdir(parents=True, exist_ok=True)
Path(os.path.join(root, "outputs_vertical")).mkdir(parents=True, exist_ok=True)
# 1.1
app = Flask(__name__, static_url_path='', static_folder=root, template_folder=os.path.join(root, "templates"))
lock = threading.Lock()
# 1.2
size_base = 64
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = f'max_split_size_mb:{size_base}'
torch_device = "cuda" if torch.cuda.is_available() else "cpu"


def image_grid(imgs, rows, cols):
    assert len(imgs) == rows * cols
    w, h = imgs[0].size
    grid = Image.new('RGB', size=(cols * w, rows * h))
    for i, img in enumerate(imgs):
        grid.paste(img, box=(i % cols * w, i // cols * h))
    return grid


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/run-model", methods=["POST"])
def run_model():
    prompts = request.form.getlist('prompt[]')
    prompts_negative = request.form.getlist('promptNegative[]')
    model_id = request.form.get('model_id')
    no_img = int(request.form.get('no_img'))
    step = int(request.form.get('step'))
    size = request.form.get('size').split(",")
    img_width, img_height = int(size[0])*size_base , int(size[1])*size_base

    class MyThread(threading.Thread):
        def __init__(self, num):
            threading.Thread.__init__(self)
            self.num = num

        def clean_cache(self):
            if torch.cuda.is_available():
                gc.collect()
                torch.cuda.empty_cache()
                torch.cuda.ipc_collect()
                print(f"Thread{self.num}: torch.cuda.empty_cache")

        def run(self):
            lock.acquire()

            images = []
            cur_time = datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            path_folder = os.path.join(root, "outputs", cur_time)
            Path(path_folder).mkdir(parents=True, exist_ok=True)

            prompt_negative = ""
            if prompts_negative[self.num]:
                prompt_negative = prompts_negative[self.num]
            prompt = prompts[self.num]
            print(cur_time, f"Thread{self.num}")

            with open(os.path.join(path_folder, f"{cur_time}_prompt.txt"), 'w+') as f:
                f.write(f"{model_id} || {prompt} ||　{prompt_negative}")

            self.clean_cache()

            if 'anything-v3.0' in model_id:
                pipe = StableDiffusionPipeline.from_pretrained(model_id, local_files_only=False, cache_dir=root, torch_dtype=torch.float16, revision="diffusers").to(torch_device)
            else:
                pipe = StableDiffusionPipeline.from_pretrained(model_id, local_files_only=False, cache_dir=root, torch_dtype=torch.float32).to(torch_device)

            for j in range(no_img):
                image = pipe(prompt, negative_prompt=prompt_negative, num_inference_steps=step, height=img_height, width=img_width).images[0]
                image.save(os.path.join(path_folder, f"{cur_time}_{j}.png"))
                images.append(image)

            if no_img == 20:
                rows = 4
            elif no_img == 15:
                rows = 3
            elif no_img == 10:
                rows = 2
            elif no_img == 5:
                rows = 1

            grid1 = image_grid(images, rows=rows, cols=5)
            grid2 = image_grid(images, rows=5, cols=rows)
            grid1.save(os.path.join(path_folder, f"{cur_time}_showcase_horizontal.png"))
            grid2.save(os.path.join(path_folder, f"{cur_time}_showcase_vertical.png"))

            grid1.save(os.path.join(root, "outputs_horizontal", f"{cur_time}_showcase_horizontal.png"))
            grid2.save(os.path.join(root, "outputs_vertical", f"{cur_time}_showcase_vertical.png"))

            self.clean_cache()
            time.sleep(30)
            lock.release()

    threads = []
    for i in range(len(prompts)):
        if prompts[i]:
            threads.append(MyThread(i))
            threads[i].start()

    data1 = {'status': 'success'}
    return app.response_class(response=json.dumps(data1), status=200, mimetype='application/json')


@app.route('/get-images', methods=['GET', 'POST'])
def get_images():
    data1 = []
    for x1 in os.walk(os.path.join(root, "outputs")):
        if x1[2]:
            data2 = {'label': '', 'showcase_horizontal': '', 'showcase_vertical': '', 'result': [], 'prompt': ''}
            if x1[0]:
                data2['label'] = x1[0].split('/')[3]
            for x2 in sorted(x1[2]):
                if 'prompt' in x2:
                    with open(os.path.join(x1[0], x2)) as f:
                        data2['prompt'] = f.read()
                elif 'showcase_horizontal' in x2:
                    data2['showcase_horizontal'] = x2
                elif 'showcase_vertical' in x2:
                    data2['showcase_vertical'] = x2
                else:
                    data2['result'].append(x2)
            data1.append(data2)
    data2 = sorted(data1, key=itemgetter('label'), reverse=True)
    return app.response_class(response=json.dumps(data2), status=200, mimetype='application/json')


@app.route('/get-gpu', methods=['GET', 'POST'])
def get_gpu():
    data1 = {
        'allocated': round(torch.cuda.memory_allocated(0) / 1024 ** 3, 2),
        'cached': round(torch.cuda.memory_cached(0) / 1024 ** 3, 2),
        'reserved': round(torch.cuda.memory_reserved(0) / 1024 ** 3, 2),
        'max_memory_reserved': round(torch.cuda.max_memory_reserved(0) / 1024 ** 3, 2),
    }
    return app.response_class(response=json.dumps(data1), status=200, mimetype='application/json')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=82)
