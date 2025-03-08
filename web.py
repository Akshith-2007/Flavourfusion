import streamlit as st
import google.generativeai as genai
import random

# ----------------------- Helper Functions -----------------------

def get_api_key():
    return "AIzaSyD_jB8En_E4vhuuTBiE9Ial1Zny2TwTM0c"

@st.cache_data
def generate_recipe(query, attempt=1):
    try:
        genai.configure(api_key=get_api_key())
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(query)
        if response and hasattr(response, 'text'):
            return response.text
        return "No recipe found: Try Again"
    except Exception as e:
        return f"Error fetching recipe: {e}"

def refine_query(query, cuisine, diet, time, budget):
    base_query = f"recipe for {query}" if "recipe" not in query.lower() else query
    filters = []
    if cuisine != "All": filters.append(f"{cuisine} cuisine")
    if diet != "All": filters.append(f"{diet}")
    if time != "All": filters.append(f"ready in {time}")
    if budget != "All": filters.append(f"{budget} budget")
    return f"Generate a {base_query} {' with '.join(filters) if filters else ''}"

# ----------------------- UI Configuration -----------------------
st.set_page_config(page_title="Flavour Fusion", page_icon="🍽", layout="wide")

# Custom Styling
st.markdown(
    """
    <style>
    body { background-color: #FAF3E0; color: #343a40; }
    .recipe-card { background: #fff; border-radius: 12px; padding: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); color: black; width: 100%; }
    .stButton>button { border-radius: 8px; padding: 10px 20px; font-size: 16px; }
    .search-btn { background-color: #FF5733; color: white; }
    .random-btn { background-color: #28A745; color: white; }
    .search-btn:hover { background-color: #C70039; }
    .random-btn:hover { background-color: #218838; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.image("https://png.pngtree.com/background/20230611/original/pngtree-many-different-kinds-of-food-are-arranged-on-a-table-picture-image_3145533.jpg", use_container_width=True)
st.title("🍽 Flavour Fusion: AI-Powered Recipe Blog")

# ----------------------- Filters -----------------------
st.subheader("🔍 Filter Your Recipe Search")
col1, col2, col3, col4 = st.columns(4)

with col1:
    cuisine_filter = st.selectbox("Cuisine Type", ["All", "Italian", "Indian", "Chinese", "Mexican", "French", "Mediterranean", "Japanese", "Thai", "American"], index=0)

with col2:
    dietary_filter = st.selectbox("Dietary Preferences", ["All", "Vegetarian", "Vegan", "Gluten-Free", "Keto", "High Protein", "Paleo", "Low-Carb"], index=0)

with col3:
    time_filter = st.selectbox("Cooking Time", ["All", "Under 15 minutes", "Under 30 minutes", "Under 1 hour", "More than 1 hour"], index=0)

with col4:
    budget_filter = st.selectbox("Budget", ["All", "Low", "Medium", "High"], index=0)

# ----------------------- User Input -----------------------
query = st.text_input("Enter ingredients, dish name, or dietary goal", placeholder="e.g., Spicy Tofu Stir-fry")

col1, col2 = st.columns(2)
with col1:
    if st.button("Search Recipes", key="search", help="Find a recipe", use_container_width=True, type="primary"):
        if query:
            refined_query = refine_query(query, cuisine_filter, dietary_filter, time_filter, budget_filter)
            recipe = generate_recipe(refined_query)
            st.markdown(f"<div class='recipe-card'><h3>Recipe for '{query}'</h3><p>{recipe}</p></div>", unsafe_allow_html=True)

with col2:
    if st.button("Surprise Me! 🎉", key="random", help="Get a random recipe", use_container_width=True, type="secondary"):
        random_query = random.choice(["pasta recipe", "healthy salad recipe", "easy chicken recipe", "vegetarian curry recipe", "vegan dessert recipe"])
        refined_random_query = refine_query(random_query, cuisine_filter, dietary_filter, time_filter, budget_filter)
        st.session_state["random_recipe"] = generate_recipe(refined_random_query)
        st.session_state["random_query"] = refined_random_query

if "random_recipe" in st.session_state:
    st.markdown(f"<div class='recipe-card'><h3>Random Recipe: {st.session_state['random_query'].capitalize()}</h3><p>{st.session_state['random_recipe']}</p></div>", unsafe_allow_html=True)

# ----------------------- About Section -----------------------
st.subheader("📌 About Flavour Fusion")
st.info("An AI-powered recipe blog to help you explore new flavors and cook delicious meals effortlessly.")

st.markdown("---")
st.markdown("Powered by Streamlit and Gemini 2.0 Flash")