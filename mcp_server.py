# mcp_server.py
import os
from dotenv import load_dotenv
from fastmcp import FastMCP
from supabase import create_client, Client

load_dotenv()  # Loads variables from your local .env file

# Instantiate the Supabase database client here
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase: Client = create_client(supabase_url, supabase_key)

mcp = FastMCP("EY Nottingham Spirk Touchpoint")

@mcp.tool()
def save_teen_survey(name: str, age: int, favorite_tech: str) -> str:
    # Uses the instantiated client to insert rows into Supabase
    supabase.table("surveys").insert({
        "name": name,
        "age": age,
        "favorite_tech": favorite_tech
    }).execute()
    return "Saved successfully!"