FROM continuumio/miniconda

# Set the working directory to /usr/src/app
WORKDIR /usr/src/app

# Copy the current directory necessary contents into the container at /usr/src/app
COPY main.py .
COPY env.yml .
COPY utilities utilities
COPY indata indata
COPY output output
COPY entrypoint.sh .

# Create the environment:
RUN conda env create -f env.yml

# Make RUN commands use the new environment:
RUN echo "conda activate maze" >> ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]

# Run the program:
ENTRYPOINT ["./entrypoint.sh"]
