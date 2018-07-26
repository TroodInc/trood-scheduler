FROM python:3

ENV APPDIR=/home/scheduler
ENV PYTHONPATH=$PYTHONPATH:$APPDIR

RUN mkdir -p $APPDIR

RUN apt-get update && \
    apt-get install gcc g++ python3-dev musl-dev -y && \
    mkdir -p $APPDIR

WORKDIR $APPDIR

COPY ./scheduler $APPDIR/scheduler
COPY ./tasks $APPDIR/tasks
COPY ./manage.py $APPDIR/manage.py
COPY ./circus.ini $APPDIR/circus.ini
COPY ./requirements.txt $APPDIR/requirements.txt

RUN pip install --upgrade -r $APPDIR/requirements.txt

EXPOSE 8000

CMD /usr/local/bin/circusd /home/scheduler/circus.ini
