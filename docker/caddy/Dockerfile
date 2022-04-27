FROM caddy:2-alpine
RUN apk update && apk add vim && apk add bash
COPY docker/caddy/Caddyfile /etc/caddy/Caddyfile
WORKDIR /app
COPY staticfiles/ /app/staticfiles
