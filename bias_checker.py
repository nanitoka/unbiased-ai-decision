import pandas as pd

def analyze_bias(file_path):
    data = pd.read_csv(file_path)

    # Basic validation
    if "gender" not in data.columns or "approved" not in data.columns:
        print("❌ Required columns missing (gender, approved)")
        return

    male = data[data["gender"] == "M"]
    female = data[data["gender"] == "F"]

    male_rate = male["approved"].mean()
    female_rate = female["approved"].mean()

    diff = male_rate - female_rate

    print("\n📊 BIAS ANALYSIS REPORT")
    print("---------------------------")
    print(f"Male Approval Rate   : {round(male_rate, 2)}")
    print(f"Female Approval Rate : {round(female_rate, 2)}")
    print(f"Difference           : {round(diff, 2)}")

    # Fairness check (80% rule concept)
    ratio = female_rate / male_rate if male_rate != 0 else 0
    print(f"Disparate Impact Ratio: {round(ratio, 2)}")

    if ratio < 0.8:
        print("⚠️ Potential Bias Detected (Below 0.8 threshold)")
    else:
        print("✅ Fair System (Within acceptable range)")

# Run analysis
analyze_bias("data.csv")