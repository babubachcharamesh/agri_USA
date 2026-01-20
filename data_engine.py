import pandas as pd
import numpy as np

def generate_2025_ag_data():
    """Generates synthetic but realistic agriculture production data for 2025."""
    states = [
        "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", 
        "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", 
        "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", 
        "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", 
        "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", 
        "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", 
        "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", 
        "Wisconsin", "Wyoming"
    ]
    
    crops = ["Corn", "Soybeans", "Wheat", "Cotton", "Hay", "Rice", "Potatoes", "Sugarcane"]
    
    # State coordinates (rough centers for pydeck)
    state_coords = {
        "California": [36.7783, -119.4179],
        "Texas": [31.9686, -99.9018],
        "Iowa": [41.8780, -93.0977],
        "Illinois": [40.6331, -89.3985],
        "Nebraska": [41.1254, -98.2681],
        "Kansas": [38.5266, -96.7265],
        "Minnesota": [46.7296, -94.6859],
        "Indiana": [40.2672, -86.1349],
        "North Dakota": [47.5289, -99.7840],
        "South Dakota": [44.2998, -99.4388],
        "Ohio": [40.4173, -82.9071],
        "Wisconsin": [43.7844, -88.7879],
        "Missouri": [37.9643, -91.8318],
        "Arkansas": [34.9697, -92.3731],
        "North Carolina": [35.7596, -79.0193],
        "Michigan": [44.3148, -85.6024],
        "Washington": [47.7511, -120.7401],
        "Idaho": [44.0682, -114.7420],
        "Colorado": [39.5501, -105.7821],
        "Florida": [27.6648, -81.5158],
        "Georgia": [32.1656, -82.9001],
        "Mississippi": [32.3547, -89.3985],
        "Louisiana": [30.9843, -91.9623],
        "Oklahoma": [35.0078, -97.0929],
        "Kentucky": [37.8393, -84.2700],
        "Tennessee": [35.5175, -86.5804],
        "Alabama": [32.3182, -86.9023],
        "Montana": [46.8797, -110.3626],
        "Oregon": [43.8041, -120.5542],
        "Arizona": [34.0489, -111.0937],
        "New York": [43.0000, -75.0000],
        "Pennsylvania": [41.2033, -77.1945],
        "Virginia": [37.4316, -78.6569],
        "Utah": [39.3210, -111.4312],
        "Maryland": [39.0458, -76.6413],
        "New Jersey": [40.0583, -74.4057],
        "West Virginia": [38.5976, -80.4549],
        "South Carolina": [33.8361, -81.1637],
        "New Mexico": [34.5199, -105.8701],
        "Maine": [45.2538, -69.4455],
        "Nevada": [38.8026, -116.4194],
        "Wyoming": [43.0760, -107.2903],
        "New Hampshire": [43.1939, -71.5724],
        "Vermont": [44.5588, -72.5778],
        "Massachusetts": [42.4072, -71.3824],
        "Hawaii": [20.7967, -156.3319],
        "Rhode Island": [41.5801, -71.4774],
        "Connecticut": [41.6032, -73.0877],
        "Delaware": [38.9108, -75.5277],
        "Alaska": [63.5867, -154.4931],
    }

    data = []
    for state in states:
        lat, lon = state_coords.get(state, [39.8283, -98.5795])
        for crop in crops:
            # Base production with state-specific weights and random variability for 2025
            base = np.random.randint(10, 500)
            if state in ["Iowa", "Illinois", "Nebraska"] and crop == "Corn":
                base *= 10
            elif state == "California" and crop == "Fruits":
                base *= 15
            elif state == "Idaho" and crop == "Potatoes":
                base *= 8
            
            yield_per_acre = np.random.uniform(50, 200)
            total_production = base * yield_per_acre
            market_value = total_production * np.random.uniform(2, 10)
            
            data.append({
                "State": state,
                "Crop": crop,
                "Latitude": lat,
                "Longitude": lon,
                "Production_MT": round(total_production, 2),
                "Market_Value_USD": round(market_value, 2),
                "Yield_Index": round(np.random.uniform(0.8, 1.2), 2)
            })
            
    return pd.DataFrame(data)

def get_ticker_data():
    """Mock live ticker data for 2025 commodities."""
    commodities = [
        {"name": "Corn", "price": 4.56, "change": +0.12},
        {"name": "Soybeans", "price": 12.45, "change": -0.05},
        {"name": "Wheat", "price": 6.78, "change": +0.34},
        {"name": "Cotton", "price": 0.89, "change": -0.01},
        {"name": "Sugar", "price": 0.22, "change": +0.02},
    ]
    return commodities

def create_pdf_report(df, filename="agri_report_2025.pdf"):
    """Generates a PDF report from the dataframe using fpdf2."""
    from fpdf import FPDF
    
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 14)
            self.cell(0, 10, 'USA Agriculture 2025 - Production Report (Values in Millions)', 0, 1, 'C')
            self.ln(10)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    
    # Table Header
    cols = ["State", "Crop", "Production_MT", "Market_Value_USD"]
    pdf.set_fill_color(200, 220, 255)
    for col in cols:
        pdf.cell(45, 10, col, 1, 0, 'C', 1)
    pdf.ln()

    # Table Data (Full data)
    pdf.set_fill_color(255, 255, 255)
    for index, row in df.iterrows():
        # Check for page break to re-add header if necessary
        # FPDF automatically adds pages, but we can override if we want headers on every page.
        # For simplicity in this "mind-blowing" app, let's keep it clean.
        pdf.cell(45, 10, str(row['State']), 1)
        pdf.cell(45, 10, str(row['Crop']), 1)
        pdf.cell(45, 10, f"{row['Production_MT']:.2f}", 1)
        pdf.cell(45, 10, f"${row['Market_Value_USD']:.2f}", 1)
        pdf.ln()
    
    return bytes(pdf.output())

if __name__ == "__main__":
    df = generate_2025_ag_data()
    print(df.head())
