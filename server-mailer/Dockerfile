FROM ubuntu as base

RUN apt update
RUN apt install -y ca-certificates

FROM golang as app

ENV GOPROXY="https://goproxy.io,direct"

WORKDIR /app

COPY go.mod go.sum ./

RUN go mod download

COPY . .

RUN go build -o app .

FROM base

COPY --from=app /app/app .

CMD [ "/app" ]
