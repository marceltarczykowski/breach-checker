FROM nginx:alpine
RUN apk add --no-cache curl
CMD sh -c 'if curl -s -f http://backend:8080/health > /dev/null; then echo "backend: OK"; else echo "backend: UNREACHABLE"; fi'
