FROM python:3.9

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY install_pytorch3d.sh .

RUN chmod +x install_pytorch3d.sh

RUN ./install_pytorch3d.sh

COPY shapeaxi /app/shapeaxi

ENV PYTHONPATH="${PYTHONPATH}:/app"

EXPOSE 8080

CMD ["python", "shapeaxi/saxi_folds.py"]