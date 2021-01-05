# example-web-python

To get the progress page up and running you have to assign the view role to the service account in the namespace:
```
kubectl create rolebinding progress --clusterrole=view --serviceaccount=<namespace>:default --namespace=<namespace>
```
