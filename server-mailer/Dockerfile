FROM golang:latest

ENV GOPROXY="https://goproxy.io,direct"

WORKDIR /app

COPY . .

RUN go mod download

RUN go build -o app .

FROM busybox

WORKDIR /app

COPY --from=0 ./app ./app

CMD [ "./app" ]
