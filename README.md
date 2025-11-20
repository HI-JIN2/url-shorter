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



