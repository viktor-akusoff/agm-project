FROM node:latest as build-stage

WORKDIR /app

COPY . ./
RUN npm install
RUN npm run build

# Production stage
FROM nginx:alpine

COPY ./nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=build-stage /app/dist /usr/share/nginx/html

EXPOSE 8080