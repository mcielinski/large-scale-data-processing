FROM ubuntu

ARG TARGETPLATFORM

RUN echo "I'm building for $TARGETPLATFORM"

# RUN apt-get install update
# RUN echo "This text comes from inside of Dockerfile"

ENTRYPOINT [ "echo" ]

CMD [ "This text comes from inside of Dockerfile." ]
#CMD "echo" "This text comes from inside of Dockerfile"

ENV WORK_DIR ${HOME}/workdir

WORKDIR /workdir

ADD . /workdir