FROM python:3 as base

LABEL com.centurylinklabs.watchtower.enable="false"

WORKDIR /app
RUN dpkg-reconfigure -f noninteractive git
RUN git clone https://github.com/OfirValla/Speedtest.git
WORKDIR /app/Speedtest
RUN git pull

COPY . .

FROM python:3 as final

COPY --from=base /app/Speedtest /app

WORKDIR /app
RUN pip install -r requirements.txt

CMD [ "python", "-u", "main.py" ]
