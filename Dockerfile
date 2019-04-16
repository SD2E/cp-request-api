from sd2e/python3 as basebuilder
RUN mkdir -p /app
WORKDIR /app
COPY . .
RUN python3 setup.py develop

