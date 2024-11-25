# Dockerfile for Backend using Conda
#FROM continuumio/miniconda3
FROM continuumio/miniconda3

WORKDIR /app

# Copy environment setup file
COPY environment_dockerfile.yml .

# Create conda environment and install dependencies
RUN conda env create -f environment_dockerfile.yml

# Activate the environment and set it as the default
RUN echo "conda activate ced-backend" >> ~/.bashrc
ENV PATH /opt/conda/envs/ced-backend/bin:$PATH

# for health check in docker-compose
#RUN apt-get update && apt-get install -y curl
RUN apt-get update && apt-get install -y netcat-openbsd

# Copy the rest of the code
COPY . /app

# Expose the application port
EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
