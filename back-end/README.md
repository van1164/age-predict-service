``` bash
python.exe -m uvicorn main:app --reload
```

## nginx에서 8080 포트 내부 fastapi로 연결시키기

```nginx
server {
    listen 443 ssl;
    server_name your_domain.com;

    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private/key.key;

    location / {
        root /path/to/your/static/files;
        index index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8080/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }


server {
    listen 80;
    server_name your_domain.com;

    location / {
        root /path/to/your/static/files;
        index index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8080/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Redirect HTTP to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 8080;
    server_name localhost;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}


```

## 오류 처리

### [nginx] 413 Request Entity Too Large 오류
nginx.conf 파일에서 http, server, location에 설정이 가능하다.
```
http {
    client_max_body_size 5M;
    ...
}
```