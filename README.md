# 🌾 USA Agriculture 2025 | Strategic Mission Control

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

An advanced, high-resolution agricultural analytics platform designed to visualize and project USA crop production and market values for the year 2025. Built with a "Neon Cosmic" aesthetic, the dashboard provides interactive 3D mapping, market dynamics, and AI-driven sustainability insights.

## ✨ Core Features

- **🚀 Interactive 3D Production Map**: High-fidelity ColumnLayer visualizations representing metric tons of production across the US.
- **📍 State-Level Deep-Dives**: Zoom and filter by specific states to reveal localized agricultural performance.
- **📊 Executive Summary**: A persistent "Mission Control" header providing real-time totals for Production, Market Value, and Primary Crops based on active filters.
- **📈 Market Analytics**: Interactive Plotly visualizations for value distribution and yield comparisons.
- **🤖 AI Insights**: Simulation of resource optimization and climate resilience projections.
- **📥 Data Export Hub**: Dual-mode export functionality (CSV & PDF) that respects your active filters.
- **🔍 Precision Formatting**: Professional number scaling (Millions/Billions/Trillions) for clear reading of national-scale data.

## 🛠️ Technology Stack

- **Frontend/Backend**: [Streamlit](https://streamlit.io/)
- **Visualizations**: [Pydeck](https://deckgl.github.io/pydeck/) (3D Maps), [Plotly Express](https://plotly.com/python/plotly-express/) (Charts)
- **Report Generation**: [fpdf2](https://github.com/fpdf2/fpdf2)
- **Data Engine**: Pandas & NumPy for synthetic but realistic 2025 projections.

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- `uv` (recommended) or `pip`

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/USA_agriculture.git
   cd USA_agriculture
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run main.py
   ```

## 📋 Data Disclosure

> [!IMPORTANT]
> **Units**: All numerical values in the system represent base units in **Millions (M)**. 
> For example:
> - `10.00M` = 10,000,000
> - `1.50B` = 1,500,000,000
> - `2.10T` = 2,100,000,000,000

The data used in this dashboard isUSDA-simulated and represents projections for the 2025 agricultural cycle.

## ☁️ Deployment

This project is optimized for deployment on **Streamlit Cloud**.

- **Runtime**: `python-3.12`
- **Theme**: Automatically enforced via `.streamlit/config.toml` (Cosmic Dark).
- **Entry Point**: `main.py`

## 📄 License

© 2025 USA Agriculture Vision. Built for Advanced Agricultural Analytics.
