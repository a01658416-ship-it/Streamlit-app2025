import streamlit as st

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="Crime Data Analytics Dashboard",
    page_icon="🗺️",
    layout="wide"
)

# Session state initialization
if "role" not in st.session_state:
    st.session_state.role = None

ROLES = [None, "PC", "Professor", "Team", "Thales Partner"]

def login():
    st.header("🔐 Log in")
    st.markdown("### Crime Data Analytics AI - Mexico City")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("---")
        role = st.selectbox("Choose your role *", ROLES)
        
        st.markdown("""
        **Role Descriptions:**
        - **PC**: Access to visualizations only
        - **Professor**: Full access to all features
        - **Team**: Full access to all features
        - **Thales Partner**: Access to visualizations and ML analysis
        """)
        
        if st.button("Log in", type="primary", use_container_width=True):
            st.session_state.role = role
            st.rerun()

def logout():
    st.sidebar.markdown("---")
    st.sidebar.header("👤 User Session")
    st.sidebar.write(f"**Role:** {st.session_state.role}")
    
    if st.sidebar.button("🚪 Log out", use_container_width=True):
        st.session_state.role = None
        st.rerun()

# Get current role
role = st.session_state.role

# Define pages based on roles
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
settings = st.Page("settings.py", title="Settings", icon=":material/settings:")

# Visualization pages
visualization = st.Page(
    "Visualization/visualization.py",
    title="Dashboard",
    icon="🗺️",
    default=(role == "PC"),
)
maps = st.Page(
    "Visualization/maps.py",
    title="Interactive Maps",
    icon="🌍",
)
maps2 = st.Page(
    "Visualization/maps2.py",
    title="Advanced Maps",
    icon="📍",
)

# ML pages
ml = st.Page(
    "ml/ml_analysis.py",
    title="Machine Learning",
    icon="🤖",
    default=(role == "Thales Partner"),
)

# EDA pages
eda = st.Page(
    "EDA/eda.py",
    title="Exploratory Data Analysis",
    icon="📊",
    default=(role == "Professor"),
)

# Configure pages based on role
if role is not None:
    # Add logo and title
    st.logo("images/horizontal_blue.png", icon_image="images/icon_blue.png")
    st.title("🗺️ Crime Data Analytics AI - Mexico City")
    
    # Call logout in sidebar
    logout()
    
    page_dict = {}
    
    # Define access permissions
    if role in ["Professor", "Team"]:
        # Full access
        page_dict["📊 EDA"] = [eda]
        page_dict["🗺️ Visualization"] = [visualization, maps, maps2]
        page_dict["🤖 Machine Learning"] = [ml]
        page_dict["⚙️ Account"] = [settings]
    
    elif role == "Thales Partner":
        # Visualization + ML access
        page_dict["🗺️ Visualization"] = [visualization, maps, maps2]
        page_dict["🤖 Machine Learning"] = [ml]
        page_dict["⚙️ Account"] = [settings]
    
    elif role == "PC":
        # Visualization only
        page_dict["🗺️ Visualization"] = [visualization, maps, maps2]
        page_dict["⚙️ Account"] = [settings]
    
    # Create navigation
    if len(page_dict) > 0:
        pg = st.navigation(page_dict)
    else:
        st.warning("No pages available for your role.")
        pg = st.navigation([st.Page(login)])
else:
    # Not logged in - show login page
    pg = st.navigation([st.Page(login)])

pg.run()