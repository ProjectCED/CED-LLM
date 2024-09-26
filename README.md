# CED-LLM
Classify and Enhance Data with LLM - Project for Tampere University course Software Engineering Project. Working with Solita.

# Project Setup

## Prerequisites
Make sure you have the following installed:
- [Conda](https://docs.conda.io/en/latest/miniconda.html) (Miniconda or Anaconda)
- [Docker](https://docs.docker.com/get-docker/) (if using Docker for containers)
- [Visual Studio Code](https://code.visualstudio.com/)

## 1. Clone the Repository
```bash
git clone https://github.com/ProjectCED/CED-LLM.git
cd CED-LLM

# Create and Activate Conda Environment

conda env create -f backend/environment.yml
conda activate ced-backend

# Install Node.js Packages for Frontend

cd frontend
npm install

```

## Running the Project
To run both the backend and frontend with Docker use:
```bash
docker-compose up
```

Alternatively, you can run the backend and frontend locally:
- Backend:
```bash
conda activate ced-backend
flask run
```

- Frontend:
```bash
cd frontend
npm run dev
```

## Running Tests (Backend)
Navigate to the backend/tests folder and run the tests with pytest:
```bash
cd backend/tests
pytest
```

## Updating the Environment
If any dependencies change, update the Conda environment with:
```bash
conda env update --file backend/environment.yml
```

### 2. **Push the Environment Configuration to Git**
To automate the setup of the Conda environment for your team, you can push the `environment.yml` file to the repository.

## Setting up the Environment variables

#### Create the `environment.yml` file:
From your current Conda environment, export the environment configuration:
```bash
conda env export > backend/environment.yml
```

#### setup .env file
rename the .env.example file to .env and fill in the required values using:
```bash
cp .env.example .env
```