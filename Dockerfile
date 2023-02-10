FROM continuumio/miniconda
WORKDIR /usr/src/app

COPY main.py .
COPY env.yml .
COPY utilities utilities
COPY indata indata
COPY output output
COPY entrypoint.sh .

RUN conda env create -f env.yml
# Make RUN commands use the new environment:
RUN echo "conda activate maze" >> ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]

ENTRYPOINT ["./entrypoint.sh"]
