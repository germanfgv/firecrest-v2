 docker build -t f7tdemo -f ./build/demo-sidecar/Dockerfile .

 docker run  -p 8080:8080 f7tdemo        