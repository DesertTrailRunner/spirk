# mcp_server.py
import os
import streamlit as st
from dotenv import load_dotenv
from fastmcp import FastMCP
from supabase import create_client, Client

load_dotenv()  # Loads variables from your local .env file

# Helper function to get secrets from Streamlit Cloud OR local .env
def get_secret(key_name: str) -> str:
    # 1. Check Streamlit Secrets first (for Cloud Deployment)
    if hasattr(st, "secrets") and key_name in st.secrets:
        return st.secrets[key_name]
    # 2. Check system/local environment variables (for Local Dev)
    return os.getenv(key_name, "")

# Instantiate the Supabase database client here
supabase_url = get_secret("SUPABASE_URL")
supabase_key = get_secret("SUPABASE_SERVICE_ROLE_KEY")

# Sanity check to prevent hard crashes with a clear error message
if not supabase_url or not supabase_key:
    raise ValueError(
        f"Missing Supabase configuration! URL: {'Found' if supabase_url else 'Missing'}, "
        f"Key: {'Found' if supabase_key else 'Missing'}"
    )

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