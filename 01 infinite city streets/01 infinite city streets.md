# 01: Infinite city streets

## Status

🟩 Active

## Contents

🟩 [Base](#base)

🟩 [Bonus 1: Arbitrary start and end within city](#bonus-1)

🟩 [Bonus 2: City with wrapping streets](#bonus-2)

🟩 [Bonus 3: N-dimensional city](#bonus-3)

🟩 [Bonus 4: Wandering routes](#bonus-4)

🟩 [Bonus 5: Time to destination](#bonus-5)

## Base

[(top)](#contents)

Imagine a city with infinitely long horizontal and vertical streets. There are $n$ horizontal streets and $m$ vertical streets. The vertical and horizontal streets cross each other forming a 2D grid of $m \cdot n$ intersections. Some of these intersections are blocked off and cannot be driven through.

Write a function that determines how many different paths there are from the top left intersection to the bottom right intersection. Assume you must follow the streets and you are only able to move right and down. Your inputs are $n$, $m$, and a list of intersections that are blocked off.

### Test cases

#### Case 1

Input

```
OO
OO

(2, 2, [])
```

Expected

```
2
```

#### Case 2

Input

```
OX
OO

(2, 2, [(1, 2)])
```

Expected

```
1
```

#### Case 3

Input

```
OX
XO

(2, 2, [(1, 2), (2, 1)])
```

Expected

```
0
```

#### Case 4

Input

```
OXO
OOX
OOO

(3, 3, [(1, 2), (2, 3)])
```

Expected

```
2
```

### Function signature

Python

```python
from typing import List, Tuple

def num_routes(n: int, m: int, blocked: List[Tuple[int, int]]) -> int:
    return 0
```

Kotlin

```kotlin
fun numRoutes(n: Int, m: Int, blocked: List<Pair<Int, Int>>): Int {
    return 0
}
```

Java

```java
import java.util.List;

public static int numRoutes(int n, int m, List<int[]> blocked) {
    return 0;
}
```

### Expected

We are looking for the following general things in relation to this question. These are not hard requirements, but rather are points that the interviewer can use to guide the candidate throughout the solving process.

-   The candidate should be able to represent the problem in an appropriate problem space (i.e. a graph problem or DP).
-   The candidate should apply an appropriate algorithm to the problem space (i.e. DFS).
    -   The candidate may want to discuss why they chose a specific algorithm for this problem.

-   The candidate should try to identify edge cases and early termination cases.
    -   The candidate should hopefully ask how the blocked points are indexed. For the purposes of this question, we assume that blocked points are 1 indexed. That is, the top left intersection has coordinates $(1, 1)$ instead of $(0, 0)$ and the bottom right intersection has coordinates $(m, n)$ instead of $(m - 1, n - 1)$.

#### General techniques

1.   Graph based search problem

     -   The problem can be represented as a graph where the root node can have up to two children. This graph may or may not be a tree depending on the candidate's choice. The tree version clearly indicates the re-computation of subproblems, while the connected graph version may indicates the reuse of computation of subproblems.

     -   In the following example, the representation as a tree or graph shows

         ```
         OXO
         OOX
         OOO
         ```

         The options at each intersection are the following, where `D` is down, `R` is right, `X` is blocked, and `G` is goal.

         ```
         D  X  D
         DR D  X
         R  R  G
         ```

         This can translate into a tree graph that looks like the following, where the number of leaves represents the number of possible routes.

         ```
           D
         D   R
         R   D
         R   R
         G   G
         ```

         This can also translate into a connected graph that looks like the following, where some kind of tracking will need to be done to determine the number of possible routes.

         ```
           D
         D   R
         R   D
           R
           G
         ```

         In the tree version, we can see that lines 4 and 5 are repeated computations, where in the connected graph version we can see it is shared.

2.   Inline recursive (DFS) approach

     -   This problem can also be solved as a DFS terminating at the goal (bottom right intersection). This solution is somewhat reminiscent of a backtracking algorithm. This should be implemented without any large additional data structures, in place.

     -   The base cases required are as follows.

         -   Out of bounds of the array should `return 0`.
         -   Blocked intersection should `return 0`.
         -   Goal state should `return 1`.

     -   The general case is derivable from a simple example.

         ```
         CA
         BO
         OG
         ```

         By inspection, it is clear that there exists only one route from `A` to the goal `G`. It is also clear that there exists only two routes from `B` to the goal `G`. By inspection it is possible to determine that there are three routes from `C` to `G`. These three routes are made by combining the routes from `A` with the routes from `B`.

         As such, our general case is given by the sum of the number of routes of the intersection below and the intersection to the right.

3.   Recursive memoization (top down) approach

     -   This is very similar to the recursive approach. The only change is we avoid re-computing sub problems by storing the result of computations in a table and referencing that table as we do the recursion.

4.   Iterative dynamic programming (bottom up) approach

     -   The dynamic programming bottom up approach is the alternative to the top down approach. It replaces the recursion with iteration over the table. There are a few important aspects of this solution, which include identifying the recurrence, identifying the direction of iteration, and identifying essentially the same base cases from the recursive approach.
     -   Depending on how the candidate chooses their base case, either the top left $(0, 0)$ cell of the array will be initialized to `1` or the bottom right $(m - 1, n - 1)$ will be initialized similarly. Iteration should start from the base case cell and move away from it gradually column by column or row by row.
     -   Depending on how the candidate choses their base case, the recurrence may either rely on the cells above and to the left or on the cells below and to the right.
     -   The result should be returned from the opposite corner of the base case cell.

#### Code examples

Recursive (DFS) approach forward

```python
def num_routes_recursive_forward(n: int, m: int, blocked: List[Tuple[int, int]]) -> int:
    def num_routes_helper(y: int, x: int, n: int, m: int, blocked: List[Tuple[int, int]]) -> int:
        # Out of bounds base case
        if y >= n or x >= m:
            return 0

        # Blocked base case
        if (y, x) in blocked:
            return 0

        # Goal base case
        if y == n - 1 and x == m - 1:
            return 1

        # General case, cell is computed from result of cell to the right and cell below
        return num_routes_helper(y + 1, x, n, m, blocked) + num_routes_helper(y, x + 1, n, m, blocked)

    # Transform blocked such that it is 0 indexed
    return num_routes_helper(0, 0, n, m, [(y - 1, x - 1) for y, x in blocked])
```

Recursive (DFS) approach backward

```python
def num_routes_recursive_backward(n: int, m: int, blocked: List[Tuple[int, int]]) -> int:
    def num_routes_helper(y: int, x: int, blocked: List[Tuple[int, int]]) -> int:
        # Out of bounds base case
        if y < 0 or x < 0:
            return 0

        # Blocked base case
        if (y, x) in blocked:
            return 0

        # Goal base case
        if y == 0 and x == 0:
            return 1

        # General case, cell is computed from result of cell to the right and cell below
        return num_routes_helper(y - 1, x, blocked) + num_routes_helper(y, x - 1, blocked)

    # Transform blocked such that it is 0 indexed
    return num_routes_helper(n - 1, m - 1, [(y - 1, x - 1) for y, x in blocked])
```

Recursive (DFS) approach with memoization (top down) forward

```python
def num_routes(n: int, m: int, blocked: List[Tuple[int, int]]) -> int:
    # Create table for saving results to avoid re-computation
    num_routes_table = [[-1 for _ in range(m)] for _ in range(n)]

    def num_routes_helper(y: int, x: int, n: int, m: int, blocked: List[Tuple[int, int]]) -> int:
        # Out of bounds base case
        if y >= n or x >= m:
            return 0

        # Blocked base case
        if (y, x) in blocked:
            return 0

        # Goal base case
        if y == n - 1 and x == m - 1:
            return 1

        # Check if we have already computed this sub-problem, if we have, just reuse that computation
        if num_routes_table[y][x] != -1:
            return num_routes_table[y][x]

        # General case, cell is computed from result of cell to the right and cell below
        routes = num_routes_helper(y + 1, x, n, m, blocked) + num_routes_helper(y, x + 1, n, m, blocked)
        # Save the result of this computation to the table
        num_routes_table[y][x] = routes
        return routes

    # Transform blocked such that it is 0 indexed
    return num_routes_helper(0, 0, n, m, [(y - 1, x - 1) for y, x in blocked])
```

Recursive (DFS) approach with memoization (top down) backward

```python
def num_routes_recursive_td_backward(n: int, m: int, blocked: List[Tuple[int, int]]) -> int:
    # Create table for saving results to avoid re-computation
    num_routes_table = [[-1 for _ in range(m)] for _ in range(n)]

    def num_routes_helper(y: int, x: int, blocked: List[Tuple[int, int]]) -> int:
        # Out of bounds base case
        if y < 0 or x < 0:
            return 0

        # Blocked base case
        if (y, x) in blocked:
            return 0

        # Goal base case
        if y == 0 and x == 0:
            return 1

        # Check if we have already computed this sub-problem, if we have, just reuse that computation
        if num_routes_table[y][x] != -1:
            return num_routes_table[y][x]

        # General case, cell is computed from result of cell to the right and cell below
        routes = num_routes_helper(y - 1, x, blocked) + num_routes_helper(y, x - 1, blocked)
        # Save the result of this computation to the table
        num_routes_table[y][x] = routes
        return routes

    # Transform blocked such that it is 0 indexed
    return num_routes_helper(n - 1, m - 1, [(y - 1, x - 1) for y, x in blocked])
```

Dynamic programming bottom up approach forward

```python
def num_routes(n: int, m: int, blocked: List[Tuple[int, int]]) -> int:
    # Construct DP array, here we assign (0, 0) in the array to be the goal (m, n)
    dp = [[0 for _ in range(m)] for _ in range(n)]
    # Initialize number of paths from goal
    dp[0][0] = 1

    # Early termination if start or end is blocked
    if (n, m) in blocked or (1, 1) in blocked:
        return 0

    # Iteration direction is important here to ensure we match the recurrence
    for y in range(n):
        for x in range(m):
            # If the current cell is blocked, leave DP value as 0
            if (y + 1, x + 1) in blocked:
                continue

            # Out of bounds check for y (above)
            if y - 1 < n:
                # Add number of routes from cell above
                dp[y][x] += dp[y - 1][x]

            # Out of bounds check for x (left)
            if x - 1 < m:
                # Add number of routes from cell to the left
                dp[y][x] += dp[y][x - 1]

    return dp[n - 1][m - 1]
```

Dynamic programming bottom up approach backward

```python
def num_routes(n: int, m: int, blocked: List[Tuple[int, int]]) -> int:
    # Construct DP array, here we assign (m - 1, n - 1) in the array to be the goal (m, n)
    dp = [[0 for _ in range(m)] for _ in range(n)]
    # Initialize number of paths from goal
    dp[n - 1][m - 1] = 1

    # Early termination if start or end is blocked
    if (n, m) in blocked or (1, 1) in blocked:
        return 0

    # Iteration direction is important here to ensure we match the recurrence
    for y in reversed(range(n)):
        for x in reversed(range(m)):
            # If the current cell is blocked, leave DP value as 0
            if (y + 1, x + 1) in blocked:
                continue

            # Out of bounds check for y (below)
            if y + 1 < n:
                # Add number of routes from cell below
                dp[y][x] += dp[y + 1][x]

            # Out of bounds check for x (right)
            if x + 1 < m:
                # Add number of routes from cell to the right
                dp[y][x] += dp[y][x + 1]

    return dp[0][0]
```

### Raw

```
Imagine a city with infinitely long horizontal and vertical streets. There are n horizontal streets and m vertical streets. The vertical and horizontal streets cross each other forming a 2D grid of (m * n) intersections. Some of these intersections are blocked off and cannot be driven through.

Write a function that determines how many different paths there are from the top left intersection to the bottom right intersection. Assume you must follow the streets and you are only able to move right and down. Your inputs are n, m, and a list of intersections that are blocked off.
```



---



## Bonus 1

##### Arbitrary start and end within city

[(top)](#contents)

Assume now that we want to find the number of routes between any two arbitrary intersections, $(x_1, y_1)$ To $(x_2, y_2)$, within the city. You cannot modify the code you have already written and should write a new function that utilizes your previous function to compute the result to this modified problem.

### Test cases

#### Case 1

Input

```

```

Expected

```

```

### Function signature

Python

```python
from typing import List, Tuple

def num_routes_any(x1: int, y1: int, x2: int, y2: int, blocked: List[Tuple[int, int]]) -> int:
    return 0
```

Kotlin

```kotlin
fun numRoutesAny(x1: Int, y1: Int, x2: Int, y2: Int, blocked: List<Pair<Int, Int>>): Int {
    return 0
}
```

Java

```java
import java.util.List;

public static int numRoutesAny(int x1, int y1, int x2, int y2, List<int[]> blocked) {
    return 0;
}
```

### Expected

Provide general reasoning behind use of question here. Also provide any other general question expectations here.

#### General techniques

1.   

#### Code examples

```

```

### Raw

```

```



---



## Bonus 2

##### City with wrapping streets

[(top)](#contents)

Imagine now that the streets of this city are not infinite, but instead wrap around and connect back on themselves. In this new city, continuing to the right from the rightmost intersection will lead you to the leftmost intersection on that same road. How would you modify your solution to account for this type of city?

### Test cases

#### Case 1

Input

```
OOXX
XOOX
OXOO
OXXX
OOOO

()
```

Expected

```

```

### Function signature

Python

```python
from typing import List, Tuple

def num_routes_wrap(n: int, m: int, blocked: List[Tuple[int, int]]) -> int:
    return 0
```

Kotlin

```kotlin
fun numRoutesWrap(n: Int, m: Int, blocked: List<Pair<Int, Int>>): Int {
    return 0
}
```

Java

```java
import java.util.List;

public static int numRoutesWrap(int n, int m, List<int[]> blocked) {
    return 0;
}
```

### Expected

Provide general reasoning behind use of question here. Also provide any other general question expectations here.

#### General techniques

1.   

#### Code examples

```

```

### Raw

```

```



---



## Bonus 3

##### N-dimensional city

[(top)](#contents)

Imagine now that the city is built with aliens technology. In this alien city, the streets exist in any number of dimensions. We want to try and determine the number of routes in this N-dimensional city.

Assume you are given a list of length $d$ of dimension sizes and a list of intersection coordinates that are blocked off. Also assume that you can only move in the positive coordinate direction and that you want to travel from $(0, 0, \cdots)$ to the largest possible coordinate intersection.

### Test cases

#### Case 1

Input

```

```

Expected

```

```

### Function signature

Python

```python
from typing import List, Tuple

def num_routes_wrap(dimension_sizes: List[int], blocked: List[Tuple[int, ...]]) -> int:
    return 0
```

Kotlin

```kotlin
fun numRoutesWrap(dimensionSizes: List<Int>, blocked: List<Array<Int>>): Int {
    return 0
}
```

Java

```java
import java.util.List;

public static int numRoutesWrap(List<Integer> dimensionSizes, List<int[]> blocked) {
    return 0;
}
```

### Expected

Provide general reasoning behind use of question here. Also provide any other general question expectations here.

#### General techniques

1.   

#### Code examples

```

```

### Raw

```

```



---



## Bonus 4

##### Wandering routes

[(top)](#contents)

Assume now that we wish to move from any arbitrary start point to any other target point. In this situation we are able to move in any direction, but cannot visit the same intersection twice. Assume you are given the two points $(x_1, y_1)$ and $(x_2, y_2)$ and a list of blocked intersections. We want to find the number of possible routes from our start to the target.

### Test cases

#### Case 1

Input

```

```

Expected

```

```

### Function signature

Python

```python
from typing import List, Tuple

def num_routes_any(x1: int, y1: int, x2: int, y2: int, blocked: List[Tuple[int, int]]) -> int:
    return 0
```

Kotlin

```kotlin
fun numRoutesAny(x1: Int, y1: Int, x2: Int, y2: Int, blocked: List<Pair<Int, Int>>): Int {
    return 0
}
```

Java

```java
import java.util.List;

public static int numRoutesAny(int x1, int y1, int x2, int y2, List<int[]> blocked) {
    return 0;
}
```

### Expected

Provide general reasoning behind use of question here. Also provide any other general question expectations here.

#### General techniques

1.   

#### Code examples

```

```

### Raw

```

```



---



## Bonus 5

##### Time to destination

[(top)](#contents)

Imagine now that we live at the origin in our N-dimensional grid city. We have some target that we wish to travel to. Some intersections are still blocked off and we can only move in the positive coordinate direction. We want to know the minimum number of time it would take to arrive at the target.

Assume you are given a list of length $d$ of dimension sizes and a list of intersection coordinates that are blocked off.

### Test cases

#### Case 1

Input

```

```

Expected

```

```

### Function signature

Python

```python
from typing import List, Tuple

def num_routes_wrap(dimension_sizes: List[int], blocked: List[Tuple[int, ...]]) -> int:
    return 0
```

Kotlin

```kotlin
fun numRoutesWrap(dimensionSizes: List<Int>, blocked: List<Array<Int>>): Int {
    return 0
}
```

Java

```java
import java.util.List;

public static int numRoutesWrap(List<Integer> dimensionSizes, List<int[]> blocked) {
    return 0;
}
```

### Expected

Provide general reasoning behind use of question here. Also provide any other general question expectations here.

#### General techniques

1.   

#### Code examples

```

```

### Raw

```

```