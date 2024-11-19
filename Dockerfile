# # Use the official Conda image as a base
# FROM continuumio/miniconda3

# # Install necessary packages
# RUN apt-get update && apt-get install -y \
#     bash \
#     git \
#     && rm -rf /var/lib/apt/lists/*

# # Create the vscode user
# RUN useradd -ms /bin/bash vscode

# # Switch to the vscode user
# USER vscode

# # Copy the environment.yml file into the container
# COPY environment.yml /tmp/environment.yml

# # Create the Conda environment
# RUN conda env create -f /tmp/environment.yml

# # Set the default shell to bash
# SHELL ["/bin/bash", "-c"]

# # Initialize Conda
# RUN conda init bash

# # Source .bashrc and activate the Conda environment
# RUN echo "source ~/.bashrc && conda activate quantum" >> ~/.bashrc

# # Set the environment path to include the Conda environment
# ENV PATH /opt/conda/envs/quantum/bin:$PATH

# # Set the working directory
# WORKDIR /workspace

# # Start with the conda environment active when you enter the container
# ENTRYPOINT [ "/bin/bash", "-c", "source ~/.bashrc && conda activate quantum && exec bash" ]


FROM python:3.11-slim

WORKDIR /workspace

RUN pip install --no-cache-dir \
    jupyter \
    numpy \
    pandas \
    matplotlib \
    qiskit \
    qiskit-aer \
    pylatexenc

EXPOSE 8888
