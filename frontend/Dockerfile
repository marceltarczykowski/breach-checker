FROM nginx:alpine
LABEL maintainer="imie.nazwisko@example.com"v
LABEL autor="Marcel Tarczykowski" data="2026-10-15"
RUN apk add --no-cache nodejs npm && npm install -g htmlhint
COPY index.html style.css script.js /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf
RUN date > /usr/share/nginx/html/build.txt
RUN htmlhint /usr/share/nginx/html/index.html
EXPOSE 80
