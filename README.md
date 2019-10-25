# challenge

Simple web app that connects to www.alphavantage.co to retrieve closing prices for a specified stock and averages them over a number of specified days.

You will need an API key for the service from [here](https://www.alphavantage.co/support/#api-key)

The deployment manifest points to a Docker image on docker.io.

# Building the container and pushing to GCR:
1. Clone this repo
2. Set up Docker with Google creds:
```
glcoud auth configure-docker
```
3. In the `./src` directory, build and tag an image:
```
docker build -t eu.gcr.io/your-project-id/challenge:[version]
```
4. Push the image:
```
docker push eu.gcr.io/your-project-id/challenge:[version]
```
5. Update `./k8s/challenge-deployment.yaml` with the your new image location

# running in Kubernetes

1. Clone out this repo
2. Update `./k8s/challenge-config.yaml` with values for `ndays` and `symbol`
3. Create the Kubernetes secret:
```
kubectl create secret generic challenge-secret --from-literal apikey=YOUR_KEY
```
4. Deploy to your Kubernetes cluster:
```
kubectl apply -f k8s
```
5. Wait for the ingress controller to assign an IP:
```
watch "kubectl get ingress"
```
6. Once that's assigned, simply:
```
curl <ingress_ip>
```

Minikube requires the Nginx Ingress Controller to be enabled:
```
minikube addons enable ingress
```
