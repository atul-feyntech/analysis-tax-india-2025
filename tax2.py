import numpy as np
import matplotlib.pyplot as plt

# -------------------------------
# Tax functions (in rupees)
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
    New Tax Regime for salaried individuals (Union Budget 2025–26).
    Standard Deduction: ₹75,000.
    Tax exemption: For taxable income (income - 75,000) ≤ ₹12,00,000,
      Section 87A rebate of ₹60,000 ensures net tax is zero.
    Revised slabs (on taxable income):
         0 – ₹4,00,000: Nil
         ₹4,00,001–₹8,00,000: 5%
         ₹8,00,001–₹12,00,000: 10%
         ₹12,00,001–₹16,00,000: 15%
         ₹16,00,001–₹20,00,000: 20%
         ₹20,00,001–₹24,00,000: 25%
         Above ₹24,00,000: 30%
    """
    taxable = income - 75000  # apply standard deduction of ₹75,000
    if taxable <= 1200000:
        # With Section 87A rebate of ₹60,000, net tax is zero
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
        tax = (400000 * 0.05) + (400000 * 0.10) + (400000 * 0.15) + (taxable - 1200000 - 400000) * 0.20
    elif taxable <= 2400000:
        tax = (400000 * 0.05) + (400000 * 0.10) + (400000 * 0.15) + (400000 * 0.20) + (taxable - 2000000) * 0.25
    else:
        tax = (400000 * 0.05) + (400000 * 0.10) + (400000 * 0.15) + (400000 * 0.20) + (400000 * 0.25) + (taxable - 2400000) * 0.30

    return tax

# -------------------------------
# Inflation and Taxpayer Growth Parameters
# -------------------------------

inflation_rate = 0.0522  # Overall inflation rate (5.22%)

# Taxpayer numbers by assessment year (in absolute numbers):
taxpayer_counts = {
    "AY 2021-22": 45_000_000,  # 4.5 crore
    "AY 2022-23": 63_000_000,  # 6.3 crore
    "AY 2023-24": 67_700_000,  # 6.77 crore
    "AY 2024-25": 72_800_000   # 7.28 crore
}

# -------------------------------
# Taxpayer Distribution for AY 2024-25 by Income Slab
# -------------------------------
# Distribution (as fractions) and representative incomes (in rupees)
# Note: The representative income is an approximate mid–value for each bracket.
taxpayer_distribution = {
    "Up to ₹3 lakh": {"percentage": 0.50, "rep_income": 200000},
    "₹3–7 lakh": {"percentage": 0.30, "rep_income": 500000},
    "₹7–10 lakh": {"percentage": 0.10, "rep_income": 850000},
    "₹10–12 lakh": {"percentage": 0.05, "rep_income": 1100000},
    "₹12–15 lakh": {"percentage": 0.03, "rep_income": 1350000},
    "Above ₹15 lakh": {"percentage": 0.02, "rep_income": 2500000}
}

total_taxpayers_AY2425 = taxpayer_counts["AY 2024-25"]

# Compute per-slab tax savings for AY 2024-25
slab_names = []
savings_per_taxpayer = []
num_taxpayers_slab = []
aggregate_savings_slab = []

for slab, info in taxpayer_distribution.items():
    rep_income = info["rep_income"]
    percent = info["percentage"]
    saving = old_tax(rep_income) - new_tax(rep_income)
    count = total_taxpayers_AY2425 * percent
    slab_names.append(slab)
    savings_per_taxpayer.append(saving)
    num_taxpayers_slab.append(count)
    aggregate_savings_slab.append(saving * count)

# Calculate overall average saving per taxpayer (weighted)
total_aggregate_savings_AY2425 = sum(aggregate_savings_slab)
avg_saving_AY2425 = total_aggregate_savings_AY2425 / total_taxpayers_AY2425

# Also compute "real" (inflation-adjusted) savings:
real_total_savings = total_aggregate_savings_AY2425 / (1 + inflation_rate)

print(f"AY 2024-25: Average tax saving per taxpayer: ₹{avg_saving_AY2425:,.2f}")
print(f"AY 2024-25: Total discretionary income increase (nominal): ₹{total_aggregate_savings_AY2425:,.2f}")
print(f"AY 2024-25: Total discretionary income increase (real): ₹{real_total_savings:,.2f}")

# -------------------------------
# Plot 1: Tax Savings by Income Slab for AY 2024-25
# -------------------------------
plt.figure(figsize=(10, 6))
bar_positions = np.arange(len(slab_names))
plt.bar(bar_positions, savings_per_taxpayer, color='blue', alpha=0.7)
plt.xticks(bar_positions, slab_names, rotation=45)
plt.xlabel("Income Tax Slab")
plt.ylabel("Tax Savings per Taxpayer (₹)")
plt.title("Tax Savings per Taxpayer by Income Slab (AY 2024-25)")
plt.grid(axis='y', alpha=0.5)
plt.tight_layout()
plt.show()

# -------------------------------
# Plot 2: Aggregate Tax Savings over Assessment Years
# -------------------------------
# Assume that the average saving per taxpayer computed for AY 2024-25 applies for earlier years as a baseline.
# (In practice, the distribution and saving may vary; here we simplify.)
years = list(taxpayer_counts.keys())
taxpayer_numbers = [taxpayer_counts[year] for year in years]
aggregate_savings_yearly = [avg_saving_AY2425 * n for n in taxpayer_numbers]
real_aggregate_savings_yearly = [s / (1 + inflation_rate) for s in aggregate_savings_yearly]

plt.figure(figsize=(10, 6))
plt.plot(years, np.array(aggregate_savings_yearly)/1e12, marker='o', label="Nominal Savings (₹ Trillion)")
plt.plot(years, np.array(real_aggregate_savings_yearly)/1e12, marker='s', label="Real Savings (₹ Trillion)")
plt.xlabel("Assessment Year")
plt.ylabel("Aggregate Tax Savings (Trillion ₹)")
plt.title("Aggregate Discretionary Income Increase over Assessment Years")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

