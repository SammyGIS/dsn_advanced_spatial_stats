import json

nb_path = 'notebooks/02_spatial_statistics_modeling.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

vif_markdown = r"""## 3. Pre-Modeling Diagnostics: Multicollinearity & Variance Inflation Factor (VIF)

### 3.1 What Is Multicollinearity & Why Does It Break Models?
Multicollinearity occurs when two or more explanatory covariates ($X_1, X_2, \dots, X_p$) in a regression model are highly correlated with each other. While multicollinearity does not violate the OLS Gauss-Markov assumption of unbiasedness (coefficients remain theoretically centered around their true population values), it introduces **devastating practical consequences**:
1. **Variance Inflation:** The variance of the estimated coefficients $\text{Var}(\hat{\beta}_k)$ explodes toward infinity as collinearity increases.
2. **Standard Error Blowup:** Wide standard errors produce artificially small $t$-statistics and inflated $p$-values, leading researchers to conclude that key policy interventions have "no significant effect" (**Type-II Error**).
3. **Coefficient Instability & Sign Reversals:** Minor perturbations or adding/removing a single variable can cause estimated coefficients to swing erratically or flip to counter-intuitive signs (e.g., healthcare clinics appearing to "increase" poverty).

---

### 3.2 The Mathematical Mechanics of VIF
To measure the exact degree to which collinearity inflates the variance of coefficient $\hat{\beta}_k$, we compute the **Variance Inflation Factor ($\text{VIF}_k$)**:

$$
\text{VIF}_k = \frac{1}{1 - R_k^2}
$$

**Step-by-Step Mathematical Derivation:**
1. **Auxiliary Regression:** We take predictor $X_k$ and run an ordinary regression using $X_k$ as the dependent variable against all other remaining $p-1$ predictors in the matrix:
   $$X_k = \alpha_0 + \sum_{j \neq k} \alpha_j X_j + u_k$$
2. **Coefficient of Determination ($R_k^2$):** We extract $R_k^2$, which represents the proportion of variance in $X_k$ that is completely explained by the other predictors.
3. **Variance Inversion:** The variance of $\hat{\beta}_k$ in the full regression is given by:
   $$\text{Var}(\hat{\beta}_k) = \frac{\sigma^2}{(n-1) s_k^2} \cdot \left(\frac{1}{1 - R_k^2}\right) = \text{Var}_{\text{orthogonal}}(\hat{\beta}_k) \cdot \text{VIF}_k$$
   where $s_k^2$ is the sample variance of $X_k$.

**Intuitive Walkthrough:**
- If $X_k$ is completely orthogonal to all other predictors: $R_k^2 = 0 \implies \text{VIF}_k = \frac{1}{1 - 0} = 1.0$ (Zero variance inflation).
- If other predictors explain 80% of $X_k$: $R_k^2 = 0.80 \implies \text{VIF}_k = \frac{1}{1 - 0.80} = 5.0$ (Variance is inflated $5\times$).
- If other predictors explain 90% of $X_k$: $R_k^2 = 0.90 \implies \text{VIF}_k = \frac{1}{1 - 0.90} = 10.0$ (Variance is inflated $10\times$, standard error is inflated $\sqrt{10} \approx 3.16\times$).

---

### 3.3 Interpretation Benchmark Thresholds

| VIF Range | Collinearity Level | Practical Meaning & Prescribed Action |
| :---: | :---: | :--- |
| **VIF = 1.0** | **Ideal (Orthogonal)** | Predictor shares zero linear overlap with other features. Maximum parameter precision. |
| **1.0 < VIF < 5.0** | **Low / Safe** | Mild correlation that does not compromise parameter stability. **Safe to proceed with OLS and Spatial Econometrics.** |
| **5.0 ≤ VIF < 10.0** | **Moderate Concern** | Noticeable coefficient inflation. Coefficients should be scrutinized and standard errors verified. |
| **VIF ≥ 10.0** | **Severe Multicollinearity** | Critical violation: feature matrix is near-singular. Variables must be dropped, combined via dimensionality reduction, or regularized. |

---

### 3.4 Why VIF Is Mandatory BEFORE Spatial Econometrics (SAR & SEM)
In Spatial Autoregressive models (SAR: $y = \rho Wy + X\beta + \epsilon$), the spatial lag $\rho Wy$ acts as an endogenous regressor. If the exogenous feature matrix $X$ is already contaminated with high multicollinearity, the Maximum Likelihood or Instrumental Variables estimator cannot reliably separate exogenous predictor effects ($X\beta$) from endogenous spatial contagion ($\rho Wy$). Verifying low VIF ($\text{VIF} < 5$) establishes the essential empirical foundation before spatial diagnostics.
"""

for cell in nb['cells']:
    if cell['cell_type'] == 'markdown':
        src = "".join(cell.get('source', []))
        if '3. Pre-Modeling Diagnostics' in src or 'extVIF' in src or '3.3 Interpretation Benchmark' in src:
            cell['source'] = [line + '\n' for line in vif_markdown.splitlines()]
            print("Successfully updated VIF markdown in notebook 02!")

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
