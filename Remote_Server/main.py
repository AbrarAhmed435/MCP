import sqlite3
from mcp.server.fastmcp import FastMCP
import os
import json
import random


mcp=FastMCP("Calculator-server")

@mcp.tool()
def add(a:int,b:int)->int:
    """
    Add two numbers together
    Args:
    a:first number
    b:second number
    """
    return a+b

@mcp.tool()
def random_number(min_val:int=1,max_val:int=100)->int:
    """
    Generates a randm number between max and min val
    """
    return random.randint(min_val,max_val)


# @mcp.custom_route("/")
# async def home(request):
#     # return PlainTextResponse("Server running")
#     return {
#         "message":"Hello how are you?"
#     }

@mcp.resource("info://server")
def server_info()->str:
    """
    Get information about this server
    """
    info={
        "name":"simple Calculator Server",
        "version":"1.0.0",
        "description":"A basic MCP server with main tools",
        "tools":["add","random_number"],
        "author":"Your Name"
    }
    return json.dumps(info,indent=2)




if __name__=="__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
    # mcp.run()


    





