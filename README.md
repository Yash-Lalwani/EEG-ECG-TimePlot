# EEG + ECG Visualization

This project loads raw EEG + ECG signals from a CSV file and generates an interactive Plotly visualization.  

---

## ⚡ How to Run

### 1. Clone or copy the repo
Make sure your CSV file (e.g., `EEG and ECG data_02_raw.csv`) is available in the project.

**Typical structure:**
```
project-root/
│── src/
│   └── plotter.py
│── data/
│   └── EEG and ECG data_02_raw.csv
│── requirements.txt
```

### 2. Create a virtual environment (recommended)
```
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies
Use a `requirements.txt` so everyone installs the same packages:

**Install from `requirements.txt`:**
```
pip install -r requirements.txt
```

**Example `requirements.txt` (copy into a file named `requirements.txt` in the project root):**
```
pandas==2.1.0
plotly==5.17.0
numpy>=1.25
```

*(Adjust versions as needed — pinning versions helps reproducibility.)*

### 4. Run the script
From the `src/` folder:
```
python plotter.py "../data/EEG and ECG data_02_raw.csv"
```

#### Optional flags:
- Save with a custom name:
  ```
  python plotter.py "../data/EEG and ECG data_02_raw.csv" --out myplot.html
  ```

- Convert ECG signals from μV to mV:
  ```
  python plotter.py "../data/EEG and ECG data_02_raw.csv" --convert-ecg
  ```

The output is an interactive HTML file (`eeg_ecg_plot.html` by default) that you can open in your browser.

---

## 🎨 Design Choices

### Usability
- The visualization supports scroll, zoom, hover, and hiding/showing channels via the legend.  
- A range slider is provided for fast navigation.

### EEG vs ECG Scaling
EEG signals (μV) are much smaller than ECG signals (mV). To keep both readable, a separate-subplot approach is used:

- **Top subplot**: EEG channels in μV  
- **Bottom subplot**: ECG + CM in μV or mV (optional `--convert-ecg`)  

This ensures EEG doesn’t flatten out under ECG scale.

### Code Quality
- The script is modular (`load_csv`, `find_columns`, `build_figure`, `main`) and flexible.  
- It auto-detects EEG, ECG, and CM columns without hardcoding positions.

---

## 🤖 Use of AI Assistance
I used AI (ChatGPT) as a coding assistant to:
- Break the problem into steps. 
- Learn Plotly syntax.  
- Debug errors.

---

## 🚀 Future Work
Given more time, I would add:
- Custom CSS & JS in the output HTML to improve readability and presentation of the graphs.  
  (For example: dark theme styling, better hover labels, and collapsible channel groups.)  
- Dropdown filters to select individual EEG channels or groups instead of plotting all 20 at once.  
- Annotations for highlighting significant events in the signals.  
- Export options (e.g., PNG, PDF snapshots of specific zoom levels).  

---

## 📸 Screenshots
