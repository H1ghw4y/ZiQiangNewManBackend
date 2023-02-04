docker rm -f recommend_container
docker rmi recommend
docker build -t recommend .
docker run -it --network=traefik --label "traefik.enable=true" --label "traefik.http.routers.recommend.rule=Host(\`api.recommend.temp.ziqiang.net.cn\`)"  --label "traefik.http.routers.recommend.entrypoints=websecure" --label "traefik.http.services.recommend.loadbalancer.server.port=8085" --name recommend_container recommend
