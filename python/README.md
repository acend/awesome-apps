# example-web-python

to get the progress page up and running you have assign the view role to the service account in the namespace:
```
kubectl -n lab create rolebinding progress --clusterrole=view --serviceaccount=lab:default
```
