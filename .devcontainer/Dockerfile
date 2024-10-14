# Use the official Conda image as a base
FROM continuumio/miniconda3

# Install necessary packages
RUN apt-get update && apt-get install -y \
    bash \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy the environment.yml file into the container
COPY environment.yml /tmp/environment.yml

# Create the Conda environment
RUN conda env create -f /tmp/environment.yml

# Set the default shell to bash
SHELL ["/bin/bash", "-c"]

# Activate the Conda environment
RUN echo "source activate quantum" > ~/.bashrc
ENV PATH /opt/conda/envs/quantum/bin:$PATH

# Set the working directory
WORKDIR /workspace
