import pandas as pd
import numpy as np

def find_best_solution_for_group(df):
    """
    For a given DataFrame subset (a single experimental group), this function
    identifies the best solution according to the metric:
    1. Find the best cluster (minimum of the maximum relative errors).
    2. Find the best solution within that cluster (minimum of the mean relative errors).
    """
    if df.empty:
        return None
    
    # Find the best cluster: the one with the minimum-of-maximum parameter error
    param_df = df[df['variable_type'] == 'parameter']
    if param_df.empty:
        return None # No parameters to judge by

    cluster_max_errors = param_df.groupby('cluster_id')['rel_error'].max()
    if cluster_max_errors.empty:
        return None
        
    best_cluster_id = cluster_max_errors.idxmin()
    best_cluster_df = df[df['cluster_id'] == best_cluster_id]

    # Within that cluster, find the best solution (minimum mean parameter error)
    solution_mean_errors = best_cluster_df[best_cluster_df['variable_type'] == 'parameter'].groupby('solution_in_cluster')['rel_error'].mean()
    if solution_mean_errors.empty: # Handle cases like 'Opt' with no explicit cluster/solution IDs
        return best_cluster_df

    best_solution_id = solution_mean_errors.idxmin()
    
    return best_cluster_df[best_cluster_df['solution_in_cluster'] == best_solution_id]


def generate_latex_table(filepath="ifac_analysis_results.csv", output_path="summary_table.tex"):
    """
    Generates a LaTeX table from the analysis results and saves it to a file.
    """
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"Error: The file {filepath} was not found.")
        return

    # Normalize estimator names and handle data types
    df.replace('Inf', np.inf, inplace=True)
    df['rel_error'] = pd.to_numeric(df['rel_error'], errors='coerce')
    df['estimator_name'] = df.apply(
        lambda row: 'GPR' if row['estimator'] == 'PE' and row['interpolator_method'] == 'GPR'
        else ('AAA' if row['estimator'] == 'PE' and row['interpolator_method'] == 'aaad' else 'Opt.'),
        axis=1
    )

    # -- Find the best solution for each group and collect results --
    results = []
    groups = df.groupby(['model_name', 'noise_level', 'estimator_name'])
    
    for (model, noise, est_name), group_df in groups:
        best_solution_df = find_best_solution_for_group(group_df)
        
        if best_solution_df is not None:
            params_df = best_solution_df[best_solution_df['variable_type'] == 'parameter']
            mre = params_df['rel_error'].mean()
            failed = params_df['rel_error'].max() > 1e10
            results.append([model, noise, est_name, mre, failed])

    result_df = pd.DataFrame(results, columns=['model_name', 'noise_level', 'estimator_name', 'mre', 'failed'])

    # Pivot the table
    pivot_df = result_df.pivot_table(
        index='noise_level',
        columns=['model_name', 'estimator_name'],
        values=['mre', 'failed']
    ).sort_index()

    # --- Generate LaTeX string ---
    latex_lines = ["{\\small", "\\begin{tabular}{@{}l@{\\hspace{1pt}}|@{\\hspace{2pt}}c@{\\hspace{4pt}}c@{\\hspace{4pt}}c@{\\hspace{1pt}}|@{\\hspace{2pt}}c@{\\hspace{4pt}}c@{\\hspace{4pt}}c@{}}", "\\toprule"]
    latex_lines.append("& \\multicolumn{3}{c}{\\textbf{Lotka-Volterra}} & \\multicolumn{3}{c}{\\textbf{Van der Pol}} \\\\")
    latex_lines.append("\\cmidrule(lr){2-4} \\cmidrule(lr){5-7}")
    latex_lines.append("\\textbf{Noise} & \\textbf{GPR} & \\textbf{AAA} & \\textbf{Opt.} & \\textbf{GPR} & \\textbf{AAA} & \\textbf{Opt.} \\\\")
    latex_lines.append("\\midrule")

    for noise_level, row in pivot_df.iterrows():
        line = f"{noise_level*100:.1f}\\%"
        for model_name in ['lv_periodic', 'vanderpol']:
            for est_name in ['GPR', 'AAA', 'Opt.']:
                try:
                    mre_val = row[('mre', model_name, est_name)]
                    fail_val = row[('failed', model_name, est_name)]
                    
                    val_str = ""
                    if fail_val or pd.isna(mre_val):
                        val_str = "\\textcolor{errorred}{FAIL}"
                    elif mre_val > 1.0:
                        val_str = f"\\textcolor{{errorred}}{{${'>'}{int(mre_val*100)}\\%$}}"
                    else:
                        cell_val = f"{mre_val*100:.1f}\\%"
                        if est_name == 'GPR':
                            val_str = f"\\textcolor{{successgreen}}{{\\textbf{{{cell_val}}}}}"
                        else:
                            val_str = cell_val
                    line += f" & {val_str}"
                except KeyError:
                    line += " & --"
        line += " \\\\"
        latex_lines.append(line)
        
    latex_lines.append("\\bottomrule")
    latex_lines.append("\\end{tabular}}")
    
    latex_string = "\n".join(latex_lines)

    with open(output_path, 'w') as f:
        f.write(latex_string)
    
    print(f"LaTeX table successfully generated at '{output_path}'")


if __name__ == "__main__":
    generate_latex_table()