import pandas as pd
import numpy as np

def generate_loan_data(n=10000):
    np.random.seed(42)
    
    # Features
    genders = np.random.choice(['M', 'F'], n)
    incomes = np.random.normal(60000, 20000, n).clip(20000, 200000)
    credit_scores = np.random.randint(300, 850, n)
    loan_amounts = np.random.normal(200000, 100000, n).clip(10000, 1000000)
    employment_years = np.random.randint(0, 40, n)
    
    # Generate hidden "Approval Score" (0 to 1)
    # Base score on income, credit, employment
    score = (
        0.3 * (incomes / 200000) +
        0.5 * (credit_scores / 850) +
        0.2 * (employment_years / 40)
    )
    
    # Add slight noise
    score += np.random.normal(0, 0.05, n)
    
    # Introduce Bias: Boost males by 5%
    score = np.where(genders == 'M', score + 0.05, score)
    score = score.clip(0, 1)
    
    # Create final binary approval (base threshold 0.6)
    approved = (score >= 0.6).astype(int)
    
    df = pd.DataFrame({
        'gender': genders,
        'income': incomes.round(0),
        'credit_score': credit_scores,
        'loan_amount': loan_amounts.round(0),
        'employment_years': employment_years,
        'score': score.round(4), # Added for the simulator
        'approved': approved
    })
    
    df.to_csv('loan_data_10k.csv', index=False)
    print("Dataset 'loan_data_10k.csv' generated with 10,000 rows.")

if __name__ == "__main__":
    generate_loan_data()
