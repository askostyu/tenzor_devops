# Создание volume

sudo docker volume create --name dd_result

# Запуск контейнера и запуск в нем dd

sudo docker run -it --rm --device-write-iops /dev/sda:1000 -v dd_result:/result ubuntu
dd if=/dev/urandom of=/file.tmp bs=1024 count=1000000 oflag=direct status=progress 2>/result/result.txt

# Запуск контейнера, который выводит результат работы dd соседнего контейнера в shell

sudo docker run -it --rm -v dd_result:/result ubuntu
while true; do tail -n 1 /result/result.txt; sleep 5; done

# Запуск экспортера метрик

sudo docker build -t prometheus-devops .
sudo docker run -it --rm -p 80:8000 --name c2 -v dd_result:/result prometheus-devops

# Проверка установленного ограничения

sudo docker ps --no-trunc

sudo cgget /docker/fc0d95d401b685304f98075df9ff81a63c0657202baacee1afea6d079c3ba437 | grep blkio.throttle.write_iops_device

sudo cgset -r blkio.throttle.write_iops_device="8:0 10000" /docker/fc0d95d401b685304f98075df9ff81a63c0657202baacee1afea6d079c3ba437
