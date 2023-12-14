docker stop test-system
docker rm test-system
docker build -t test-system .
# docker run -d --name test-system -p 8080:8080 test-system 

# docker run --name test-system --gpus all -d -p 8000:8000 test-system 

# 需要挂载的文件夹
# db.sqlite3
# static

docker run --name test-system --gpus all -d -p 8000:8000 -v ./db.sqlite3:/app/db.sqlite3 -v ./static:/app/static test-system