# ===========================
# Stage 1: Build React App
# ===========================
FROM node:20-alpine AS builder

WORKDIR /app

# Copy dependency files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application source
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

# Remove default nginx site configuration
RUN rm -f /etc/nginx/conf.d/default.conf

# Copy React build
COPY --from=builder /app/build /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

# Expose HTTP port
EXPOSE 80

# Start Nginx
ENTRYPOINT ["nginx", "-g", "daemon off;"]