FROM nvidia/cuda:10.2-cudnn8-runtime-ubuntu18.04
LABEL maintainer="Hugging Face"
LABEL repository="diffusers"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && \
    apt install -y bash \
                   build-essential \
                   git \
                   git-lfs \
                   curl \
                   ca-certificates \
                   libsndfile1-dev \
                   python3.8 \
                   python3-pip \
                   python3.8-venv \
                   python3-venv && \
    rm -rf /var/lib/apt/lists
    
# link libcudart.so.10.2 to libcudart.so.10.1
RUN ln -s /usr/local/cuda-10.2/targets/x86_64-linux/lib/libcudart.so.10.2 /usr/lib/x86_64-linux-gnu/libcudart.so.10.1

# link python3 to python3.8
RUN rm /usr/bin/python3 && \
    ln -s /usr/bin/python3.8 /usr/bin/python3

# make sure to use venv
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# pre-install the heavy dependencies (these can later be overridden by the deps from setup.py)
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir \
        torch==1.10.1+cu102 \
        torchvision==0.11.2+cu102 \
        torchaudio==0.10.1 \
        -f https://download.pytorch.org/whl/cu102/torch_stable.html && \
    python3 -m pip install --no-cache-dir \
        accelerate \
        datasets \
        hf-doc-builder \
        huggingface-hub \
        diffusers \
        librosa \
        modelcards \
        numpy \
        scipy \
        tensorflow-gpu==2.3.0 \
        tensorboard \
        transformers \
        jupyterlab \
        flask

CMD ["/bin/bash"]