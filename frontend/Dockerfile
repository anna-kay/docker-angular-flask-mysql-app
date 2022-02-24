### Stage 1: Build ###

FROM node:12.7-alpine AS build
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
RUN npm run build --prod

### Stage 2: Run ###

FROM nginx:1.17.1-alpine AS prod-stage 

RUN apk add python3 python3-dev py3-pip build-base libressl-dev musl-dev libffi-dev rust cargo
RUN pip3 install pip --upgrade

COPY --from=build /app/dist/card-view-demo /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

COPY default.conf /etc/nginx/conf.d/default.conf
