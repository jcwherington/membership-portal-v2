FROM node:18-slim
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json next.config.js tsconfig.json .env ./
RUN npm install

# Copy source code and generate static assets
COPY src src
COPY public public

CMD npm run build
