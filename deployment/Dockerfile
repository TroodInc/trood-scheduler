FROM python:3.6

ENV APPDIR=/home/src
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
COPY ./pytest.ini $APPDIR/pytest.ini
COPY ./requirements.txt $APPDIR/requirements.txt
COPY ./entry-point.sh $APPDIR/

RUN pip install --upgrade -r $APPDIR/requirements.txt

EXPOSE 8000

CMD sh entry-point.sh
CMD /usr/local/bin/circusd /home/src/circus.ini

