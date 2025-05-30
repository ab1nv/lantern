# Stage 1: Build
FROM golang:1.24-alpine AS build

WORKDIR /app

# Install system dependencies
RUN apk add --no-cache git nodejs npm

# Install templ and air
RUN go install github.com/a-h/templ/cmd/templ@latest
RUN go install github.com/air-verse/air@latest

# Install TailwindCSS globally via npm
RUN npm install -g tailwindcss

# Copy source
COPY . .

# Download Go dependencies
RUN go mod tidy

# Generate templ files
RUN templ generate

# Stage 2: Runtime
FROM golang:1.24-alpine

WORKDIR /app

# Copy binaries from build stage
COPY --from=build /go/bin/* /usr/local/bin/
COPY --from=build /app /app

# Install runtime dependencies
RUN apk add --no-cache nodejs npm
RUN npm install -g tailwindcss

# Permission for entry script
RUN chmod +x ./client/entry.sh

EXPOSE 8090

CMD ["./client/entry.sh"]
