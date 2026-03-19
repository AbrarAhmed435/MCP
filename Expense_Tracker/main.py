import random
from mcp.server.fastmcp import FastMCP

# MUST be global
mcp = FastMCP("demo-server")


@mcp.tool()
def roll_dice(n_dice: int = 1) -> list[int]:
    """
    Roll n_dice 6-sided dice and return the results
    """
    return [random.randint(1, 6) for _ in range(n_dice)]


@mcp.tool()
def add_number(a: float, b: float) -> float:
    """
    Add two numbers together
    """
    return a + b