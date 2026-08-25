# mcp_server.py
import os
import streamlit as st
from fastmcp import FastMCP
from dotenv import load_dotenv
from supabase import create_client, Client
from langchain_core.tools import tool

load_dotenv()

# mcp = FastMCP("survey-server")

def get_secret(key_name: str) -> str:
    try:
        if key_name in st.secrets:
            return st.secrets[key_name]
    except Exception:
        pass
    return os.getenv(key_name, "")

supabase_url = get_secret("SUPABASE_URL")
supabase_key = get_secret("SUPABASE_SERVICE_ROLE_KEY")

if not supabase_url or not supabase_key:
    # Safe error context for app initialization
    st.error("⚠️ Database connection parameters are missing. Please check your secrets configuration.")

try:
    supabase: Client = create_client(supabase_url, supabase_key)
except Exception as e:
    supabase = None

@tool
def save_teen_survey(name: str, age: int, favorite_tech: str) -> str:
    """Saves a teenager's survey responses into the Supabase database.
    
    Args:
        name: Name or nickname of the teenager.
        age: Age of the teenager in years.
        favorite_tech: What technology/app they like the most.
    """
    if not supabase:
        return "ERROR: Database client is not connected."

    try:
        data = supabase.table("surveys").insert({
            "name": name,
            "age": int(age),
            "favorite_tech": favorite_tech
        }).execute()
        return f"SUCCESS: Saved response for {name}!"
    except Exception as e:
        # Catch network timeouts, invalid schema types, or permission errors
        return f"ERROR: Could not complete save operation - {str(e)}"