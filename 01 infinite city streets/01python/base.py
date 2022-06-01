from typing import List, Tuple

from cases import base
from util import run_tests


def num_routes_recursive_forward(n: int, m: int, blocked: List[Tuple[int, int]]) -> int:
    def num_routes_recursive_forward_helper(y: int, x: int, n: int, m: int, blocked: List[Tuple[int, int]]) -> int:
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
        return num_routes_recursive_forward_helper(y + 1, x, n, m, blocked) + num_routes_recursive_forward_helper(y, x + 1, n, m, blocked)

    # Transform blocked such that it is 0 indexed
    return num_routes_recursive_forward_helper(0, 0, n, m, [(y - 1, x - 1) for y, x in blocked])


def num_routes_recursive_backward(n: int, m: int, blocked: List[Tuple[int, int]]) -> int:
    def num_routes_recursive_backward_helper(y: int, x: int, blocked: List[Tuple[int, int]]) -> int:
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
        return num_routes_recursive_backward_helper(y - 1, x, blocked) + num_routes_recursive_backward_helper(y, x - 1, blocked)

    # Transform blocked such that it is 0 indexed
    return num_routes_recursive_backward_helper(n - 1, m - 1, [(y - 1, x - 1) for y, x in blocked])


def num_routes_recursive_td_forward(n: int, m: int, blocked: List[Tuple[int, int]]) -> int:
    # Create table for saving results to avoid re-computation
    num_routes_recursive_td_forward_table = [[-1 for _ in range(m)] for _ in range(n)]

    def num_routes_recursive_td_forward_helper(y: int, x: int, n: int, m: int, blocked: List[Tuple[int, int]]) -> int:
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
        if num_routes_recursive_td_forward_table[y][x] != -1:
            return num_routes_recursive_td_forward_table[y][x]

        # General case, cell is computed from result of cell to the right and cell below
        routes = num_routes_recursive_td_forward_helper(y + 1, x, n, m, blocked) + num_routes_recursive_td_forward_helper(y, x + 1, n, m, blocked)
        # Save the result of this computation to the table
        num_routes_recursive_td_forward_table[y][x] = routes
        return routes

    # Transform blocked such that it is 0 indexed
    return num_routes_recursive_td_forward_helper(0, 0, n, m, [(y - 1, x - 1) for y, x in blocked])


def num_routes_recursive_td_backward(n: int, m: int, blocked: List[Tuple[int, int]]) -> int:
    # Create table for saving results to avoid re-computation
    num_routes_recursive_td_forward_table = [[-1 for _ in range(m)] for _ in range(n)]

    def num_routes_recursive_backward_helper(y: int, x: int, blocked: List[Tuple[int, int]]) -> int:
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
        if num_routes_recursive_td_forward_table[y][x] != -1:
            return num_routes_recursive_td_forward_table[y][x]

        # General case, cell is computed from result of cell to the right and cell below
        routes = num_routes_recursive_backward_helper(y - 1, x, blocked) + num_routes_recursive_backward_helper(y, x - 1, blocked)
        # Save the result of this computation to the table
        num_routes_recursive_td_forward_table[y][x] = routes
        return routes

    # Transform blocked such that it is 0 indexed
    return num_routes_recursive_backward_helper(n - 1, m - 1, [(y - 1, x - 1) for y, x in blocked])


def num_routes_dp_bu_forward(n: int, m: int, blocked: List[Tuple[int, int]]) -> int:
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


def num_routes_dp_bu_backward(n: int, m: int, blocked: List[Tuple[int, int]]) -> int:
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


strategies = [
    ("recursive forward", num_routes_recursive_forward),
    ("recursive backward", num_routes_recursive_backward),
    ("recursive top down forward", num_routes_recursive_td_forward),
    ("recursive top down backward", num_routes_recursive_td_backward),
    ("dp bottom up forward ", num_routes_dp_bu_forward),
    ("dp bottom up backward", num_routes_dp_bu_backward)
]


if __name__ == '__main__':
    run_tests(strategies, base.CASE, base.CASE_EXPECTED)
