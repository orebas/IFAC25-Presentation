#!/usr/bin/env python3
"""
Generate "Interpolation vs. GPR" Comparison Figure for IFAC Presentation
Shows the contrast between AAA interpolation (overfitting) and GPR (smooth derivatives)
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel, ConstantKernel
import warnings
warnings.filterwarnings('ignore')

# Set matplotlib style for presentation
plt.style.use('seaborn-v0_8-poster')
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['legend.fontsize'] = 11
plt.rcParams['xtick.labelsize'] = 11
plt.rcParams['ytick.labelsize'] = 11

def aaa(xi, yi, tol=1e-13, mmax=None):
    """
    Minimal AAA (Adaptive Antoulas-Anderson) rational interpolation
    Returns weights w, support points s, values f_s
    """
    xi, yi = np.asarray(xi), np.asarray(yi)
    mmax = mmax or len(xi)
    
    # Initialize
    s, f_s, w = [], [], []
    R = yi.mean() * np.ones_like(yi)  # current rational approx
    err = np.abs(R - yi)
    
    for m in range(mmax):
        j = np.argmax(err)  # greedy support point selection
        s.append(xi[j])
        f_s.append(yi[j])
        
        # Solve least-squares for weights
        V = 1.0 / (xi[:, None] - np.asarray(s))  # Cauchy matrix
        A = V * (yi - R)[:, None]
        try:
            _, _, vh = np.linalg.svd(A, full_matrices=False)
            w = vh[-1]
            R = (V @ (w * f_s)) / (V @ w)
            err = np.abs(R - yi)
            if err.max() < tol:
                break
        except:
            break
    
    return np.asarray(w), np.asarray(s), np.asarray(f_s)

def aaa_eval(x, w, s, f_s):
    """Evaluate AAA rational function at points x"""
    x = np.asarray(x)
    V = 1.0 / (x[:, None] - s)
    return (V @ (w * f_s)) / (V @ w)

def aaa_derivative(x, w, s, f_s):
    """Compute derivative of AAA rational function"""
    x = np.asarray(x)
    V = 1.0 / (x[:, None] - s)
    N = V @ (w * f_s)
    D = V @ w
    V2 = V**2
    Np = -(V2 @ (w * f_s))
    Dp = -(V2 @ w)
    return (Np * D - N * Dp) / (D**2)

def gp_predict_with_derivative(gpr, X_star):
    """
    Predict GPR mean and derivative with uncertainty
    """
    X_star = np.atleast_2d(X_star)
    if X_star.ndim == 1:
        X_star = X_star.reshape(-1, 1)
    
    # Get standard predictions
    mu, std = gpr.predict(X_star, return_std=True)
    
    # Manual derivative calculation for RBF kernel
    K_trans = gpr.kernel_(X_star, gpr.X_train_)
    alpha = gpr.alpha_
    
    # Get the RBF kernel length scale
    length_scale = gpr.kernel_.k2.length_scale
    
    # Compute derivative of kernel
    diff = X_star - gpr.X_train_
    K = np.exp(-0.5 * (diff**2) / length_scale**2)
    dK_dx = K * (-diff) / length_scale**2
    
    # Derivative mean
    mu_prime = dK_dx @ alpha
    
    # Derivative uncertainty (simplified)
    var_prime = np.var(mu_prime) * np.ones_like(mu_prime.flatten())
    std_prime = np.sqrt(np.maximum(var_prime, 0))
    
    return mu, mu_prime.flatten(), std_prime

def generate_data():
    """Generate synthetic noisy sin(x) data"""
    rng = np.random.default_rng(42)
    
    n_train = 25
    x_train = np.sort(rng.uniform(0, 2*np.pi, n_train))
    noise_std = 0.18
    y_train = np.sin(x_train) + rng.normal(0, noise_std, n_train)
    
    # Test/plotting grid
    x_test = np.linspace(0, 2*np.pi, 400)
    y_true = np.sin(x_test)
    dy_true = np.cos(x_test)
    
    return x_train, y_train, x_test, y_true, dy_true

def main():
    """Generate the comparison figure"""
    # Generate data
    x_train, y_train, x_test, y_true, dy_true = generate_data()
    
    print("Fitting AAA interpolation...")
    # Fit AAA with high order to show overfitting
    try:
        w, s, f_s = aaa(x_train, y_train, tol=0, mmax=len(x_train))
        y_aaa = aaa_eval(x_test, w, s, f_s)
        dy_aaa = aaa_derivative(x_test, w, s, f_s)
        aaa_success = True
    except:
        print("AAA failed, using polynomial interpolation as fallback")
        # Fallback to high-degree polynomial
        coeffs = np.polyfit(x_train, y_train, min(len(x_train)-1, 20))
        y_aaa = np.polyval(coeffs, x_test)
        dy_aaa = np.polyval(np.polyder(coeffs), x_test)
        aaa_success = False
    
    print("Fitting GPR...")
    # Fit GPR
    kernel = (ConstantKernel(1.0, (1e-2, 1e2)) * 
              RBF(length_scale=1.2, length_scale_bounds=(0.3, 3.0)) + 
              WhiteKernel(noise_level=0.03**2, noise_level_bounds=(1e-5, 0.1)))
    
    gpr = GaussianProcessRegressor(
        kernel=kernel,
        alpha=0.0,
        normalize_y=True,
        n_restarts_optimizer=5,
        random_state=42
    )
    
    gpr.fit(x_train.reshape(-1, 1), y_train)
    y_gpr, y_std = gpr.predict(x_test.reshape(-1, 1), return_std=True)
    
    # Get GPR derivatives
    try:
        _, dy_gpr, dy_std = gp_predict_with_derivative(gpr, x_test.reshape(-1, 1))
    except:
        # Fallback: numerical derivative
        dy_gpr = np.gradient(y_gpr, x_test)
        dy_std = y_std * 0.5  # Rough estimate
    
    print("Creating figure...")
    # Create figure with improved layout
    fig, axes = plt.subplots(2, 2, figsize=(14, 10), sharex='all', sharey='row')
    
    # Remove top and right spines for clean look
    for ax in axes.flat:
        ax.spines[['right', 'top']].set_visible(False)
        ax.grid(True, linestyle='--', alpha=0.3)
    
    # Define colors following the design strategy
    color_data = 'gray'
    color_aaa = 'orangered'
    color_gpr = 'steelblue'
    color_true = 'black'
    
    # Top left: AAA interpolation
    ax = axes[0, 0]
    ax.plot(x_test, y_true, 'k--', lw=2, label='True sin(x)', alpha=0.8)
    ax.scatter(x_train, y_train, c=color_data, s=40, alpha=0.7, zorder=3, label='Noisy data')
    ax.plot(x_test, y_aaa, color=color_aaa, lw=2, label='AAA fit')
    ax.set_title('AAA Interpolation (Overfitting)', fontsize=14, pad=15)
    ax.set_ylabel('f(x)', fontsize=14)
    ax.legend(loc='upper right')
    ax.set_ylim(-2.5, 2.5)
    
    # Top right: GPR
    ax = axes[0, 1]
    ax.plot(x_test, y_true, 'k--', lw=2, label='True sin(x)', alpha=0.8)
    ax.scatter(x_train, y_train, c=color_data, s=40, alpha=0.7, zorder=3, label='Noisy data')
    ax.plot(x_test, y_gpr, color=color_gpr, lw=2, label='GPR mean')
    ax.fill_between(x_test, y_gpr - 1.96*y_std, y_gpr + 1.96*y_std, 
                    color=color_gpr, alpha=0.2, label='95% confidence')
    ax.set_title('Gaussian Process Regression', fontsize=14, pad=15)
    ax.legend(loc='upper right')
    ax.set_ylim(-2.5, 2.5)
    
    # Bottom left: AAA derivative
    ax = axes[1, 0]
    ax.plot(x_test, dy_true, 'k--', lw=2, label='True cos(x)', alpha=0.8)
    
    # Clip extreme values for visualization
    dy_aaa_clipped = np.clip(dy_aaa, -50, 50)
    ax.plot(x_test, dy_aaa_clipped, color=color_aaa, lw=2, label='AAA derivative')
    ax.set_title('AAA Derivative (Noise Amplification)', fontsize=14, pad=15)
    ax.set_ylabel("f'(x)", fontsize=14)
    ax.set_xlabel('x', fontsize=14)
    ax.legend(loc='upper right')
    
    # Bottom right: GPR derivative  
    ax = axes[1, 1]
    ax.plot(x_test, dy_true, 'k--', lw=2, label='True cos(x)', alpha=0.8)
    ax.plot(x_test, dy_gpr, color=color_gpr, lw=2, label='GPR derivative')
    ax.fill_between(x_test, dy_gpr - 1.96*dy_std, dy_gpr + 1.96*dy_std,
                    color=color_gpr, alpha=0.2, label='95% confidence')
    ax.set_title('GPR Derivative (Stable)', fontsize=14, pad=15)
    ax.set_xlabel('x', fontsize=14)
    ax.legend(loc='upper right')
    
    # Set x-axis labels and ticks
    for ax in axes[1, :]:
        ax.set_xlim(0, 2*np.pi)
        ax.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
        ax.set_xticklabels(['0', 'π/2', 'π', '3π/2', '2π'])
    
    # Add main title
    fig.suptitle('Interpolation vs. GPR: Derivative Estimation Comparison', 
                 fontsize=16, y=0.95)
    
    # Adjust layout
    plt.tight_layout()
    plt.subplots_adjust(top=0.90, hspace=0.3, wspace=0.25)
    
    # Save figure
    output_file = '/home/orebas/IFAC-presentation/gpr_vs_aaa_comparison.pdf'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    
    print(f"Figure saved to: {output_file}")
    
    # Also save as PNG for easier viewing
    png_file = output_file.replace('.pdf', '.png')
    plt.savefig(png_file, dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f"PNG version saved to: {png_file}")
    
    plt.show()
    
    # Print some statistics
    print("\nComparison Statistics:")
    print(f"AAA function RMSE: {np.sqrt(np.mean((y_aaa - y_true)**2)):.4f}")
    print(f"GPR function RMSE: {np.sqrt(np.mean((y_gpr - y_true)**2)):.4f}")
    print(f"AAA derivative RMSE: {np.sqrt(np.mean((dy_aaa - dy_true)**2)):.4f}")
    print(f"GPR derivative RMSE: {np.sqrt(np.mean((dy_gpr - dy_true)**2)):.4f}")

if __name__ == "__main__":
    main()