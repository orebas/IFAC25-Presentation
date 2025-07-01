import pandas as pd
import numpy as np

def format_latex_cell(val, is_deriv=False):
    """Formats a number into a complete, color-coded LaTeX cell string."""
    if pd.isna(val) or np.isinf(val):
        return r"\textcolor{errorred}{FAIL}"

    # Determine thresholds for coloring
    threshold_bad = 1e3 if is_deriv else 1.0
    threshold_good = 10 if is_deriv else 0.1

    # Format the number string
    if val == 0.0:
        num_str = "0.00"
    elif 1e-2 <= abs(val) < 100:
        num_str = f"{val:.2f}"
    else:
        # Format for scientific notation and wrap in math mode
        num_str = f"{val:.1e}".replace("e-0", "e-").replace("e+0", "e").replace("e-", "e-").replace("e+", "e")
        num_str = f"${num_str}$"

    # Apply color
    if val > threshold_bad:
        return r"{\color{errorred}" + num_str + "}"
    if val < threshold_good:
        return r"{\color{successgreen}" + num_str + "}"
    
    return num_str

def generate_latex_table(df, deriv_order, filename):
    """Generates a LaTeX table from the dataframe for a specific derivative order."""
    is_deriv = deriv_order > 0
    table_data = df[['method', 'noise_level', str(deriv_order)]].copy()
    table_pivot = table_data.pivot(index='method', columns='noise_level', values=str(deriv_order))
    try:
        table_pivot = table_pivot.reindex([0.0, 1e-6, 0.001], axis=1)
    except KeyError:
        print(f"Warning: Could not find all noise levels for deriv {deriv_order}. Columns might be missing.")
        
    with open(filename, 'w') as f:
        f.write(r"\begin{tabular}{@{}l|ccc@{}}" + "\n")
        f.write(r"\toprule" + "\n")
        f.write(r"\textbf{Method} & \textbf{Noise = 0} & \textbf{Noise = 1e-6} & \textbf{Noise = 1e-3} \\" + "\n")
        f.write(r"\midrule" + "\n")

        for method, row in table_pivot.iterrows():
            method_name = method.replace("_", r"\_")
            if method == 'GPR_Julia':
                method_name = f"\\textbf{{{method_name}}}"

            col0 = format_latex_cell(row.get(0.0), is_deriv)
            col1 = format_latex_cell(row.get(1e-6), is_deriv)
            col2 = format_latex_cell(row.get(0.001), is_deriv)
            
            f.write(f"{method_name} & {col0} & {col1} & {col2} \\\\\n")

        f.write(r"\bottomrule" + "\n")
        f.write(r"\end{tabular}" + "\n")

def main():
    """Main function to generate both appendix tables."""
    try:
        df = pd.read_csv('pivot_rmse_wide_format.csv')
    except FileNotFoundError:
        print("Error: pivot_rmse_wide_format.csv not found.")
        return

    # Filter for the methods the user wants to keep
    methods_to_keep = [
        'AAA_Julia', 'Butterworth_Python', 'Chebyshev_Python', 'FiniteDiff_Python',
        'GPR_Julia', 'GP_RBF_Iso_Python', 'KalmanGrad_Python', 'LOESS_Julia',
        'SVR_Python', 'SavitzkyGolay_Python', 'TVDiff_Julia'
    ]
    filtered_df = df[df['method'].isin(methods_to_keep)].copy()
    
    generate_latex_table(filtered_df, 0, 'appendix_table_d0.tex')
    print("Generated appendix_table_d0.tex")
    
    generate_latex_table(filtered_df, 3, 'appendix_table_d3.tex')
    print("Generated appendix_table_d3.tex")

if __name__ == '__main__':
    main() 