# Dockerfile for Backend using Conda
FROM continuumio/miniconda3

WORKDIR /app

# Copy environment setup file
COPY environment.yml /app

# Create conda environment and install dependencies
RUN conda env create -f environment.yml

# Activate the environment and set it as the default
RUN echo "conda activate mybackendenv" >> ~/.bashrc
ENV PATH /opt/conda/envs/mybackendenv/bin:$PATH

# Copy the rest of the code
COPY . /app

# Expose the application port
EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
