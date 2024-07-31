FROM golang:alpine as app

ENV GOPROXY="https://goproxy.io,direct"

WORKDIR /app

COPY go.mod go.sum ./

RUN go mod download

COPY . .

RUN go build -o app .

FROM alpine

COPY --from=app /app/app .

CMD [ "/app" ]
