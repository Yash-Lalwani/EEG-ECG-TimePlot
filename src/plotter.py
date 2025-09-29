"""
plot_eeg_ecg.py
Usage:
    python plot_eeg_ecg.py "EEG and ECG data_02_raw.csv" --out out.html --convert-ecg
"""

import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import argparse

# 1: Load CSV
def load_csv(path):
    """
    Load the CSV file, ignoring lines that start with '#'.
    """
    df = pd.read_csv(path, comment='#')
    return df

# 2: Known EEG channels
EEG_CHANNELS = [
    "Fz","Cz","P3","C3","F3","F4","C4","P4","Fp1","Fp2",
    "T3","T4","T5","T6","O1","O2","F7","F8","A1","A2","Pz"
]

# 3: Detect columns
def find_columns(df):
    """
    Identify which columns are Time, EEG, ECG, and CM.
    Returns a tuple: (time_col, eeg_cols, ecg_cols, cm_col)
    """
    cols = df.columns.tolist()

    # Time column
    time_col = None
    for c in cols:
        if c.lower().startswith("time"):
            time_col = c
            break

    # EEG columns
    eeg_cols = []
    for c in cols:
        if c in EEG_CHANNELS:
            eeg_cols.append(c)

    # ECG columns (X1:LEOG, X2:REOG)
    ecg_cols = [
        c for c in cols
        if c.upper().startswith('X1') or c.upper().startswith('X2')
        or 'LEOG' in c.upper() or 'REOG' in c.upper()
    ]

    # CM column
    cm_col = next((c for c in cols if c.upper() == 'CM'), None)

    return time_col, eeg_cols, ecg_cols, cm_col

# 5: Build figure
def build_figure(df, time_col, eeg_cols, ecg_cols, cm_col, convert_ecg_to_mV=False):
    """
    Build a figure with two subplots:
    - Row 1: EEG channels
    - Row 2: ECG channels + CM
    """
    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        row_heights=[0.7, 0.3], vertical_spacing=0.03,
        subplot_titles=("EEG channels (µV)", "ECG & CM")
    )

    # EEG traces
    for ch in eeg_cols:
        fig.add_trace(
            go.Scatter(x=df[time_col], y=df[ch], name=ch, mode="lines"),
            row=1, col=1
        )

    # ECG traces (convert to mV if asked)
    for ch in ecg_cols:
        y = df[ch]
        if convert_ecg_to_mV:
            y = y / 1000.0
        fig.add_trace(
            go.Scatter(x=df[time_col], y=y, name=ch, mode="lines"),
            row=2, col=1
        )

    # CM trace
    if cm_col:
        fig.add_trace(
            go.Scatter(x=df[time_col], y=df[cm_col], name="CM", mode="lines", opacity=0.7),
            row=2, col=1
        )

    # Labels + layout
    fig.update_xaxes(title_text="Time (s)", rangeslider=dict(visible=True))
    fig.update_layout(
        height=800,
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig.update_yaxes(title_text="µV", row=1, col=1)
    bottom_unit = "mV" if convert_ecg_to_mV else "µV"
    fig.update_yaxes(title_text=bottom_unit, row=2, col=1)

    return fig

# 6: Main program
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", help="path to CSV file")
    parser.add_argument("--out", default="eeg_ecg_plot.html", help="output HTML file")
    parser.add_argument("--convert-ecg", action="store_true", help="divide ECG channels by 1000 (µV -> mV)")
    args = parser.parse_args()

    # Load data
    df = load_csv(args.csv)
    time_col, eeg_cols, ecg_cols, cm_col = find_columns(df)

    print("Detected columns:")
    print(" Time:", time_col)
    print(" EEG:", eeg_cols)
    print(" ECG:", ecg_cols)
    print(" CM:", cm_col)

    if time_col is None:
        raise SystemExit("Could not find a Time column in the CSV.")

    # Build and save figure
    fig = build_figure(df, time_col, eeg_cols, ecg_cols, cm_col, convert_ecg_to_mV=args.convert_ecg)
    fig.write_html(args.out, include_plotlyjs="cdn")
    print("Wrote interactive plot to", args.out)

if __name__ == "__main__":
    main()