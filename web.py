import streamlit as st
import google.generativeai as genai
import random
import sqlite3
from PIL import Image
import os
import requests

def get_api_key():
    return "AIzaSyD_jB8En_E4vhuuTBiE9Ial1Zny2TwTM0c"

def generate_recipe(query):
    try:
        genai.configure(api_key=get_api_key())
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(query)
        return response.text if response and hasattr(response, 'text') else "No recipe found."
    except Exception as e:
        return f"Error fetching recipe: {e}"

def get_youtube_link(query):
    search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}+recipe"
    return search_url

def refine_query(query, cuisine, diet, time, budget, spice, meal_type):
    base_query = f"recipe for {query}" if "recipe" not in query.lower() else query
    filters = [
        f"{cuisine} cuisine" if cuisine != "All" else "", 
        f"{diet}" if diet != "All" else "", 
        f"ready in {time}" if time != "All" else "", 
        f"{budget} budget" if budget != "All" else "",
        f"{spice} spice level" if spice != "All" else "",
        f"{meal_type}" if meal_type != "All" else ""
    ]
    return f"Generate a {base_query} {' with '.join(filter(None, filters))}"

def setup_database():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

st.set_page_config(page_title="Flavour Fusion", page_icon="🍽", layout="wide")

setup_database()

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.image("https://png.pngtree.com/background/20230611/original/pngtree-many-different-kinds-of-food-are-arranged-on-a-table-picture-image_3145533.jpg", use_container_width=True)
    st.title("🍽 Flavour Fusion: AI-Powered Recipe Blog")
    selected_tab = st.radio("Choose an option", ["Sign Up", "Login"], horizontal=True)
    
    if selected_tab == "Sign Up":
        st.subheader("👤 Sign Up")
        new_username = st.text_input("Choose a Username")
        new_password = st.text_input("Choose a Password", type="password")
        if st.button("Sign Up"):
            if register_user(new_username, new_password):
                st.success("Registration successful! Please log in.")
            else:
                st.error("Username already exists!")
    
    elif selected_tab == "Login":
        st.subheader("🔑 Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if authenticate_user(username, password):
                st.session_state["authenticated"] = True
                st.success("Login successful! Redirecting...")
                st.rerun()
            else:
                st.error("Invalid credentials")
else:
    st.image("https://wallpapers.com/images/featured/1pf6px6ryqfjtnyr.jpg", use_container_width=True)
    st.title("🍽 Flavour Fusion: AI-Powered Recipe Blog")
    
    st.sidebar.header("🔍 Filter Your Recipes")
    cuisine = st.sidebar.selectbox("Cuisine", ["All", "Italian", "Indian", "Chinese", "Mexican", "French", "Mediterranean"])
    diet = st.sidebar.selectbox("Diet", ["All", "Vegetarian", "Vegan", "Gluten-Free", "Keto", "Paleo"])
    time = st.sidebar.selectbox("Cooking Time", ["All", "Under 15 min", "Under 30 min", "Under 1 hour", "More than 1 hour"])
    budget = st.sidebar.selectbox("Budget", ["All", "Low", "Medium", "High"])
    spice = st.sidebar.selectbox("Spice Level", ["All", "Mild", "Medium", "Spicy", "Very Spicy"])
    meal_type = st.sidebar.selectbox("Meal Type", ["All", "Breakfast", "Lunch", "Dinner", "Snack", "Dessert"])
    
    query = st.text_input("Enter ingredients or dish name", placeholder="e.g., Spicy Tofu Stir-fry")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Search Recipe"):
            if query:
                refined_query = refine_query(query, cuisine, diet, time, budget, spice, meal_type)
                recipe = generate_recipe(refined_query)
                youtube_link = get_youtube_link(query)
                
                st.markdown(f"""
                <div style='background: white; padding: 20px; border-radius: 10px; color: black;'>
                    <h3>Recipe: {query}</h3>
                    <p>{recipe}</p>
                    <p><a href='{youtube_link}' target='_blank'>📺 Watch on YouTube</a></p>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        if st.button("Surprise Me! 🎉"):
            random_query = "random recipe"
            refined_random_query = refine_query(random_query, cuisine, diet, time, budget, spice, meal_type)
            random_recipe = generate_recipe(refined_random_query)
            youtube_link = get_youtube_link(random_query)
            
            st.markdown(f"""
            <div style='background: white; padding: 20px; border-radius: 10px; color: black;'>
                <h3>Random Recipe</h3>
                <p>{random_recipe}</p>
                <p><a href='{youtube_link}' target='_blank'>📺 Watch on YouTube</a></p>
            </div>
            """, unsafe_allow_html=True)
