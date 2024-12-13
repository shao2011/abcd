Cách debug khi dựng pods không thành công:
- Cách 1: kubectl logs <tên_pod>
- Cách 2: minikube dashboard

------------------------------------------------------------------------------------------------------------------------------------------------------
Cách dựng cluster cho HDFS (bằng minikube - windows)
    - Vào app Docker Desktop và bật Docker lên.
    - vào cmd (hoặc powershell) và chạy các lệnh: 
        - cd Traffic-accident-analysis\src\hdfs
        - minikube start 
        - kubectl get all (để kiểm tra)
        - kubectl create namespace hdfs
        - kubectl apply -f .\datanode-deployment.yaml
        - kubectl apply -f .\hdfs-client.yaml
        - kubectl apply -f .\namenode-deployment.yaml
        - kubectl apply -f .\resourcemanager.yaml  
        - kubectl get pods -n hdfs   (để kiểm tra trong namespace hdfs >>> phải Status đều running thì mới là được)
	- kubectl get all -n hdfs   (để kiểm tra trong namespace hdfs >>> phải Status đều running thì mới là được)
    
-> tắt đi: 
        - minikube delete --all
        - Vào app Docker Desktop và tắt đi, tắt Docker ở thanh taskbar đi.
        - wsl --list --running (để kiểm tra xem có những môi trường máy ảo nào đang chạy)
        - wsl --shutdown
        - wsl --list --running (kiểm tra lại xem tắt hết chưa)

------------------------------------------------------------------------------------------------------------------------------------------------------
Qui trình chạy cho Spark (bằng minikube -windows)
- Vào app Docker Desktop và bật Docker lên.
- vào cmd (hoặc powershell) và chạy các lệnh: 
        - cd "C:\Users\ADMIN\OneDrive\Desktop\Traffic-accident-analysis"

        # Dựng cluster lên
        - minikube start
	- helm install my-release oci://registry-1.docker.io/bitnamicharts/spark --set serviceType=NodePort
        (lần đầu chạy thì nên làm cái này:
		- để ý cái Note hiện ra thì chạy lệnh trong Note để lấy Spark master WebUI URL: kubectl port-forward --namespace default svc/my-release-spark-master-svc 80:80
		- Mở Chrome và truy cập: http://127.0.0.1/
		- copy cái Spark master WebUI URL và lưu tạm ra đâu đó. Cái URL này sẽ là tham số để truyền vào --master ở lệnh spark-submit ở dưới)
		- xong rồi thì Ctrl + C
	Note: nếu chạy lệnh port-forward bị lỗi thì là do các pods chưa dựng xong, chạy lệnh dưới để check status)
	
        - kubectl get pods (để kiểm tra 3 cái: master, 2 worker xem đã Ready chưa | nếu status đang ContainerCreating thì là dựng chưa xong, phải đợi)
	...đợi cho đến khi Ready
       
        # Copy file transform.py từ máy local lên máy Master
        - kubectl cp transform.py my-release-spark-master-0:/tmp/transform_master.py (note: file transform.py phải ở "C:\Users\ADMIN\OneDrive\Desktop\Traffic-accident-analysis")
      
        # Chạy file transform.py trên spark
        - kubectl exec -it my-release-spark-master-0 -- /bin/bash (Để truy cập vào Master và làm việc trên Master; Master là hệ điều hành Debian)
        - cd .. liên tục (cho đến khi thoát khỏi dir /opt)
        - ls (sẽ thấy dir tmp, đây mới là folder tmp lưu file transform_master.py)
        - cd tmp
        - /opt/bitnami/spark/bin/spark-submit --master spark://my-release-spark-master-0.my-release-spark-headless.default.svc.cluster.local:7077 transform_master.py
        ... đợi nó chạy
	- exit
	
-> tắt đi:
	- helm delete my-release
	(nếu không nhớ tên release thì dùng lệnh: helm list)
        - minikube delete --all
        - Vào app Docker Desktop và tắt đi, tắt Docker ở thanh taskbar đi.
        - wsl --list --running (để kiểm tra xem có những môi trường máy ảo nào đang chạy)
        - wsl --shutdown
        - wsl --list --running (kiểm tra lại xem tắt hết chưa)

------------------------------------------------------------------------------------------------------------------------------------------------------
Helm cho các bộ phận:
	- kafka: https://bitnami.com/stack/kafka/helm
	- cassandra: https://bitnami.com/stack/cassandra/helm

helm install my-release oci://registry-1.docker.io/bitnamicharts/kafka --set serviceType=NodePort
helm install my-release oci://registry-1.docker.io/bitnamicharts/cassandra --set serviceType=NodePort

kubectl cp --namespace default client-producer.properties my-release-kafka-client:/tmp/client.properties



