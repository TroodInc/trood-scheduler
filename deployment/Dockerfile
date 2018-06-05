FROM python:3-alpine

ENV APPDIR=/home/scheduler
ENV PYTHONPATH=$PYTHONPATH:$APPDIR

RUN mkdir -p $APPDIR

RUN apk update && \
    apk add postgresql-dev gcc g++ linux-headers python3-dev musl-dev && \
    mkdir -p $APPDIR

WORKDIR $APPDIR

COPY ./scheduler $APPDIR/scheduler
COPY ./tasks $APPDIR/tasks
COPY ./manage.py $APPDIR/manage.py
COPY ./circus.ini $APPDIR/circus.ini
COPY ./requirements.txt $APPDIR/requirements.txt

RUN pip install -r $APPDIR/requirements.txt
RUN rm $APPDIR/requirements.txt

EXPOSE 8000

CMD /usr/local/bin/circusd /home/scheduler/circus.ini
