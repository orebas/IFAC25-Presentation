# Presentation Outline: Robust Algebraic Parameter Estimation via GPR

## IFAC/COSY/SSSC Joint Conference
**Time allocation: 16-17 minutes presentation + 3-4 minutes Q&A**

---

## Slide 1: Title Slide (30 seconds)
- **Title:** Robust Algebraic Parameter Estimation via Gaussian Process Regression
- **Authors:** Oren Bassik, Alexander Demin, Alexey Ovchinnikov
- **Affiliations:** CUNY Graduate Center, HSE University, CUNY Queens College
- **Acknowledgment:** NSF grants CCF-2212460 and DMS-1853650

---

## Slides 2-3: Introduction & Motivation (2 minutes)
### Key Points:
- Parameter estimation is fundamental in ODE system modeling
- Traditional nonlinear optimization challenges:
  - Requires good initial guesses
  - Gets stuck in local minima
  - Finds only single solution
- Our approach: Differential algebra + Gaussian Process Regression
  - No initial guesses needed
  - Finds all solutions (for locally identifiable parameters)
  - Robust to noise

**[PLACEHOLDER: Add visual comparing optimization vs algebraic approaches]**

---

## Slide 4: Problem Statement (1 minute)
### Mathematical Formulation:
- **Given:**
  - ODE model: x' = f(x(t), u(t), p)
  - Output: y = g(x(t), u(t), p)
  - Initial conditions: x(0) = x₀
  - Measurements: (tᵢ, yᵢ) for i = 1, 2, ..., N
- **Find:** Parameters p and initial conditions x₀

**[PLACEHOLDER: Add clean mathematical notation/diagram]**

---

## Slides 5-7: The Algebraic Method Overview (3 minutes)
### Algorithm Overview:
1. Differentiate the ODE system
2. Approximate derivatives from data
3. Form polynomial equation system
4. Solve the polynomial system
5. Backsolve and filter solutions

### Key Innovation:
- No initial guesses required
- Handles multiple solutions
- Systematic approach

**[PLACEHOLDER: Add flowchart/algorithm diagram]**

---

## Slides 8-11: Toy Example Walkthrough (4 minutes)
### Example System:
- x' = a²x² + b
- y = x² + x
- Find: a, b, x(0)

### Step-by-step demonstration:
1. **Differentiation:**
   - x'' = 2a²xx'
   - y' = 2xx' + x'
   - y'' = 2(x'² + xx'') + x''

2. **Derivative approximation at time tᵢ:**
   - y₀ ≈ y(tᵢ), y₁ ≈ y'(tᵢ), y₂ ≈ y''(tᵢ)

3. **Polynomial system (5 equations, 5 unknowns):**
   - System of polynomial equations in x₀, x₁, x₂, a, b

4. **Solving:**
   - Multiple solutions expected (a vs -a symmetry)

5. **Backsolving/filtering:**
   - Propagate to initial conditions
   - Filter by error

**[PLACEHOLDER: Add animated slides showing each step]**

---

## Slides 12-13: The Key Problem: Noise (2 minutes)
### The Challenge:
- Original method uses AAA baryrational interpolation
- Excellent performance on clean/synthetic data
- Catastrophic failure with even minimal noise (10⁻⁸)
- Interpolation → overfitting → poor derivative estimates

**[PLACEHOLDER: Add graph showing AAA failure with noise]**

---

## Slides 14-15: GPR Solution (2 minutes)
### Gaussian Process Regression:
- Replace interpolation with GPR
- Squared exponential kernel
- Automatic hyperparameter learning:
  - Noise variance
  - Lengthscale
- Smooth mean function → reliable derivatives

### Benefits:
- Handles noisy data naturally
- Self-tuning (retains "hands-off" nature)
- Minimal computational overhead

**[PLACEHOLDER: Add visual comparing AAA vs GPR on noisy data]**

---

## Slides 16-17: Results (2.5 minutes)
### Benchmark Suite:
- Population dynamics: Lotka-Volterra, SEIR
- Biology: Crauste NELM, HIV dynamics, Fitzhugh-Nagumo
- Noise levels: 10⁻⁸ to 10⁻²

### Comparisons:
- AAA interpolation (fails with noise)
- GPR-enhanced method (our approach)
- Traditional optimizers: IQM, SciML, AMIGO2

### Key Finding:
- GPR method significantly outperforms original interpolation
- Comparable to IQM/SciML
- AMIGO2 typically best, but requires more user input

**[PLACEHOLDER: Add results table/graphs showing performance vs noise level]**
**[PLACEHOLDER: Add specific example showing GPR success where AAA fails]**

---

## Slide 18: Discussion & Future Work (1.5 minutes)
### Current Status:
- Bottleneck: polynomial system solving (not GPR)
- GPR adds minimal overhead
- Default method in our software

### Future Directions:
- Uncertainty quantification from GPR
- Optimal timepoint selection
- Confidence intervals on parameter estimates

### Software:
- Open source implementation
- GitHub: https://github.com/orebas/ODEParameterEstimation

---

## Slide 19: Summary (30 seconds)
### Key Takeaways:
- **Problem:** Algebraic parameter estimation fails with noisy data
- **Solution:** Replace interpolation with GPR
- **Result:** Robust parameter estimation without initial guesses
- **Impact:** Makes algebraic approach practical for real-world data

---

## Slide 20: Questions (3-4 minutes)
- Contact: obassik@gradcenter.cuny.edu
- Software: https://github.com/orebas/ODEParameterEstimation
- Thank you!

---

## Preparation Checklist

### Data/Visuals Needed:
1. Comparison diagram: optimization vs algebraic methods
2. Algorithm flowchart (5 steps)
3. Toy example animations/step-by-step visuals
4. AAA failure graph (showing oscillations with noise)
5. AAA vs GPR comparison plots
6. Performance comparison table/graphs
7. One compelling example (e.g., Lotka-Volterra with 1e-4 noise)

### Additional Preparation:
1. Brief demo video (30 seconds) - optional
2. Backup slides with:
   - Technical details on GPR
   - More benchmark results
   - References
3. Practice timing, especially toy example
4. Prepare for likely questions:
   - Computational cost/scalability
   - Limitations (rational functions only)
   - Comparison with other methods
   - Choice of GPR kernel

### Timing Notes:
- Have shorter versions of sections 8-11 and 16-17 if running behind
- Critical sections: Introduction, toy example, GPR solution
- Can abbreviate: Some benchmark details, future work