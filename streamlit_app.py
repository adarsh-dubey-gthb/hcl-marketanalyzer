"""Streamlit Community Cloud Entrypoint.

Forwards execution to the main application dashboard in app.py.
"""
import runpy
import sys

if __name__ == "__main__" or "streamlit" in sys.modules:
    runpy.run_path("app.py", run_name="__main__")
