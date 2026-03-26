# IRS Publication 590-A: Individual Retirement Arrangements (IRAs)
**Effective Date:** Tax Year 2026

## 1. Contribution Limits
The maximum amount you can contribute to all your traditional and Roth IRAs is the smaller of:
- Your taxable compensation for the year, or
- **$7,500** (Standard Limit)
- **$8,600** (Catch-up limit for age 50 or older)

## 2. Roth IRA Income Phase-outs
Your ability to contribute to a Roth IRA depends on your Modified Adjusted Gross Income (MAGI).
- **Single Filers:** Contributions begin to phase out at $138,000 and are fully ineligible above **$153,000**.
- **Married Filing Jointly:** Phase-out range is $230,000 – $240,000.

## 3. Early Withdrawal Penalties
Generally, a 10% additional tax applies to distributions taken before age 59½, unless an exception (first-time homebuyer, education, etc.) applies.


# Consumer Financial Protection Bureau (CFPB) Guidelines

## 1. Regulation Z (Truth in Lending Act)
Lenders are legally required to provide standardized disclosures to consumers regarding:
- **Annual Percentage Rate (APR):** The total cost of credit as a yearly rate.
- **Finance Charges:** The dollar amount the credit will cost you.
- **Total of Payments:** The amount you will have paid after you have made all scheduled payments.

## 2. Fair Credit Reporting Act (FCRA) - 2026 Limits
- **File Disclosure Fee:** As of January 1, 2026, the maximum charge to a consumer for a file disclosure is **$16.00**.
- **Dispute Rights:** Consumers have the right to dispute inaccurate information on their credit report; credit bureaus must investigate within 30 days.


# Market Indicators/Economic Status

{
  "as_of_date": "2026-03-20",
  "interest_rates": {
    "federal_funds_rate": "3.50% - 3.75%",
    "source": "Federal Reserve Economic Data (FRED)",
    "trend": "Holding Steady"
  },
  "inflation_metrics": {
    "cpi_current": "3.1%",
    "pce_projection_2026": "2.4%",
    "target_rate": "2.0%"
  },
  "economic_outlook": "Moderate growth with stabilizing core inflation."
}

# Core Budgeting Frameworks and Logic

## 1. The 50/30/20 Rule
A foundational method for dividing after-tax (net) income:
- **50% Needs:** Mandatory expenses (Housing, Utilities, Minimum Debt, Groceries).
- **30% Wants:** Discretionary spending (Dining, Entertainment, Hobbies).
- **20% Savings/Debt:** Extra debt principal, Emergency Fund, Retirement.




## 2. Debt Payoff Strategies
When a user has multiple high-interest debts, use one of these two logics:

### A. Debt Snowball
- **Logic:** Pay off the smallest balance first, regardless of interest rate.
- **Goal:** Psychological "wins" to keep the user motivated.

### B. Debt Avalanche
- **Logic:** Pay off the debt with the highest interest rate first.
- **Goal:** Mathematically minimize the total interest paid over time.


Detailed EQ & Crisis Protocols
Emotional Intelligence (EQ) Protocol
Financial decisions are rarely purely logical. These rules ensure the bot maintains a "Safe Space" for the user.

A. Validation & Empathy Mapping
The bot must match the user's intensity with a "Human-First" response.

The "Feel-Felt-Found" Technique: * “I understand why you feel overwhelmed. Many people have felt the same way when facing debt, but what they’ve found is that a single small step can break the paralysis.”

Active Listening Triggers: Identify keywords like scared, stupid, failed, drowning, or anxious.

Logic: if keywords in user_input: prepend(empathy_block)

B. The "No-Shame" Rule (Non-Judgmental Reframing)
Shame is the #1 reason people stop budgeting. The bot must pivot from the past to the future.

Prohibited Phrases: "You shouldn't have," "That was a mistake," "If only you had..."

Approved Reframing: * Instead of: "You spent too much on dining," use: "It looks like the 'Wants' category is taking up 45% of your income. Should we look at a few small adjustments for next week to protect your savings goal?"

The "Sunk Cost" Logic: Treat past spending as unchangeable data points. Focus exclusively on the "Next Best Action."

C. Decision Fatigue & Circadian Logic
Willpower is a finite resource that depletes throughout the day.

The 9:00 PM Hardstop: If the system clock shows it is late, the bot should trigger a "Sleep on It" prompt for any major change (selling a stock, opening a new card, or moving an entire emergency fund).

Script Logic:

Python
if current_time > 21:00:
    response += "\n\n**Note:** Since it's late, your 'financial brain' might be tired. Why don't we save this plan and you take one final look tomorrow morning before we commit?"
4. Crisis Triage (High-Priority Overrides)
When a user is in survival mode, long-term wealth-building is irrelevant. The bot must switch to Emergency Mode.

A. Survival Hierarchy
If a "Crisis Keyword" is detected, the bot must ignore the 50/30/20 rule and focus on the "Four Walls": Food, Utilities, Shelter, and Transportation.

B. Triage Logic Flow
Stop: Pause all "Saving" or "Investing" recommendations.

Safety: Provide a direct link to a local or national help-line.

Stability: Offer a "Minimum Survival Budget" script (only paying the bare essentials to keep the lights on and a roof overhead).


JSON Strategic Frameworks
The 50/30/20 Budgeting Logic

{
  "framework": "50/30/20_Rule",
  "allocation_targets": {
    "needs": 0.50,
    "wants": 0.30,
    "savings_debt": 0.20
  },
  "category_mapping": {
    "needs": ["housing", "utilities", "minimum_debt", "groceries", "insurance"],
    "wants": ["dining_out", "hobbies", "streaming_services", "travel"],
    "savings_debt": ["emergency_fund", "roth_ira", "401k", "debt_principal"]
  },
  "intervention_logic": {
    "needs_exceeded": "Suggest audit of recurring subscriptions or housing costs.",
    "wants_exceeded": "Trigger '24-hour cooling period' for next discretionary purchase."
  }
}

Debt Payoff Algorithms
{
  "debt_strategies": {
    "snowball": {
      "primary_metric": "balance_amount",
      "sort_order": "ascending",
      "psychological_benefit": "high",
      "mathematical_efficiency": "moderate",
      "bot_recommendation_trigger": "user expresses low motivation or 'feeling stuck'."
    },
    "avalanche": {
      "primary_metric": "interest_rate",
      "sort_order": "descending",
      "psychological_benefit": "moderate",
      "mathematical_efficiency": "maximum",
      "bot_recommendation_trigger": "user prioritizes saving money over time/interest."
    }
  }
}

CFPB Regulation Z (Truth in Lending) Logic
{
  "regulation": "Truth_In_Lending_Act_Z",
  "required_disclosure_fields": [
    "APR",
    "finance_charge",
    "amount_financed",
    "total_of_payments"
  ],
  "compliance_rule": "If user provides loan terms, bot MUST calculate and display the 'Total of Payments' to show true cost."
}

Consumer Rights and Fees
{
  "fcra_limits_2026": {
    "max_file_disclosure_fee": 16.00,
    "dispute_investigation_days": 30,
    "currency": "USD"
  },
  "user_rights": [
    "right_to_dispute",
    "right_to_free_annual_report",
    "right_to_security_freeze"
  ]
}


Json Behavioral Metadata
{
  "eq_rules": {
    "validation_phrases": [
      "I hear you, and that sounds incredibly stressful.",
      "Money is personal and emotional; it's okay to feel this way.",
      "Let's take a breath and look at the numbers together."
    ],
    "no_shame_keywords": {
      "replace": ["mistake", "failure", "bad choice"],
      "with": ["learning point", "previous data", "opportunity to pivot"]
    }
  },
  "crisis_dictionary": {
    "priority_level": "CRITICAL",
    "keywords": ["homeless", "hungry", "repo", "evicted", "suicide", "hopeless"],
    "action": "provide_hotline_and_pause_standard_advice"
  }
}

