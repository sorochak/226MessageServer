FROM python

RUN mkdir /server

COPY server.py /server

CMD [ "python", "/server/server.py" ]
