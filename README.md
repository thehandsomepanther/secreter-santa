#secreter-santa

This is a python script to generate secret santa matchings such that it is less likely for someone to be assigned a person if he or she has already had that person in years previous. This works by creating a weighted bipartite graph of Santas and running the Munkres algorithm over them.

You can install the Munkres library by running

```
pip install munkres
```

In order to run this script, you'll also need to create your own `credentials.py` and `santa.json` files. There are examples of both in this repo. The credentials are your email and password, which will be used to send out assignments. This script assumes you're using Gmail, but it could easily be modified to any email server.

In the construction of the graph, people are given a maximum cost of 100 to themselves and the person they had the year previous, and then a cost for every other person based on how many times each person has been had previously. There's also a small amount of random cost assigned to every person that isn't already at the maximum cost, because secret santa should always have some level of randomness involved.
