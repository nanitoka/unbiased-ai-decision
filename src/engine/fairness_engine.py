import pandas as pd

def run_fairness_audit(data):
    data.columns = [col.strip().lower() for col in data.columns]
    
    # Identify Columns
    outcome_col = next((c for c in ["approved", "prediction", "y_pred", "selected", "approval"] if c in data.columns), None)
    truth_col = next((c for c in ["label", "actual", "y_true", "truth"] if c in data.columns), None)
    protected_cols = [c for c in data.columns if any(attr in c for attr in ["gender", "race", "age", "ethnicity"])]

    if not outcome_col:
        return None, "Outcome column not found."
    if not protected_cols:
        return None, "Protected attributes not found."

    # Data Cleaning
    data[outcome_col] = pd.to_numeric(data[outcome_col], errors='coerce').fillna(0)
    if truth_col:
        data[truth_col] = pd.to_numeric(data[truth_col], errors='coerce').fillna(0)

    all_results = {}

    for attr in protected_cols:
        groups = data[attr].unique()
        if len(groups) < 2: continue
        
        rates = data.groupby(attr)[outcome_col].mean()
        privileged_group = rates.idxmax()
        unprivileged_groups = [g for g in groups if g != privileged_group]
        
        group_metrics = []
        for group in unprivileged_groups:
            p_priv = rates[privileged_group]
            p_unpriv = rates[group]
            
            metrics = {
                "group": str(group),
                "baseline": str(privileged_group),
                "rates": {"privileged": round(p_priv, 2), "unprivileged": round(p_unpriv, 2)},
                "demographic_parity_diff": round(p_priv - p_unpriv, 2),
                "disparate_impact_ratio": round(p_unpriv / p_priv if p_priv != 0 else 1.0, 2),
            }

            if truth_col:
                priv_df = data[data[attr] == privileged_group]
                unpriv_df = data[data[attr] == group]
                
                tpr_priv = priv_df[priv_df[truth_col] == 1][outcome_col].mean() if len(priv_df[priv_df[truth_col] == 1]) > 0 else 0
                tpr_unpriv = unpriv_df[unpriv_df[truth_col] == 1][outcome_col].mean() if len(unpriv_df[unpriv_df[truth_col] == 1]) > 0 else 0
                
                metrics["equal_opportunity_diff"] = round(abs(tpr_priv - tpr_unpriv), 2)
                metrics["accuracy_diff"] = round(abs((priv_df[outcome_col] == priv_df[truth_col]).mean() - (unpriv_df[outcome_col] == unpriv_df[truth_col]).mean()), 2)

            group_metrics.append(metrics)
        all_results[attr] = group_metrics

    return all_results, None
