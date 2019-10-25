# challenge

Simple web app that connects to www.alphavantage.co to retrieve closing prices for a specified stock and averages them over a number of specified days.

You will need an API key for the service from [here](https://www.alphavantage.co/support/#api-key)

# running in Kubernetes

1. Check out this repo
2. Update `./k8s/challenge-config.yaml` with values for `ndays` and `symbol`
3. Create the Kubernetes secret:
```
kubectl create secret generic challenge-secret --from-literal apikey=YOUR_KEY
```
4. Deploy to your Kubernetes cluster:
```
kubectl apply -f k8s
```

Minikube requires the Nginx Ingress Controller to be enabled:
```
minikube addons enable ingress
```
