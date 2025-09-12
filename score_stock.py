from advanced_factors import fetch_advanced_factors

def score_stock(data, ticker=None):
    score = 0
    breakdown = []

    # 1️⃣ Profitability (ROE & ROCE)
    roe = data.get('roe', 0)
    roce = data.get('roce', 0)
    prof_score = 0
    if roe > 15: prof_score += 1
    if roce > 15: prof_score += 1
    score += prof_score
    breakdown.append(f"🧮 Profitability: {prof_score}/2 (ROE: {roe}, ROCE: {roce})")

    # 2️⃣ Growth (Revenue CAGR & Profit CAGR)
    rev_cagr = data.get('revenue_cagr', 0)
    prof_cagr = data.get('profit_cagr', 0)
    growth_score = 0
    if rev_cagr > 10: growth_score += 1
    if prof_cagr > 10: growth_score += 1
    score += growth_score
    breakdown.append(f"📈 Growth: {growth_score}/2 (Revenue CAGR: {rev_cagr}%, Profit CAGR: {prof_cagr}%)")



    # 3️⃣ Valuation (PE + PEG)
    pe = data.get('pe_ratio', 0)
    peg = data.get('peg_ratio', 0)

    # Convert to float safely
    try:
        pe = float(pe)
    except (ValueError, TypeError):
        pe = 0

    try:
        peg = float(peg)
    except (ValueError, TypeError):
        peg = 0

    val_score = 0
    if 10 <= pe <= 30:
        val_score += 0.75
    if peg <= 1.5:
        val_score += 0.75

    score += val_score
    breakdown.append(f"💰 Valuation: {val_score:.1f}/1.5 (PE: {pe}, PEG: {peg})")


    # 4️⃣ Risk (Debt/Equity)
    de = data.get('de_ratio', 0)
    risk_score = 0
    if de < 1: risk_score += 1.0
    elif de < 2: risk_score += 0.5
    score += risk_score
    breakdown.append(f"⚠️ Risk: {risk_score}/1.5 (Debt/Equity: {de})")

    # 5️⃣ Management Quality
    promoter_holding = data.get('promoter_holding', 0)
    mgmt_score = 1 if promoter_holding >= 50 else 0
    score += mgmt_score
    breakdown.append(f"🧑‍💼 Management: {mgmt_score}/1 (Promoter Holding: {promoter_holding}%)")

    # 6️⃣ Sector Bonus
    good_sectors = ["AI", "Technology", "Healthcare", "Renewable", "Green", "EV"]
    sector = data.get('sector', '').lower()
    sector_score = 0.5 if any(x.lower() in sector for x in good_sectors) else 0
    score += sector_score
    breakdown.append(f"🏭 Sector Bonus: {sector_score}/0.5 ({data.get('sector', 'Unknown').title()})")

    # 7️⃣ FII/DII Trend
    trend = data.get('fii_dii_trend', '').lower()
    fii_dii_score = 0.5 if trend in ['positive', 'increasing'] else 0
    score += fii_dii_score
    breakdown.append(f"📊 FII/DII Trend: {fii_dii_score}/0.5 ({trend.title() if trend else 'N/A'})")

    # 8️⃣ Red Flags (Negative Marks)
    red_flag_score = 0
    if data.get('pledged_percent', 0) > 10:
        red_flag_score -= 0.5
        breakdown.append("🚩 Pledged Shares > 10%: -0.5")
    if de > 2:
        red_flag_score -= 0.5
        breakdown.append("🚩 High Debt/Equity > 2: -0.5")
    if red_flag_score == 0:
        breakdown.append("✅ No major red flags")
    score += red_flag_score

    return round(score, 2), breakdown
