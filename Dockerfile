FROM python:3

RUN dpkg-reconfigure -f noninteractive tzdata
ENV TZ=Asia/Jerusalem
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY . .

RUN pip install -r requirements.txt

CMD [ "python", "./main.py" ]
