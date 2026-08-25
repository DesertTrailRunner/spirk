# mcp_server.py
import os
import streamlit as st
from dotenv import load_dotenv
from fastmcp import FastMCP
from supabase import create_client, Client

load_dotenv()

def get_secret(key_name: str) -> str:
    # 1. Check Streamlit secrets first
    if hasattr(st, "secrets") and key_name in st.secrets:
        return st.secrets[key_name]
    # 2. Check local environment variables
    return os.getenv(key_name, "")

supabase_url = get_secret("SUPABASE_URL")
supabase_key = get_secret("SUPABASE_SERVICE_ROLE_KEY")

if not supabase_url or not supabase_key:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY environment variables.")

supabase: Client = create_client(supabase_url, supabase_key)

# Initialize the FastMCP instance
mcp = FastMCP("Workshop Survey Server")

@mcp.tool()
def save_teen_survey(name: str, age: int, favorite_tech: str) -> str:
    """Saves a teenager's survey responses into the Supabase database."""
    try:
        data = supabase.table("surveys").insert({
            "name": name,
            "age": age,
            "favorite_tech": favorite_tech
        }).execute()
        return f"Successfully saved response for {name}!"
    except Exception as e:
        return f"Database insertion failed: {str(e)}"