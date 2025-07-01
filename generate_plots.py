#!/usr/bin/env python3
"""
Generate plots for IFAC presentation from CSV data
Creates the "Noise Cliff" and "Derivative Wall" visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set up matplotlib for publication-quality plots
plt.rcParams.update({
    'font.size': 11,
    'font.family': 'serif',
    'axes.linewidth': 1.0,
    'grid.alpha': 0.3,
    'legend.framealpha': 0.9,
    'figure.dpi': 300
})

def load_and_prepare_data():
    """Load and prepare the CSV data for plotting"""
    # Load the long-format data
    df = pd.read_csv('pivot_rmse_by_method_noise_deriv.csv')
    
    # Handle infinite values (failed convergence)
    df['rmse'] = df['rmse'].replace([np.inf, -np.inf], np.nan)
    
    # Log transform for visualization
    df['log_rmse'] = np.log10(df['rmse'])
    df['log_noise'] = np.log10(df['noise_level'].replace(0.0, 1e-16))  # Handle zero noise
    
    return df

def create_noise_cliff_plot(df, methods_to_plot=['GPR_Julia', 'AAA_Julia'], save_path='noise_cliff.pdf'):
    """Create the Noise Cliff plot (RMSE vs Noise Level)"""
    
    fig, ax = plt.subplots(figsize=(6, 4.5))
    
    # Filter data for specific derivative orders (e.g., 1st derivative)
    plot_data = df[df['derivative_order'] == 1]
    
    # Color scheme
    colors = {'GPR_Julia': '#2E7D32', 'AAA_Julia': '#D32F2F'}  # Green for good, Red for bad
    
    for method in methods_to_plot:
        if method in plot_data['method'].values:
            method_data = plot_data[plot_data['method'] == method].copy()
            
            # Remove NaN values for plotting
            method_data = method_data.dropna(subset=['log_rmse', 'log_noise'])
            
            if len(method_data) > 0:
                ax.plot(method_data['log_noise'], method_data['log_rmse'], 
                       'o-', label=method.replace('_', ' '), 
                       color=colors.get(method, 'black'), linewidth=2, markersize=6)
    
    # Add critical failure threshold line
    ax.axvline(x=np.log10(1e-8), color='red', linestyle='--', alpha=0.7, 
               label='Critical Threshold')
    
    # Formatting
    ax.set_xlabel('Log₁₀(Noise Level)', fontsize=12)
    ax.set_ylabel('Log₁₀(RMSE)', fontsize=12)
    ax.set_title('The "Noise Cliff"\nRMSE vs. Noise Level (1st Derivative)', fontsize=13, pad=20)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
    
    # Set reasonable axis limits
    ax.set_xlim(-16, -2)
    
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close()
    
    print(f"Noise cliff plot saved to {save_path}")

def create_derivative_wall_plot(df, methods_to_plot=['GPR_Julia', 'TVDiff_Julia'], 
                               noise_level=1e-6, save_path='derivative_wall.pdf'):
    """Create the Derivative Wall plot (RMSE vs Derivative Order)"""
    
    fig, ax = plt.subplots(figsize=(6, 4.5))
    
    # Filter data for specific noise level
    plot_data = df[df['noise_level'] == noise_level]
    
    # Color scheme
    colors = {'GPR_Julia': '#2E7D32', 'TVDiff_Julia': '#FF6F00'}  # Green for good, Orange for problematic
    markers = {'GPR_Julia': 'o', 'TVDiff_Julia': 's'}
    
    for method in methods_to_plot:
        if method in plot_data['method'].values:
            method_data = plot_data[plot_data['method'] == method].copy()
            
            # Separate convergent and non-convergent points
            convergent = method_data.dropna(subset=['log_rmse'])
            non_convergent = method_data[method_data['rmse'].isna()]
            
            if len(convergent) > 0:
                ax.plot(convergent['derivative_order'], convergent['log_rmse'], 
                       'o-', label=method.replace('_', ' '), 
                       color=colors.get(method, 'black'), linewidth=2, markersize=6,
                       marker=markers.get(method, 'o'))
            
            # Mark non-convergent points
            if len(non_convergent) > 0:
                ax.scatter(non_convergent['derivative_order'], 
                          [12] * len(non_convergent),  # Sentinel value for display
                          marker='x', s=100, color=colors.get(method, 'black'),
                          label=f'{method.replace("_", " ")} (Failed)')
    
    # Add derivative wall line
    ax.axvline(x=4, color='orange', linestyle='--', alpha=0.7, 
               label='Derivative Wall')
    
    # Formatting
    ax.set_xlabel('Derivative Order', fontsize=12)
    ax.set_ylabel('Log₁₀(RMSE)', fontsize=12)
    ax.set_title(f'The "Derivative Wall"\nRMSE vs. Derivative Order (σ = {noise_level})', 
                fontsize=13, pad=20)
    ax.set_xticks(range(0, 7))
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
    
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close()
    
    print(f"Derivative wall plot saved to {save_path}")

def create_comparison_heatmap(df, save_path='method_comparison_heatmap.pdf'):
    """Create a comprehensive heatmap showing all methods"""
    
    # Pivot the data for heatmap
    pivot_data = df.pivot_table(values='log_rmse', 
                               index=['method'], 
                               columns=['noise_level', 'derivative_order'], 
                               aggfunc='mean')
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create heatmap
    sns.heatmap(pivot_data, annot=False, cmap='RdYlGn_r', center=0, 
                ax=ax, cbar_kws={'label': 'Log₁₀(RMSE)'})
    
    ax.set_title('Comprehensive Method Comparison\nLog₁₀(RMSE) across Noise Levels and Derivative Orders', 
                fontsize=14, pad=20)
    ax.set_xlabel('(Noise Level, Derivative Order)', fontsize=12)
    ax.set_ylabel('Method', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close()
    
    print(f"Comparison heatmap saved to {save_path}")

def main():
    """Main function to generate all plots"""
    print("Loading data...")
    df = load_and_prepare_data()
    
    print(f"Data shape: {df.shape}")
    print(f"Methods available: {sorted(df['method'].unique())}")
    print(f"Noise levels: {sorted(df['noise_level'].unique())}")
    print(f"Derivative orders: {sorted(df['derivative_order'].unique())}")
    
    # Create the main plots for the presentation
    print("\nGenerating plots...")
    
    # Noise cliff plot
    create_noise_cliff_plot(df)
    
    # Derivative wall plot  
    create_derivative_wall_plot(df)
    
    # Comprehensive heatmap for backup slides
    create_comparison_heatmap(df)
    
    print("\nAll plots generated successfully!")
    print("Files created:")
    print("- noise_cliff.pdf")
    print("- derivative_wall.pdf") 
    print("- method_comparison_heatmap.pdf")

if __name__ == "__main__":
    main()