import streamlit as st
from core.auth import show_login
# Provide login view
def main():
    show_login()

if __name__ == "__main__":  # optionnel
    main()