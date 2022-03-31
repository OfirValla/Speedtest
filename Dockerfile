FROM python:3 as base

# RUN dpkg-reconfigure -f noninteractive tzdata
# ENV TZ=Asia/Jerusalem
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app
#RUN dpkg-reconfigure -f noninteractive git
#RUN git clone https://github.com/OfirValla/Speedtest.git

COPY . .

FROM python:3 as final

#COPY --from=base /app/Speedtest /app
COPY --from=base /app /app

WORKDIR /app
RUN pip install -r requirements.txt

CMD [ "python", "-u", "main.py" ]
