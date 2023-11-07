## Mars Rover

### 1.1

#### Info given to us

- Speed on sandy terrain = S(S) = 3 km/h
- Speed on smooth terrain = S(SM) = 5 km/h
- Speed on rocky terrain = S(R) = 2 km/h

#### Route 1 Info

- Distance = 2 km
- Probability of sandy terrain = 0.2
- Probability of smooth terrain = 0.3
- Probability of rocky terrain = 0.5

#### Route 2 Info

- Distance = 1.8 km
- Probability of sandy terrain = 0.4
- Probability of smooth terrain = 0.2
- Probability of rocky terrain = 0.4

#### Route 3 Info

- Distance = 3.1 km
- Probability of sandy terrain = 0.5
- Probability of smooth terrain = 0.4
- Probability of rocky terrain = 0.1

#### Now we need to find the expected time for each route

- Expected time for route 1 = 0.2 _ 2/3 + 0.3 _ 2/5 + 0.5 \* 2/2 = 0.133 + 0.12 + 0.5 = 0.753 hours
- Expected time for route 2 = 0.4 _ 1.8/3 + 0.2 _ 1.8/5 + 0.4 \* 1.8/2 = 0.24 + 0.072 + 0.36 = 0.672 hours
- Expected time for route 3 = 0.5 _ 3.1/3 + 0.4 _ 3.1/5 + 0.1 \* 3.1/2 = 0.516 + 0.248 + 0.155 = 0.919 hours

According to the expected time, the best route is route 2. Since it has the lowest expected time.

### 1.2

#### Additional info given to us

- Route 1 has a probability of 0.3 of having a crater wall damaged adding 45 minutes to the expected time
  = 0.3 \* 3/4 = 0.225 hours
- Route 2 has a probability of 0.6 of having the bridge damaged adding 1 hour to the expected time
  = 0.6 \* 1 = 0.6 hours

#### The new expected time for each route

- Expected time for route 1 = 0.753 + 0.225 = 0.978 hours
- Expected time for route 2 = 0.672 + 0.6 = 1.272 hours
- Expected time for route 3 = 0.919 hours

According to the new expected time, the best route is route 3. Since it has the lowest expected time.

### 1.3

#### Now suppose that we can use a satellite to find out whether the terrain in route 3 is smooth. Is this helpful? What is the value of this information? Expressed differently, how long are we willing to wait for this information from the satellite?

If route 3 has a smooth terrain, then the expected time for route 3 will be 3.1/5 = 0.62 hours. This is less than the expected time for route 1 and route 2. So, if we can use a satellite to find out whether the terrain in route 3 is smooth, then it is helpful. The value of this information is 0.919 - 0.62 = 0.299 hours. We are willing to wait for this information from the satellite for 0.299 hours.

### 1.4

#### Now put this problem into ChatGPT. Is it able to solve it correctly? If not, where does it make mistakes?

ChatGPT is not able to solve this problem correctly. It makes mistakes in the following places:

- It doesn't factor in the different lengths of the routes. It only considers the probabilities of the terrains. So, it thinks that the best route is route 2.
- It isn't able to give a correct answer about how long we are willing to wait for the information from the satellite. It says that we are willing to wait for 0 hours. But the correct answer is 0.299 hours.
