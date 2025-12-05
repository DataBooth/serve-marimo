import streamlit as st
from pathlib import Path
from loguru import logger
import sys
import os


# Always initialise session state variables at the top
if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False


class AuthenticatedNotebookApp:
    def __init__(self):
        self.root_dir = Path(__file__).resolve().parent.parent
        self.notebooks_dir = self.root_dir / "notebooks"
        self.marimo_base_url = os.environ.get(
            "MARIMO_BASE_URL", "http://localhost:8000/notebooks"
        )
        self.providers = ["Google", "Apple"]
        logger.info(
            f"App initialised. Project root: {self.root_dir}, Notebooks dir: {self.notebooks_dir}"
        )

    def sidebar_auth(self):
        with st.sidebar:
            st.header("Sign in")
            provider = st.selectbox("Choose sign-in provider", self.providers)
            if st.button("Sign in with selected provider"):
                logger.info(f"OIDC sign-in requested for provider: {provider}")
                st.login(provider.lower())
            st.markdown("---")
            self.admin_login()

    def admin_login(self):
        st.subheader("Admin sign in")
        username = st.text_input("Admin username", value="admin", key="admin_username")

        password = st.text_input(
            "Admin password", type="password", key="admin_password"
        )
        if st.button("Admin sign in"):
            admin_password = st.secrets.get("admin_password", "")
            if username == "admin" and password == admin_password:
                st.session_state["admin_logged_in"] = True
                logger.info("Admin sign-in successful")
                st.success("Admin sign-in successful!")
                st.rerun()
            else:
                logger.warning("Invalid admin credentials")
                st.error("Incorrect admin username or password.")

    def logout(self):
        with st.sidebar:
            if st.button("Sign out"):
                if st.user.is_logged_in:
                    logger.info("OIDC user signing out")
                    st.logout()
                st.session_state["admin_logged_in"] = False
                logger.info("Admin user signed out")
                st.rerun()

    def list_notebooks(self):
        if not self.notebooks_dir.exists():
            logger.error(f"Notebooks directory does not exist: {self.notebooks_dir}")
            st.error(f"Couldn’t find the notebooks directory: {self.notebooks_dir}")
            return []
        notebooks = sorted([p for p in self.notebooks_dir.glob("*.py")])
        logger.info(
            f"Found {len(notebooks)} notebook(s): {[n.name for n in notebooks]}"
        )
        return notebooks

    def show_notebooks(self):
        st.header("Available Marimo Notebooks")
        notebooks = self.list_notebooks()
        if not notebooks:
            st.warning("No notebooks found in the notebooks directory.")
            return
        for nb in notebooks:
            notebook_name = nb.stem  # 'simple_demo' instead of 'simple_demo.py'
            url = f"{self.marimo_base_url}/{notebook_name}"
            st.markdown(f"- [{nb.name}]({url})")

    def run(self):
        st.title("Marimo notebook launcher")
        # Always use session state for authentication checks
        if not st.user.is_logged_in and not st.session_state["admin_logged_in"]:
            self.sidebar_auth()
            st.info("Please sign in using the sidebar to access your notebooks.")
        else:
            st.write(f"Welcome, {st.user.name if st.user.is_logged_in else 'Admin'}!")
            self.logout()
            self.show_notebooks()


if __name__ == "__main__":
    try:
        logger.info("Starting AuthenticatedNotebookApp")
        app = AuthenticatedNotebookApp()
        app.run()
        logger.info("App ran successfully")
    except Exception as e:
        logger.exception(f"Error running Streamlit app: {e}")
        st.error(f"An error occurred: {e}")
