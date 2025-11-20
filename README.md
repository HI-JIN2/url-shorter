# url-shorter
url을 입력하면 단축 url을 반환하는 api



도커 = 개별 서비스 단위 컨테이너
도커 컴포즈 = 전체 시스템 단위로 여러 컨테이너를 묶어서 한 번에 실행

도커 컴포즈를 사용하면 한줄로 여러개를 한번에 실행할 수 있음
```
docker compose up --build
```

## 도커 컴포즈 

- FastAPI 앱: 8000 포트
- Prometheus: 9090 포트
- Grafana: 3000 포트
- 모두 monitor-net 네트워크로 연결됨

## 실행 방법

1. venv 활성화 (Mac / Linux)  
    ```
    source venv/bin/activate
    ```


2. 패키지 설치   
    ```
    pip install -r requirements.txt
    ```

3. FAST API 실행   
    ```
    ./venv/bin/uvicorn app:app --reload

    ```

그외 잘 쓰는 명령어
- 8080 포트를 사용하는 프로세스 죽이기 
    ```
    lsof -i :8000
    ```
    
    ```
    kill -9 <번호>
    ```

- 도커 굽기
    ```
    docker build -t url-shortener:latest .
    docker run -p 8000:8000 url-shortener:latest
    
    ```
  

## 라이브러리 
| 라이브러리                 | 역할                                 |
| --------------------- | ---------------------------------- |
| **fastapi**           | 메인 API 서버                          |
| **uvicorn[standard]** | FastAPI 실행용 ASGI 서버                |
| **sqlalchemy**        | SQLite ORM                         |
| **pydantic**          | 요청/응답 데이터 검증                       |
| **prometheus_client** | `/metrics` 엔드포인트 생성                |
| **python-multipart**  | POST 요청 multipart 처리 (혹시 필요할 수 있음) |



