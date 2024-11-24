# Dockerfile for frontend
FROM node:18-alpine
WORKDIR /frontend
COPY . .
RUN npm install
RUN npm run build
EXPOSE 3000
EXPOSE 5173
CMD ["npm", "run", "dev"]
