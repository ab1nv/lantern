FROM golang:1.24.3-alpine3.21

WORKDIR /app

RUN go install github.com/air-verse/air@latest

COPY . .

RUN go mod download

EXPOSE 7331

CMD ["air", "-c", ".air.toml"]