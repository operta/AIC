FROM node:lts-alpine as base

ENV NODE_ENV production
WORKDIR /usr/src/app
RUN npm config set -g production false
COPY ["package.json", "package-lock.json*", "npm-shrinkwrap.json*", "./"]
RUN npm install
COPY . .

FROM node:lts-alpine

COPY --from=base /usr/src/app /usr/src/app
WORKDIR /usr/src/app
EXPOSE 8080

CMD ["npm", "run", "serve"]
