Нет возможности запускать minikube лоально, поэтому запускаю его на виртуалке.
Вместо "скриншот браузера с результатом запроса на localhost:port/metrics" вложил скриншот браузера на рабочей машине и результат curl c виртуалки

Запуск node-exporter-depl и node-exporter-service для доступа к node-exporter с рабочей машины. В том числе добавляется доступ и с хостовой машины
```
kubectl apply -f node-exporter-depl.yml
```

Если не использовать service, то можно пробросить порт следующим образом
```
kubectl port-forward deployment/node-exporter-depl 9200:9100
```
