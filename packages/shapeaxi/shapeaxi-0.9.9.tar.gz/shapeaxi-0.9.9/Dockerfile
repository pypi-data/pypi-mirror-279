FROM python:3.9

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install shapeaxi --upgrade

COPY install_pytorch3d.sh .

RUN chmod +x install_pytorch3d.sh

RUN ./install_pytorch3d.sh

EXPOSE 8080

CMD ["shapeaxi"]