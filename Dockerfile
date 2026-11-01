#Imagem leve para reduzir tamanho e tempo de build
FROM python:3.13-slim

#Pasta onde os próximos comandos do Dockerfile serão executados
WORKDIR /app 

#Copia o arquivo de dependências para dentro do container
# . significa que copiamos o arquivo para a pasta atual do container, que é /app
COPY requirements.txt .

