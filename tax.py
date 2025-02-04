import numpy as np
import matplotlib.pyplot as plt

# -------------------------------
# Tax functions
# -------------------------------

def old_tax(income):
    """
    Old Tax Regime for salaried individuals.
    Standard Deduction: ₹50,000.
    Slabs:
      - Up to ₹2.5 lakh: 0%
      - ₹2.5 lakh to ₹5 lakh: 5%
      - ₹5 lakh to ₹10 lakh: 20%
      - Above ₹10 lakh: 30%
    """
    taxable = max(income - 50000, 0)
    if taxable <= 250000:
        tax = 0
    elif taxable <= 500000:
        tax = (taxable - 250000) * 0.05
    elif taxable <= 1000000:
        tax = (250000 * 0.05) + (taxable - 500000) * 0.20
    else:
        tax = (250000 * 0.05) + (500000 * 0.20) + (taxable - 1000000) * 0.30
    return tax

def new_tax(income):
    """
    New Tax Regime for salaried individuals as per Union Budget 2025-26.
    
    - Standard Deduction: ₹75,000.
    - Effective tax-free if taxable income (income - 75,000) <= ₹12,00,000.
      (Thus, for incomes up to ₹12.75 lakh, no tax is payable.)
    - Revised slabs (on taxable income):
         0 – ₹4,00,000: Nil
         ₹4,00,001 – ₹8,00,000: 5%
         ₹8,00,001 – ₹12,00,000: 10%
         ₹12,00,001 – ₹16,00,000: 15%
         ₹16,00,001 – ₹20,00,000: 20%
         ₹20,00,001 – ₹24,00,000: 25%
         Above ₹24,00,000: 30%
    - For taxable income up to ₹12,00,000 the Section 87A rebate of ₹60,000 ensures zero net tax.
    """
    taxable = income - 75000  # Apply standard deduction
    # If taxable income is ≤12,00,000, the rebate makes the net tax zero.
    if taxable <= 1200000:
        return 0

    tax = 0
    if taxable <= 400000:
        tax = 0
    elif taxable <= 800000:
        tax = (taxable - 400000) * 0.05
    elif taxable <= 1200000:
        tax = (400000 * 0.05) + (taxable - 800000) * 0.10
    elif taxable <= 1600000:
        tax = (400000 * 0.05) + (400000 * 0.10) + (taxable - 1200000) * 0.15
    elif taxable <= 2000000:
        tax = (400000 * 0.05) + (400000 * 0.10) + (400000 * 0.15) + (taxable - 1600000) * 0.20
    elif taxable <= 2400000:
        tax = (400000 * 0.05) + (400000 * 0.10) + (400000 * 0.15) + (400000 * 0.20) + (taxable - 2000000) * 0.25
    else:
        tax = (400000 * 0.05) + (400000 * 0.10) + (400000 * 0.15) + (400000 * 0.20) + (400000 * 0.25) + (taxable - 2400000) * 0.30

    return tax

# -------------------------------
# Simulation parameters
# -------------------------------

# Total number of taxpayers assumed: 8 crores = 80,000,000.
total_taxpayers = 80_000_000

# For simulation we generate a sample of incomes.
# We assume incomes (annual) follow a lognormal distribution.
# Choose parameters so that the median income is around, say, ₹8,00,000.
# For a lognormal distribution, median = exp(mu).
# Hence, set mu = ln(800000) and choose sigma = 0.8 (for some dispersion).
mu = np.log(800000)
sigma = 0.8
sample_size = 10**6  # simulate one million taxpayers (sample)
np.random.seed(42)  # for reproducibility

# Generate incomes in rupees:
incomes_sample = np.random.lognormal(mean=mu, sigma=sigma, size=sample_size)
# It might be sensible to clip extreme values to a reasonable upper bound:
incomes_sample = np.clip(incomes_sample, 300000, 5000000)  # between ₹3 lakh and ₹50 lakh

# -------------------------------
# Compute tax liabilities and savings for each sample taxpayer
# -------------------------------

old_taxes = np.array([old_tax(inc) for inc in incomes_sample])
new_taxes = np.array([new_tax(inc) for inc in incomes_sample])
tax_savings = old_taxes - new_taxes  # extra money that is not paid as tax under new regime

# Average tax saving per taxpayer in the sample:
avg_saving_sample = np.mean(tax_savings)
print(f"Average tax saving per taxpayer in the simulation: ₹{avg_saving_sample:,.2f}")

# Estimated total discretionary income increase (aggregate tax saving)
total_savings = avg_saving_sample * total_taxpayers
print(f"Total discretionary income increase for {total_taxpayers:,} taxpayers: ₹{total_savings:,.2f}")

# -------------------------------
# Optional: Plot histogram of tax savings
# -------------------------------
plt.figure(figsize=(10, 6))
plt.hist(tax_savings, bins=50, color='green', alpha=0.7)
plt.xlabel("Tax Savings per Taxpayer (₹)")
plt.ylabel("Number of Taxpayers (sample frequency)")
plt.title("Histogram of Tax Savings per Taxpayer under New Regime vs Old Regime")
plt.grid(True)
plt.tight_layout()
plt.show()

