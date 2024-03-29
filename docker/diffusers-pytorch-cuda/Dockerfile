FROM nvidia/cuda:11.7.0-cudnn8-runtime-ubuntu18.04
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
        torch==1.13.0+cu117 \
        torchvision==0.14.0+cu117 \
        torchaudio==0.13.0 \
        --extra-index-url https://download.pytorch.org/whl/cu117 && \
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
        tensorboard \
        transformers \
        flask \
        protobuf==3.20.3

CMD ["/bin/bash"]