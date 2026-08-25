import os
from dotenv import load_dotenv
from fastmcp import FastMCP
from supabase import create_client, Client

load_dotenv()

# Initialize Supabase Client
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# Initialize FastMCP Server
mcp = FastMCP("Workshop Survey Server")

@mcp.tool()
def save_teen_survey(name: str, age: int, favorite_tech: str) -> str:
    """Saves a teenager's survey responses into the Supabase database.
    
    Args:
        name: Name or nickname of the teenager.
        age: Age of the teenager in years.
        favorite_tech: What technology/app they like the most.
    """
    try:
        data, count = supabase.table("surveys").insert({
            "name": name,
            "age": age,
            "favorite_tech": favorite_tech
        }).execute()
        return f"Successfully saved response for {name}!"
    except Exception as e:
        return f"Database insertion failed: {str(e)}"

if __name__ == "__main__":
    mcp.run()