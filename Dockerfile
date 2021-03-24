FROM gleissonbezerra/jetson-nano-l4t-cuda-cudnn-opencv-4.2.0:1.0.2-arm64v8
WORKDIR /app
COPY requirements.txt .

ENV HTTPS_PROXY="http://172.16.98.151:8118"
ENV HTTP_PROXY="http://172.16.98.151:8118"

RUN pip3 install -r requirements.txt
COPY . .

CMD ["uvicorn", "server:app", "--host", "0.0.0.0"]