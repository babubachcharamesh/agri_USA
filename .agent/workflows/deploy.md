---
description: How to deploy the USA Agriculture 2025 app to Streamlit Cloud
---

# 🚀 Deployment Guide

Follow these steps to deploy your "USA Agriculture 2025" dashboard to **streamlit.app**.

## 1. Push to GitHub
Ensure all files are committed and pushed to a public or private GitHub repository.
- Required files: `main.py`, `data_engine.py`, `requirements.txt`, `runtime.txt`, `assets/`, and `.streamlit/config.toml`.

## 2. Connect to Streamlit Cloud
1.  Go to [share.streamlit.io](https://share.streamlit.io/).
2.  Click **"Create app"**.
3.  Choose your repository: `USA_agriculture`.
4.  Set the **Main file path** to `main.py`.
5.  (Advanced) Click **Advanced settings** and ensure the Python version is set to **3.12**.

## 3. Launch
Click **Deploy!**. Streamlit will automatically:
- Install dependencies from `requirements.txt`.
- Set up the Python environment from `runtime.txt`.
- Apply your custom neon theme from `.streamlit/config.toml`.

Your app will be live at a URL like `https://usa-agriculture-2025.streamlit.app`.
