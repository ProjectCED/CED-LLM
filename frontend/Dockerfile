# Dockerfile for frontend
FROM node:18-alpine
WORKDIR /frontend
COPY . .
RUN npm install
RUN npm run build
CMD ["npm", "run", "dev"]
