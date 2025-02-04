import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 1. TAX FUNCTIONS
# ============================================================
def old_tax(income):
    """
    Computes tax liability under the old tax regime.
    Assumptions:
      - Standard Deduction: ₹50,000.
      - Tax Slabs:
          • Up to ₹2.5 lakh: Nil
          • ₹2.5 lakh to ₹5 lakh: 5%
          • ₹5 lakh to ₹10 lakh: 20%
          • Above ₹10 lakh: 30%
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
    Computes tax liability under the new tax regime as per Union Budget 2025–26.
    Assumptions for salaried individuals:
      - Standard Deduction: ₹75,000.
      - Tax exemption threshold: Gross income up to ₹12.75 lakh (so that taxable income <= ₹12 lakh)
        is effectively tax free due to the Section 87A rebate (rebate increased from ₹25,000 to ₹60,000).
      - Revised Tax Slabs (on taxable income = income - 75,000):
          • 0 – ₹4,00,000: Nil
          • ₹4,00,001–₹8,00,000: 5%
          • ₹8,00,001–₹12,00,000: 10%
          • ₹12,00,001–₹16,00,000: 15%
          • ₹16,00,001–₹20,00,000: 20%
          • ₹20,00,001–₹24,00,000: 25%
          • Above ₹24,00,000: 30%
    """
    taxable = income - 75000  # Apply standard deduction
    # If taxable income is less than or equal to ₹12,00,000,
    # the Section 87A rebate (₹60,000) ensures net tax is zero.
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

# ============================================================
# 2. PARAMETER SETUP
# ============================================================
# Inflation rate (December 2024)
inflation_rate = 0.0522  # 5.22%

# Taxpayer counts by assessment year (in absolute numbers)
taxpayer_counts = {
    "AY 2021-22": 45_000_000,  # 4.5 crore
    "AY 2022-23": 63_000_000,  # 6.3 crore
    "AY 2023-24": 67_700_000,  # 6.77 crore
    "AY 2024-25": 72_800_000   # 7.28 crore
}

# For AY 2024-25, estimated distribution of taxpayers by income slab.
# Percentages (fractions) and representative incomes (in rupees):
taxpayer_distribution = {
    "Up to ₹3 lakh": {"percentage": 0.50, "rep_income": 200000},
    "₹3–7 lakh": {"percentage": 0.30, "rep_income": 500000},
    "₹7–10 lakh": {"percentage": 0.10, "rep_income": 850000},
    "₹10–12 lakh": {"percentage": 0.05, "rep_income": 1100000},
    "₹12–15 lakh": {"percentage": 0.03, "rep_income": 1350000},
    "Above ₹15 lakh": {"percentage": 0.02, "rep_income": 2500000}
}

total_taxpayers_AY2425 = taxpayer_counts["AY 2024-25"]

# ============================================================
# 3. COMPUTE TAX SAVINGS BY SLAB FOR AY 2024-25
# ============================================================
slab_names = []
savings_per_taxpayer = []      # tax saved per taxpayer (old_tax - new_tax) per slab
num_taxpayers_slab = []        # number of taxpayers in that slab (from distribution)
aggregate_savings_slab = []    # total savings (nominal) per slab

for slab, info in taxpayer_distribution.items():
    rep_income = info["rep_income"]
    percent = info["percentage"]
    # Calculate tax under both regimes using representative income
    saving = old_tax(rep_income) - new_tax(rep_income)
    count = total_taxpayers_AY2425 * percent
    slab_names.append(slab)
    savings_per_taxpayer.append(saving)
    num_taxpayers_slab.append(count)
    aggregate_savings_slab.append(saving * count)

# Weighted average saving per taxpayer for AY 2024-25:
total_aggregate_savings_AY2425 = sum(aggregate_savings_slab)
avg_saving_AY2425 = total_aggregate_savings_AY2425 / total_taxpayers_AY2425

# Real (inflation-adjusted) total savings:
real_total_savings_AY2425 = total_aggregate_savings_AY2425 / (1 + inflation_rate)

print(f"AY 2024-25: Average tax saving per taxpayer: ₹{avg_saving_AY2425:,.2f}")
print(f"AY 2024-25: Total discretionary income increase (nominal): ₹{total_aggregate_savings_AY2425:,.2f}")
print(f"AY 2024-25: Total discretionary income increase (real): ₹{real_total_savings_AY2425:,.2f}")

# ============================================================
# 4. COMPUTE AGGREGATE SAVINGS OVER ASSESSMENT YEARS
# ============================================================
# For simplicity, assume that the weighted average saving per taxpayer from AY 2024-25
# applies as a baseline for the earlier years as well.
years = list(taxpayer_counts.keys())
taxpayer_numbers = [taxpayer_counts[year] for year in years]
aggregate_savings_yearly = [avg_saving_AY2425 * n for n in taxpayer_numbers]
# Inflation-adjusted (real) savings for each year:
real_aggregate_savings_yearly = [s / (1 + inflation_rate) for s in aggregate_savings_yearly]

# ============================================================
# 5. ESTIMATE GDP INCREASE DUE TO EXTRA CONSUMPTION
# ============================================================
# Assume that when taxpayers save extra tax (in real terms) they spend that extra money.
# If every rupee spent adds 50 paise of value (50% profit margin or value addition),
# then the extra value added to GDP is:
value_addition_multiplier = 0.50
gdp_increase_nominal = real_total_savings_AY2425 * value_addition_multiplier

# India’s current GDP is given as ₹296.58 lakh crore.
# 1 lakh crore = 10^12 rupees. So, GDP in rupees:
current_gdp = 296.58e12
gdp_increase_percentage = (gdp_increase_nominal / current_gdp) * 100

print(f"Extra value added to GDP (real, via multiplier): ₹{gdp_increase_nominal:,.2f}")
print(f"This represents approximately {gdp_increase_percentage:.2f}% increase over current GDP.")

# ============================================================
# 6. PLOTS
# ============================================================

# Plot 1: Bar Chart of Tax Savings per Taxpayer by Income Slab (AY 2024-25)
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

# Plot 2: Line Chart of Aggregate Tax Savings (Nominal vs Real) Over Assessment Years
plt.figure(figsize=(10, 6))
plt.plot(years, np.array(aggregate_savings_yearly) / 1e12, marker='o', label="Nominal Savings (₹ Trillion)")
plt.plot(years, np.array(real_aggregate_savings_yearly) / 1e12, marker='s', label="Real Savings (₹ Trillion)")
plt.xlabel("Assessment Year")
plt.ylabel("Aggregate Tax Savings (Trillion ₹)")
plt.title("Aggregate Discretionary Income Increase Over Assessment Years")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot 3: Bar Chart for Estimated GDP Increase Due to Extra Consumption
plt.figure(figsize=(8, 6))
labels = ['Extra Value Added']
values = [gdp_increase_nominal / 1e12]  # in trillion rupees
plt.bar(labels, values, color='orange', alpha=0.8)
plt.ylabel("Increase in GDP (Trillion ₹, real terms)")
plt.title(f"Estimated GDP Increase (50% Value Addition on Extra Income)\n(~{gdp_increase_percentage:.2f}% of current GDP)")
plt.grid(axis='y', alpha=0.5)
plt.tight_layout()
plt.show()

# Plot 4: Pie Chart of Taxpayer Distribution by Income Slab (AY 2024-25)
labels = list(taxpayer_distribution.keys())
sizes = [info["percentage"] for info in taxpayer_distribution.values()]
plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
plt.title("Taxpayer Distribution by Income Slab (AY 2024-25)")
plt.tight_layout()
plt.show()

