#!/usr/bin/env python3
"""
Аналіз ринку гемблінгу / iGaming
================================
Розділи:
  1. Топ 10 ігрових (gambling) платформ / операторів
  2. Макроринок online gambling (GGR)
  3. Продуктові вертикалі та канали
  4. Український ринок
  5. Висновки

Запуск:
  python game_market_analysis.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

OUTPUT_DIR = Path("output")
REPORT_PATH = Path("GAME_MARKET_REPORT.md")

# Курс для EUR→USD у звіті (орієнтир 2025)
EUR_USD = 1.08


# ---------------------------------------------------------------------------
# Розділ 1. Топ 10 gambling-операторів за виручкою 2025
# ---------------------------------------------------------------------------
# Джерела: company FY2025 / The iGaming EU / GamblingClub rankings.
# Revenue = reported group revenue (не завжди = GGR).

TOP10_OPERATORS = pd.DataFrame(
    [
        {
            "rank": 1,
            "platform": "Flutter Entertainment",
            "brands": "FanDuel, Paddy Power, Betfair, PokerStars, Sisal, Snai",
            "category": "Sports + Casino",
            "revenue_2025_bn_usd": 16.38,
            "growth_yoy_pct": 17.0,
            "players_metric": "15.9M Average Monthly Players",
            "confidence": "high",
            "source": "Flutter FY2025 / 10-K ($16.38B)",
            "note": "Світовий №1 online operator; US (FanDuel) — ключовий драйвер росту",
        },
        {
            "rank": 2,
            "platform": "Allwyn",
            "brands": "лотереї / multi-jurisdiction lottery",
            "category": "Lottery",
            "revenue_2025_bn_usd": round(8.99 * EUR_USD, 2),
            "growth_yoy_pct": 4.0,
            "players_metric": "lottery-led group (GGR ≈ revenue scale)",
            "confidence": "high",
            "source": "The iGaming EU 2025 ranking (€8.99B)",
            "note": "Lottery-модель: великий top-line, інша економіка ніж sportsbook",
        },
        {
            "rank": 3,
            "platform": "Entain",
            "brands": "bwin, Coral, Ladbrokes, partypoker (+ BetMGM JV окремо)",
            "category": "Sports + Casino",
            "revenue_2025_bn_usd": round(6.31 * EUR_USD, 2),
            "growth_yoy_pct": 3.0,
            "players_metric": "UK/EU retail+online; US через BetMGM JV",
            "confidence": "high",
            "source": "Entain FY2025 / ranking (€6.31B; US часто окремо)",
            "note": "Зрілий EU/UK портфель; зростання стримане vs US peers",
        },
        {
            "rank": 4,
            "platform": "DraftKings",
            "brands": "DraftKings Sportsbook, Casino, DFS",
            "category": "Sports + Casino",
            "revenue_2025_bn_usd": 6.05,
            "growth_yoy_pct": 27.0,
            "players_metric": "US-focused; перший повний рік net profit",
            "confidence": "high",
            "source": "DraftKings FY2025 ($6.05B)",
            "note": "Один із найшвидших серед топ-операторів; US sportsbook war",
        },
        {
            "rank": 5,
            "platform": "bet365",
            "brands": "bet365",
            "category": "Sports + Casino",
            "revenue_2025_bn_usd": round(4.78 * EUR_USD, 2),
            "growth_yoy_pct": 9.0,
            "players_metric": "private; global sports-led brand",
            "confidence": "high",
            "source": "bet365 FY to Mar 2025 (~€4.78B / £4.04B)",
            "note": "Найбільший приватний оператор; сильний in-play sportsbook",
        },
        {
            "rank": 6,
            "platform": "FDJ United",
            "brands": "FDJ, Kindred assets (Unibet тощо)",
            "category": "Lottery + Online",
            "revenue_2025_bn_usd": round(3.68 * EUR_USD, 2),
            "growth_yoy_pct": -3.0,
            "players_metric": "France lottery core + international online",
            "confidence": "high",
            "source": "FDJ United FY2025 (€3.68B revenue; GGR вищий)",
            "note": "На GGR виглядає більшим за revenue-line (lottery accounting)",
        },
        {
            "rank": 7,
            "platform": "Kaizen Gaming",
            "brands": "Betano, Stoiximan",
            "category": "Sports + Casino",
            "revenue_2025_bn_usd": round(2.81 * EUR_USD, 2),
            "growth_yoy_pct": 13.0,
            "players_metric": "EU + LatAm (Brazil Betano)",
            "confidence": "high",
            "source": "The iGaming EU 2025 (€2.81B)",
            "note": "Активна експансія в Бразилії та регульованих ринках",
        },
        {
            "rank": 8,
            "platform": "BetMGM",
            "brands": "BetMGM",
            "category": "Sports + Casino",
            "revenue_2025_bn_usd": 2.80,
            "growth_yoy_pct": 33.0,
            "players_metric": "US JV MGM × Entain; +EBITDA",
            "confidence": "high",
            "source": "BetMGM FY2025 (~$2.8B)",
            "note": "Найшвидший ріст у топ-10; №3 у US sportsbook race",
        },
        {
            "rank": 9,
            "platform": "Lottomatica",
            "brands": "Lottomatica / Italy retail+online",
            "category": "Lottery + Online",
            "revenue_2025_bn_usd": round(2.26 * EUR_USD, 2),
            "growth_yoy_pct": 12.0,
            "players_metric": "Italy-focused; GGR > reported revenue",
            "confidence": "high",
            "source": "Lottomatica FY2025 (€2.26B)",
            "note": "Сильний домашній ринок Італії; hybrid retail/online",
        },
        {
            "rank": 10,
            "platform": "Super Group",
            "brands": "Betway, Spin",
            "category": "Sports + Casino",
            "revenue_2025_bn_usd": 2.20,
            "growth_yoy_pct": 22.0,
            "players_metric": "multi-region online; Africa + Americas focus",
            "confidence": "high",
            "source": "Super Group FY2025 ($2.2B)",
            "note": "Швидке зростання поза зрілою Європою",
        },
    ]
)


# ---------------------------------------------------------------------------
# Розділ 2. Макроринок (online GGR)
# ---------------------------------------------------------------------------

MARKET_HISTORY = pd.DataFrame(
    {
        "year": [2021, 2022, 2023, 2024, 2025, 2026],
        "ggr_bn_usd": [72.0, 82.0, 92.0, 98.0, 108.0, 121.0],
        "note": [
            "post-COVID digital shift",
            "US sportsbook ramp",
            "регульоване зростання",
            "консолідація",
            "факт / оцінка Track360",
            "прогноз ~+12% YoY",
        ],
    }
)

VERTICALS = pd.DataFrame(
    {
        "vertical": ["Online Casino", "Sports Betting", "Poker", "Bingo / Other"],
        "share_pct": [52.0, 35.0, 7.0, 6.0],
        "ggr_2026_bn": [63.0, 42.5, 8.1, 6.9],
    }
)

CHANNELS = pd.DataFrame(
    {
        "channel": ["Mobile", "Desktop / Other"],
        "share_pct": [72.0, 28.0],
    }
)

REGULATION = pd.DataFrame(
    {
        "segment": ["Regulated", "Grey / Unregulated"],
        "share_pct": [68.0, 32.0],
        "ggr_2026_bn": [82.7, 38.3],
    }
)

REGIONS = pd.DataFrame(
    {
        "region": ["Europe", "North America (US-led)", "Asia-Pacific", "LatAm", "Africa / Other"],
        "ggr_2026_bn": [43.5, 32.0, 22.0, 12.0, 11.5],
        "note": [
            "найбільший регіон ~36%",
            "US online ~$27.4B у 2025",
            "мікс regulated + grey",
            "Brazil ramp ~+$4.5B",
            "швидке, але менше базою",
        ],
    }
)

# Україна: онлайн-казино (YouControl / PlayCity), млрд грн
UA_MARKET = pd.DataFrame(
    {
        "year": [2024, 2025],
        "online_casino_revenue_uah_bn": [42.0, 45.5],
        "growth_yoy_pct": [None, 8.0],
    }
)

UA_SNAPSHOT = {
    "licensed_casinos_registry": 30,
    "licenses_annulled": 8,
    "licenses_suspended": 2,
    "budget_2025_uah_bn": 19.0,
    "blocked_illegal_sites": 3500,
    "regulator": "PlayCity",
    "top_2024_brand": "Favbet (~21.2 млрд грн виручки у 2024)",
}


def ensure_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def compute_top10_metrics(df: pd.DataFrame) -> dict:
    total = float(df["revenue_2025_bn_usd"].sum())
    top3 = float(df.head(3)["revenue_2025_bn_usd"].sum())
    fastest = df.loc[df["growth_yoy_pct"].idxmax()]
    sports_casino = df[df["category"] == "Sports + Casino"]
    return {
        "total": total,
        "top3_share": top3 / total * 100.0,
        "fastest": fastest,
        "sports_casino_n": int(len(sports_casino)),
        "sports_casino_rev": float(sports_casino["revenue_2025_bn_usd"].sum()),
        "avg_growth": float(df["growth_yoy_pct"].mean()),
    }


def compute_market_metrics() -> dict:
    ggr_2025 = float(MARKET_HISTORY.loc[MARKET_HISTORY["year"] == 2025, "ggr_bn_usd"].iloc[0])
    ggr_2026 = float(MARKET_HISTORY.loc[MARKET_HISTORY["year"] == 2026, "ggr_bn_usd"].iloc[0])
    yoy = (ggr_2026 / ggr_2025 - 1.0) * 100.0
    hist = MARKET_HISTORY.set_index("year")["ggr_bn_usd"]
    years = hist.index.max() - hist.index.min()
    cagr = (hist.iloc[-1] / hist.iloc[0]) ** (1 / years) - 1
    return {
        "ggr_2025": ggr_2025,
        "ggr_2026": ggr_2026,
        "yoy": yoy,
        "cagr": cagr * 100.0,
        "largest_vertical": VERTICALS.loc[VERTICALS["share_pct"].idxmax()],
        "largest_region": REGIONS.loc[REGIONS["ggr_2026_bn"].idxmax()],
    }


# ---------------------------------------------------------------------------
# Візуалізації
# ---------------------------------------------------------------------------

def plot_top10(df: pd.DataFrame) -> Path:
    fig, ax = plt.subplots(figsize=(11, 6.5))
    colors = {
        "Sports + Casino": "#1f6f8b",
        "Lottery": "#f18f01",
        "Lottery + Online": "#c44536",
    }
    bar_colors = [colors.get(c, "#666666") for c in df["category"]]
    y = np.arange(len(df))[::-1]
    bars = ax.barh(y, df["revenue_2025_bn_usd"], color=bar_colors)
    ax.set_yticks(y)
    ax.set_yticklabels([f"#{r}  {p}" for r, p in zip(df["rank"], df["platform"])])
    ax.set_xlabel("Revenue 2025, млрд USD")
    ax.set_title("Розділ 1. Топ 10 gambling-операторів за виручкою")
    ax.grid(axis="x", alpha=0.3)

    for bar, growth in zip(bars, df["growth_yoy_pct"]):
        w = bar.get_width()
        ax.annotate(
            f"${w:.1f}B  ({growth:+.0f}%)",
            xy=(w, bar.get_y() + bar.get_height() / 2),
            xytext=(4, 0),
            textcoords="offset points",
            va="center",
            fontsize=8,
        )

    handles = [
        plt.Rectangle((0, 0), 1, 1, color=c)
        for c in (colors["Sports + Casino"], colors["Lottery"], colors["Lottery + Online"])
    ]
    ax.legend(handles, ["Sports + Casino", "Lottery", "Lottery + Online"], loc="lower right")
    path = OUTPUT_DIR / "top10_operators_revenue.png"
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)
    return path


def plot_top10_growth(df: pd.DataFrame) -> Path:
    ordered = df.sort_values("growth_yoy_pct", ascending=True)
    fig, ax = plt.subplots(figsize=(10, 5.5))
    colors = ["#c44536" if g < 0 else "#99c24d" for g in ordered["growth_yoy_pct"]]
    ax.barh(ordered["platform"], ordered["growth_yoy_pct"], color=colors)
    ax.axvline(0, color="#333333", linewidth=0.8)
    ax.set_xlabel("YoY growth, %")
    ax.set_title("Топ 10: темпи зростання виручки 2025")
    ax.grid(axis="x", alpha=0.3)
    path = OUTPUT_DIR / "top10_operators_growth.png"
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)
    return path


def plot_market_history(df: pd.DataFrame) -> Path:
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(df["year"], df["ggr_bn_usd"], marker="o", color="#1f6f8b", linewidth=2)
    ax.fill_between(df["year"], df["ggr_bn_usd"], alpha=0.15, color="#1f6f8b")
    ax.set_xlabel("Рік")
    ax.set_ylabel("Online GGR, млрд USD")
    ax.set_title("Глобальний online gambling GGR")
    ax.grid(alpha=0.3)
    for _, row in df.iterrows():
        ax.annotate(
            f"{row['ggr_bn_usd']:.0f}",
            (row["year"], row["ggr_bn_usd"]),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center",
            fontsize=8,
        )
    path = OUTPUT_DIR / "market_ggr_history.png"
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)
    return path


def plot_verticals(df: pd.DataFrame) -> Path:
    fig, ax = plt.subplots(figsize=(7, 7))
    colors = ["#1f6f8b", "#99c24d", "#f18f01", "#c44536"]
    ax.pie(
        df["share_pct"],
        labels=df["vertical"],
        autopct="%1.0f%%",
        colors=colors,
        startangle=90,
        wedgeprops=dict(width=0.45, edgecolor="white"),
    )
    ax.set_title("Вертикалі online gambling (частка GGR)")
    path = OUTPUT_DIR / "verticals_share.png"
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)
    return path


def plot_regions(df: pd.DataFrame) -> Path:
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(df["region"], df["ggr_2026_bn"], color="#1f6f8b")
    ax.set_ylabel("GGR 2026, млрд USD")
    ax.set_title("Online gambling за регіонами (орієнтир 2026)")
    ax.tick_params(axis="x", rotation=20)
    ax.grid(axis="y", alpha=0.3)
    for _, row in df.iterrows():
        ax.annotate(
            f"{row['ggr_2026_bn']:.1f}",
            (row["region"], row["ggr_2026_bn"]),
            textcoords="offset points",
            xytext=(0, 4),
            ha="center",
            fontsize=8,
        )
    path = OUTPUT_DIR / "regions_ggr.png"
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)
    return path


def plot_ua_market(df: pd.DataFrame) -> Path:
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(df["year"].astype(str), df["online_casino_revenue_uah_bn"], color="#1f6f8b")
    ax.set_ylabel("Виручка онлайн-казино, млрд грн")
    ax.set_title("Україна: виручка ліцензованих онлайн-казино")
    ax.grid(axis="y", alpha=0.3)
    for _, row in df.iterrows():
        ax.annotate(
            f"{row['online_casino_revenue_uah_bn']:.1f}",
            (str(row["year"]), row["online_casino_revenue_uah_bn"]),
            textcoords="offset points",
            xytext=(0, 4),
            ha="center",
        )
    path = OUTPUT_DIR / "ua_online_casino.png"
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)
    return path


# ---------------------------------------------------------------------------
# Звіт
# ---------------------------------------------------------------------------

def build_report(top10: dict, market: dict, charts: list[Path]) -> str:
    fastest = top10["fastest"]
    lines = [
        "# Аналіз ринку гемблінгу (iGaming)",
        "",
        "*Звіт згенеровано скриптом `game_market_analysis.py`.*",
        "",
        "## Розділ 1. Топ 10 ігрових платформ (gambling-оператори)",
        "",
        "Ранжування за **group revenue 2025** (не GGR). "
        "Бренди в дужках — ключові продукти оператора.",
        "",
        f"- Сума топ-10: **${top10['total']:.1f}B** revenue",
        f"- Частка топ-3: **{top10['top3_share']:.0f}%** від суми топ-10",
        f"- Sports+Casino брендів у списку: **{top10['sports_casino_n']}** "
        f"(${top10['sports_casino_rev']:.1f}B)",
        f"- Найшвидший ріст: **{fastest['platform']}** "
        f"(+{fastest['growth_yoy_pct']:.0f}% YoY)",
        f"- Середній YoY по топ-10: **{top10['avg_growth']:+.1f}%**",
        "",
        "| # | Оператор | Бренди | Категорія | Revenue 2025 | YoY |",
        "|---|----------|--------|-----------|--------------|-----|",
    ]

    for _, row in TOP10_OPERATORS.iterrows():
        rev = f"${row['revenue_2025_bn_usd']:.2f}".rstrip("0").rstrip(".") + "B"
        lines.append(
            f"| {row['rank']} | **{row['platform']}** | {row['brands']} | "
            f"{row['category']} | {rev} | {row['growth_yoy_pct']:+.0f}% |"
        )

    lines += ["", "### Профілі", ""]
    for _, row in TOP10_OPERATORS.iterrows():
        lines.append(
            f"**{row['rank']}. {row['platform']}** — {row['note']} "
            f"Аудиторія/масштаб: {row['players_metric']}. "
            f"Джерело: {row['source']}."
        )
        lines.append("")

    lines += [
        "### Інсайти розділу 1",
        "",
        "1. **Flutter домінує з відривом** (~$16.4B) — майже як DraftKings + Entain разом.",
        "2. **Найшвидше ростуть US-бренди**: BetMGM (+33%), DraftKings (+27%), "
        "плюс Super Group (+22%) поза зрілою Європою.",
        "3. **Lottery-оператори (Allwyn, FDJ, Lottomatica)** на revenue-line виглядають "
        "інакше, ніж на GGR — для apples-to-apples порівнюйте GGR окремо.",
        "4. **Консолідація триває**: топ-оператори забирають дедалі більшу частку "
        "регульованого GGR (Track360: top-10 ~42% regulated GGR).",
        "5. Для України релевантні не глобальні гіганти напряму, а **локальні ліцензовані "
        "бренди** + B2B (Evolution тощо) як постачальники контенту.",
        "",
        "![top10_operators_revenue](output/top10_operators_revenue.png)",
        "",
        "![top10_operators_growth](output/top10_operators_growth.png)",
        "",
        "---",
        "",
        "## Розділ 2. Макроринок online gambling",
        "",
        f"- **2025 GGR:** ~**${market['ggr_2025']:.0f}B**",
        f"- **2026 GGR (прогноз):** ~**${market['ggr_2026']:.0f}B** "
        f"(+{market['yoy']:.0f}% YoY)",
        f"- **CAGR 2021–2026:** ~**{market['cagr']:.1f}%**",
        f"- Найбільша вертикаль: **{market['largest_vertical']['vertical']}** "
        f"({market['largest_vertical']['share_pct']:.0f}%)",
        f"- Найбільший регіон: **{market['largest_region']['region']}** "
        f"(~${market['largest_region']['ggr_2026_bn']:.1f}B)",
        "",
        "- Регульований ринок: **~68%** GGR",
        "- Mobile: **~72%** online revenue",
        "- США — найбільша країна (~$27.4B online GGR у 2025)",
        "- LatAm — найшвидший великий регіон (Brazil regulated ramp)",
        "",
        "![market_ggr_history](output/market_ggr_history.png)",
        "",
        "![regions_ggr](output/regions_ggr.png)",
        "",
        "---",
        "",
        "## Розділ 3. Вертикалі та канали",
        "",
        "| Вертикаль | Частка GGR | GGR 2026 (орієнтир) |",
        "|-----------|------------|---------------------|",
    ]
    for _, row in VERTICALS.iterrows():
        lines.append(
            f"| {row['vertical']} | {row['share_pct']:.0f}% | ${row['ggr_2026_bn']:.1f}B |"
        )

    lines += [
        "",
        "| Канал | Частка |",
        "|-------|--------|",
    ]
    for _, row in CHANNELS.iterrows():
        lines.append(f"| {row['channel']} | {row['share_pct']:.0f}% |")

    lines += [
        "",
        "| Регуляція | Частка | GGR 2026 |",
        "|-----------|--------|----------|",
    ]
    for _, row in REGULATION.iterrows():
        lines.append(
            f"| {row['segment']} | {row['share_pct']:.0f}% | ${row['ggr_2026_bn']:.1f}B |"
        )

    lines += [
        "",
        "![verticals_share](output/verticals_share.png)",
        "",
        "---",
        "",
        "## Розділ 4. Український ринок",
        "",
        f"- Регулятор: **{UA_SNAPSHOT['regulator']}** (замість КРАІЛ).",
        f"- Виручка ліцензованих онлайн-казино **2025:** "
        f"**{UA_MARKET.loc[UA_MARKET['year'] == 2025, 'online_casino_revenue_uah_bn'].iloc[0]:.1f} млрд грн** "
        f"(+8% vs 2024 / 42 млрд грн) — YouControl.",
        f"- У реєстрі: **{UA_SNAPSHOT['licensed_casinos_registry']}** онлайн-казино; "
        f"анульовано **{UA_SNAPSHOT['licenses_annulled']}**, призупинено "
        f"**{UA_SNAPSHOT['licenses_suspended']}**.",
        f"- До бюджету 2025: ~**{UA_SNAPSHOT['budget_2025_uah_bn']:.0f} млрд грн** "
        f"(ліцензії + податки + лотереї).",
        f"- Заблоковано **>{UA_SNAPSHOT['blocked_illegal_sites']}** нелегальних сайтів.",
        f"- Орієнтир лідера 2024: {UA_SNAPSHOT['top_2024_brand']}.",
        "",
        "Ринок стабілізується після бурхливої легалізації: нових ліцензій у 2025 мало (2), "
        "акцент зміщується на контроль, блокування сірого ринку та цифрові ліцензії.",
        "",
        "![ua_online_casino](output/ua_online_casino.png)",
        "",
        "---",
        "",
        "## Розділ 5. Висновки",
        "",
        "1. **Глобальний online gambling ~$108→$121B GGR** — зростання двознакове, "
        "драйвери: US, Brazil, mobile.",
        "2. **Топ-платформи = Flutter / Allwyn / Entain / DraftKings / bet365**; "
        "швидкість росту вища в US і emerging markets.",
        "3. **Casino лишається найбільшою вертикаллю**, sports betting — найдинамічніша "
        "в нових юрисдикціях.",
        "4. **Україна** — регульований, але ще консолідаційний ринок (~45.5 млрд грн "
        "онлайн-казино); compliance і боротьба з нелегалами — головна тема 2026.",
        "5. Можливості: ліцензований product + localized payments; ризики — регуляторний "
        "тиск, advertising bans, санкційні списки.",
        "",
        "## Усі графіки",
        "",
    ]
    for p in charts:
        lines.append(f"![{p.stem}]({p.as_posix()})")
        lines.append("")

    lines += [
        "## Джерела",
        "",
        "- [Track360 — Online Gambling Statistics 2026](https://track360.io/blog/online-gambling-statistics-2026-global-market-data)",
        "- [Track360 — iGaming Q1 2026 / top operators](https://track360.io/blog/igaming-industry-statistics-q1-2026-report)",
        "- [The iGaming EU — 2025 revenue ranking](https://theigaming.eu/2026/04/12/2025-gambling-revenue-15-largest-companies-ranked/)",
        "- [GamblingClub — top companies 2025](https://gamblingclub.be/en/flutter-remains-worlds-largest-gambling-company/)",
        "- Flutter Entertainment FY2025 / 10-K",
        "- [YouControl / Fair — онлайн-казино України 2025](https://www.fair.org.ua/eksperty-ozvuchyly-dani-shhodo-zrostannya-rynku-igaming-v-ukrayini/)",
        "- PlayCity / Delo.ua — бюджет і блокування нелегалів 2025",
        "",
        "> Примітка: **Revenue ≠ GGR**. Lottery-оператори часто мають вищий GGR "
        "за нижчий net revenue. Цифри сірих ринків — оцінки.",
        "",
    ]
    return "\n".join(lines)


def print_summary(top10: dict, market: dict) -> None:
    print("=" * 68)
    print(" АНАЛІЗ РИНКУ ГЕМБЛІНГУ (iGaming)")
    print("=" * 68)
    print("\nРозділ 1. Топ 10 операторів (revenue 2025):")
    for _, row in TOP10_OPERATORS.iterrows():
        print(
            f"  {row['rank']:>2}. {row['platform']:<24} "
            f"${row['revenue_2025_bn_usd']:>5.1f}B  "
            f"({row['growth_yoy_pct']:+.0f}%)  [{row['category']}]"
        )
    print(
        f"\n  Σ топ-10: ${top10['total']:.1f}B | "
        f"топ-3: {top10['top3_share']:.0f}% | "
        f"avg YoY: {top10['avg_growth']:+.1f}%"
    )
    print(
        f"\nМакроринок online GGR: "
        f"${market['ggr_2025']:.0f}B (2025) → "
        f"${market['ggr_2026']:.0f}B (2026, +{market['yoy']:.0f}%)"
    )
    print(
        f"Україна онлайн-казино 2025: "
        f"{UA_MARKET.loc[UA_MARKET['year'] == 2025, 'online_casino_revenue_uah_bn'].iloc[0]:.1f} млрд грн (+8%)"
    )
    print("=" * 68)


def main() -> None:
    ensure_output_dir()
    # Прибрати артефакти старого video-games аналізу
    for stale in OUTPUT_DIR.glob("*"):
        if stale.suffix in {".png", ".csv"}:
            stale.unlink()

    top10 = compute_top10_metrics(TOP10_OPERATORS)
    market = compute_market_metrics()

    charts = [
        plot_top10(TOP10_OPERATORS),
        plot_top10_growth(TOP10_OPERATORS),
        plot_market_history(MARKET_HISTORY),
        plot_verticals(VERTICALS),
        plot_regions(REGIONS),
        plot_ua_market(UA_MARKET),
    ]

    REPORT_PATH.write_text(build_report(top10, market, charts), encoding="utf-8")
    TOP10_OPERATORS.to_csv(OUTPUT_DIR / "top10_operators.csv", index=False)
    MARKET_HISTORY.to_csv(OUTPUT_DIR / "market_ggr_history.csv", index=False)
    VERTICALS.to_csv(OUTPUT_DIR / "verticals.csv", index=False)
    REGIONS.to_csv(OUTPUT_DIR / "regions.csv", index=False)
    UA_MARKET.to_csv(OUTPUT_DIR / "ua_market.csv", index=False)

    print_summary(top10, market)
    print(f"\nЗвіт:    {REPORT_PATH}")
    for p in charts:
        print(f"  - {p}")


if __name__ == "__main__":
    main()
