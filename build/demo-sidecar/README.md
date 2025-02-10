 docker build -t f7tdemo -f ./build/demo-sidecar/Dockerfile .
 

docker run --name demo --restart=always  -p 8080:8080 f7tdemo        


http://localhost:8080/boot