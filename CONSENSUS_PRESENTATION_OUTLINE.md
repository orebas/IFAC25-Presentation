# SCIENTIFIC PRESENTATION OUTLINE
## Robust Algebraic Parameter Estimation via Gaussian Process Regression

**Target Time:** 16-17 minutes presentation + 3-4 minutes Q&A  
**Audience:** IFAC/COSY/SSSC Joint Conference (Control Systems Experts)  
**Approach:** Data-driven technical presentation with objective analysis

---

## PRESENTATION STRUCTURE (8 Slides)

### **Slide 1: Title (0:30)**
**Title:** Robust Algebraic Parameter Estimation via Gaussian Process Regression  
**Authors:** Oren Bassik, Alexander Demin, Alexey Ovchinnikov  
**Affiliations:** CUNY Graduate Center, HSE University, CUNY Queens College  
**Acknowledgments:** NSF grants CCF-2212460 and DMS-1853650

### **Slide 2: The Core Challenge, Visualized (2:00)**
**The Algebraic Method: Promise and Peril**

**Visual:** Side-by-side comparison plots using identical noisy data:
- **Left Plot:** "Naive Differentiation via Interpolation"
  - AAA interpolant oscillating wildly through noise points
  - Resulting derivative: unusable noise amplification
- **Right Plot:** "Principled Differentiation via GPR" 
  - Smooth GPR mean function with confidence bands
  - Resulting derivative: stable, physically plausible

**Key Message:** Differential algebra offers guess-free parameter estimation, but it struggles with the requirement to differentiate noisy data. The central challenge: systematic transition from left plot to right plot.

### **Slide 3: Quantitative Validation of Method Robustness (2:30)**
**Systematic Evaluation Reveals Critical Failure Modes**

**Visual Evidence:** Two-panel comparative analysis
- **Left Panel - "The Noise Cliff":** RMSE vs Noise Level (0 to 10⁻³)
  - GPR_Julia: stable performance across all noise levels
  - AAA methods: catastrophic failure at >10⁻⁸ noise (10¹⁰-fold error increase)
  - Demonstrates fundamental brittleness vs robustness

- **Right Panel - "The Derivative Wall":** RMSE vs Derivative Order (1 to 6)
  - GPR_Julia: graceful degradation through high orders
  - TVDiff_Julia: complete failure at order 4+ (no results)
  - Finite differences: exponential error growth

**Key Finding:** Across 21 methods tested using **Automatic Differentiation** framework, only GPR with RBF kernel avoids both failure modes

### **Slide 4: Why Gaussian Process Regression Succeeds (2:30)**
**Bayesian Framework for Function Estimation:**
- Treats differentiation as statistical inference problem, not curve fitting
- Prior assumption: underlying function is smooth (RBF kernel enforces this)
- Posterior distribution provides derivatives in closed form with uncertainty quantification

**Key Technical Advantages:**
- **Automatic hyperparameter learning**: Noise variance σ² and lengthscale ℓ optimized via marginal likelihood
- **Global smoothing**: All data points inform each derivative estimate with appropriate noise weighting  
- **Numerical stability**: No finite difference subtraction, well-conditioned kernel matrix operations
- **Adaptive bandwidth**: Method automatically adjusts smoothing based on local signal characteristics

**Result:** Stable, reliable derivatives across all orders required for algebraic parameter estimation

### **Slide 5: Application: Making the Algebraic Method Viable (3:00)**
**Benchmark:** Compare GPR-Algebraic vs. Original (AAA) vs. Standard Optimization (SciML).
**Key Result:** GPR makes the algebraic method robust to noise, achieving performance that is competitive with (though not always superior to) traditional methods.
**Contribution:** The core algebraic advantages (no initial guesses, finds all solutions) are preserved, making it a viable, automated alternative to local optimization.

### **Slide 6: Conclusions (2:30)**
**Summary of Contributions:**
- Solved critical bottleneck in differential algebraic parameter estimation through systematic method selection
- Demonstrated GPR as uniquely suited for high-order derivative estimation from noisy data
- Enabled systematic evaluation via **Automatic Differentiation** framework (Julia ForwardDiff, Python JAX)
- Method retains key algebraic advantages: no initial guesses, multiple solutions, automation

**Performance:**
- Robust parameter recovery up to 10⁻² noise levels vs AAA failure at 10⁻⁸
- Minimal computational overhead (<20%), polynomial solving remains bottleneck

**Future Work:**
- Uncertainty quantification using GPR variance estimates
- Optimal experimental design for parameter estimation
- Extension to larger parameter spaces

**Software:** Available at github.com/orebas/ODEParameterEstimation

---

## BACKUP/APPENDIX SLIDES (If Q&A Extends or Technical Questions Arise)

### **A1: Computational Performance Analysis**
- Detailed timing benchmarks: GPR (2.15s) vs SavitzkyGolay (0.0015s) vs TVDiff (0.19s)
- Runtime breakdown: 70% polynomial solving, 20% GPR, 10% miscellaneous
- Scaling considerations for large datasets (O(N³) vs O(N) methods)
- Justification for accuracy-first approach over speed optimization

### **A2: Extended Benchmark Results**
- Complete performance matrix across 21 methods, 3 noise levels, 6 derivative orders
- Method failure mode analysis: "noise cliffs" and "derivative walls"
- Statistical significance analysis and confidence intervals
- Edge cases and boundary conditions

### **A3: GPR Implementation and Methodology Details**
- Hyperparameter optimization via marginal likelihood maximization
- RBF kernel choice rationale vs Matern alternatives
- Automatic differentiation framework enabling fair comparison
- Integration points with existing algebraic parameter estimation software

---

## PRESENTATION GUIDELINES

### **Visual Strategy:**
- Clean, professional slide design
- Focus on data visualization over text
- Before/after comparison plots for key results
- Minimal animations, maximum clarity

### **Data Presentation:**
- Quantitative results with error bars
- Log-scale plots for noise level comparisons
- Clear performance metrics and statistical significance
- Objective language in all descriptions

### **Technical Depth:**
- Appropriate mathematical notation
- Reference to established methods
- Clear problem formulation
- Rigorous experimental design

---

## RECOMMENDED VISUALIZATIONS TO DEVELOP

1. **Early Impact Visual (Slide 2):** Side-by-side dramatic comparison of AAA overfitting vs GPR smoothing on identical noisy data, including derivative plots

2. **Noise Cliff Demonstration (Slide 3, Left Panel):** 
   - Log(RMSE) vs Noise Level (0 to 10⁻³) 
   - Show GPR_Julia (stable), AAA methods (cliff at 10⁻⁸), SVR (flat mediocre)
   - Highlight 10¹⁰-fold error increase for AAA at minimal noise

3. **Derivative Wall Analysis (Slide 3, Right Panel):**
   - RMSE vs Derivative Order (1 to 6)
   - Show GPR_Julia (graceful degradation), TVDiff_Julia (wall at order 4), finite differences (exponential growth)
   - Use actual benchmark data: GPR stable through order 6, TVDiff no results beyond order 3

4. **Application Performance Table (Slide 5):**
   - Clean comparison showing Mean Relative Error for realistic systems
   - GPR Method vs Original (AAA) vs Status across Fitzhugh-Nagumo, Lotka-Volterra, SEIR
   - Use actual benchmark results where available

5. **Computational Context (Backup):**
   - GPR timing: 2.15s average vs alternatives
   - Runtime breakdown: 70% polynomial solving, 20% GPR, 10% misc
   - Demonstrate GPR is not the bottleneck

This scientific presentation outline focuses on objective analysis, data-driven conclusions, and technical rigor appropriate for the IFAC audience.
