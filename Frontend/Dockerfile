# ===========================
# Stage 1: Build React App
# ===========================
FROM node:20-alpine AS builder

WORKDIR /app

# Copy dependency files first
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build React application
RUN npm run build

# ===========================
# Stage 2: Nginx Runtime
# ===========================
FROM nginx:1.27-alpine

LABEL authors="Opstree Solution" \
      contact="opensource@opstree.com" \
      version="v0.1.0" \
      service="frontend"

# Copy React build
COPY --from=builder /app/build /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

ENTRYPOINT ["nginx", "-g", "daemon off;"]