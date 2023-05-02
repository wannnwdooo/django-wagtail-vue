FROM node:16.18.1

WORKDIR /app

COPY ./vue/package*.json ./
RUN yarn install

COPY ./vue/vite.config.ts ./vite.config.ts

COPY ./vue/ ./
#RUN rm -rf ./src
#RUN rm -rf ./src
#
#COPY ./vue/src/ ./vue
#RUN mv src vue


#WORKDIR /app/vue
#
#COPY ./src/* .