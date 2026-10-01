#!/usr/bin/env python3
"""
Аналіз ігрового ринку (глобальний + Україна)
============================================
Розділи:
  1. Топ 10 ігрових платформ (за виручкою ігор, 2025)
  2. Макроринок Mobile / Console / PC (Newzoo)
  3. Монетизація
  4. Український контекст
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


# ---------------------------------------------------------------------------
# Розділ 1. Топ 10 ігрових платформ (consumer games spend / storefront, 2025)
# ---------------------------------------------------------------------------
# Ранжування за виручкою ігор на платформі/сторфронті.
# Де офіційних цифр немає — позначено confidence=estimate.
# Курс для yen-фігур: ≈150 JPY/USD (орієнтир).

TOP10_PLATFORMS = pd.DataFrame(
    [
        {
            "rank": 1,
            "platform": "Apple App Store",
            "category": "Mobile",
            "owner": "Apple",
            "revenue_2025_bn": 52.5,
            "growth_yoy_pct": 0.6,
            "users_metric": "850M середн. тижневих користувачів App Store",
            "users_value_m": 850.0,
            "confidence": "high",
            "source": "Sensor Tower / industry reports",
            "note": "Найбільший ігровий сторфронт у світі за виручкою IAP",
        },
        {
            "rank": 2,
            "platform": "Google Play",
            "category": "Mobile",
            "owner": "Google",
            "revenue_2025_bn": 30.0,
            "growth_yoy_pct": -1.0,
            "users_metric": "42.4B завантажень ігор у 2025",
            "users_value_m": None,
            "confidence": "high",
            "source": "Sensor Tower",
            "note": "Лідер за обсягом downloads; виручка нижча за iOS через ціни/ринки",
        },
        {
            "rank": 3,
            "platform": "China Android stores",
            "category": "Mobile",
            "owner": "Tencent / Huawei / Xiaomi / OPPO / Vivo / TapTap",
            "revenue_2025_bn": 28.0,
            "growth_yoy_pct": 5.0,
            "users_metric": "агреговано (без Google Play у КНР)",
            "users_value_m": None,
            "confidence": "estimate",
            "source": "залишок Newzoo mobile мінус App Store/GP",
            "note": "Фрагментований канал; критичний для global mobile top-grossing",
        },
        {
            "rank": 4,
            "platform": "PlayStation Network",
            "category": "Console",
            "owner": "Sony",
            "revenue_2025_bn": 16.1,
            "growth_yoy_pct": 5.5,
            "users_metric": "124M MAU (бер. 2025)",
            "users_value_m": 124.0,
            "confidence": "high",
            "source": "Sony FY2025 digital software + add-on (¥2.415T)",
            "note": "Лише digital software/add-on; Network Services (~$5.1B) окремо",
        },
        {
            "rank": 5,
            "platform": "Steam",
            "category": "PC",
            "owner": "Valve",
            "revenue_2025_bn": 11.7,
            "growth_yoy_pct": 13.0,
            "users_metric": "~132–198M MAU (оцінки)",
            "users_value_m": 165.0,
            "confidence": "medium",
            "source": "Sensor Tower; MAU — GameDiscoverCo / DSA EU",
            "note": "Найшвидший ріст серед великих PC/console сторів (+13%); ~75% PC digital",
        },
        {
            "rank": 6,
            "platform": "Xbox (Store + Game Pass)",
            "category": "Console / PC",
            "owner": "Microsoft",
            "revenue_2025_bn": 8.0,
            "growth_yoy_pct": 8.0,
            "users_metric": "Game Pass ~37M підписників",
            "users_value_m": 37.0,
            "confidence": "estimate",
            "source": "Game Pass ~$5B + оцінка digital store",
            "note": "Підписка — ядро екосистеми; hardware слабший за PS",
        },
        {
            "rank": 7,
            "platform": "Roblox",
            "category": "UGC platform",
            "owner": "Roblox Corporation",
            "revenue_2025_bn": 5.0,
            "growth_yoy_pct": 20.0,
            "users_metric": "~450M MAU",
            "users_value_m": 450.0,
            "confidence": "estimate",
            "source": "engagement Sensor Tower; bookings — орієнтир",
            "note": "І гра, і платформа; домінує в cross-platform engagement",
        },
        {
            "rank": 8,
            "platform": "Nintendo eShop",
            "category": "Console",
            "owner": "Nintendo",
            "revenue_2025_bn": 2.6,
            "growth_yoy_pct": 25.0,
            "users_metric": "Switch 2 >10M шт. у частковому 2025",
            "users_value_m": None,
            "confidence": "high",
            "source": "Nintendo digital software FY (~¥408B / ~$2.6B)",
            "note": "Digital ~55% software; first-party IP тримає виручку",
        },
        {
            "rank": 9,
            "platform": "Epic Games Store",
            "category": "PC",
            "owner": "Epic Games",
            "revenue_2025_bn": 1.16,
            "growth_yoy_pct": 6.0,
            "users_metric": "78M MAU на PC",
            "users_value_m": 78.0,
            "confidence": "high",
            "source": "Epic Games Store 2025 Year in Review",
            "note": "3P spending +57% до $400M; без D2C Fortnite/Marvel Rivals тощо",
        },
        {
            "rank": 10,
            "platform": "Battle.net / інші клієнти",
            "category": "PC / Multi",
            "owner": "Blizzard / Riot / Amazon / Samsung",
            "revenue_2025_bn": 1.0,
            "growth_yoy_pct": 0.0,
            "users_metric": "фрагментовано (WoW, LoL client, Galaxy Store…)",
            "users_value_m": None,
            "confidence": "estimate",
            "source": "агрегований орієнтир second-tier storefronts",
            "note": "Включно з Galaxy Store, Amazon Appstore, itch.io тощо",
        },
    ]
)


# ---------------------------------------------------------------------------
# Розділ 2+. Макроринок (Newzoo)
# ---------------------------------------------------------------------------

SEGMENT_REVENUE = pd.DataFrame(
    {
        "segment": ["Mobile", "Console", "PC"],
        "revenue_2025_bn": [113.3, 44.7, 43.6],
        "growth_2025_pct": [10.7, 2.8, 12.0],
        "revenue_2026_bn": [121.1, 46.9, 45.9],
        "growth_2026_pct": [6.8, 5.1, 5.3],
    }
)

MARKET_HISTORY = pd.DataFrame(
    {
        "year": [2021, 2022, 2023, 2024, 2025, 2026],
        "revenue_bn": [180.3, 184.4, 184.0, 184.9, 201.6, 213.9],
        "note": [
            "після-COVID пік",
            "стабілізація",
            "плато",
            "повільне відновлення",
            "перший раз > $200B",
            "прогноз Newzoo",
        ],
    }
)

MONETIZATION = pd.DataFrame(
    {
        "model": [
            "In-game / live service",
            "Full-game (premium)",
            "Subscriptions",
            "Інше",
        ],
        "share_pct": [52.0, 28.0, 14.0, 6.0],
    }
)

UA_CONSOLE_SHARE = pd.DataFrame(
    {
        "brand": ["PlayStation", "Steam Deck", "Nintendo", "Xbox", "Інше (Lenovo тощо)"],
        "rank": [1, 2, 3, 4, 5],
        "approx_share_pct": [85.0, 6.0, 4.5, 3.0, 1.5],
    }
)

UA_STUDIO_PLATFORMS = pd.DataFrame(
    {
        "platform": ["Mobile", "PC", "Console / multi"],
        "studios_in_top20": [14, 12, 4],
    }
)


def ensure_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def compute_segment_metrics(df: pd.DataFrame) -> dict:
    total_2025 = float(df["revenue_2025_bn"].sum())
    total_2026 = float(df["revenue_2026_bn"].sum())
    yoy_2026 = (total_2026 / total_2025 - 1.0) * 100.0
    shares_2025 = df["revenue_2025_bn"] / total_2025 * 100.0
    shares_2026 = df["revenue_2026_bn"] / total_2026 * 100.0
    hist = MARKET_HISTORY.set_index("year")["revenue_bn"]
    years = hist.index.max() - hist.index.min()
    cagr = (hist.iloc[-1] / hist.iloc[0]) ** (1 / years) - 1
    return {
        "total_2025": total_2025,
        "total_2026": total_2026,
        "yoy_2026": yoy_2026,
        "shares_2025": shares_2025,
        "shares_2026": shares_2026,
        "fastest_2025": df.loc[df["growth_2025_pct"].idxmax()],
        "fastest_2026": df.loc[df["growth_2026_pct"].idxmax()],
        "largest_2026": df.loc[df["revenue_2026_bn"].idxmax()],
        "cagr_2021_2026": cagr * 100.0,
    }


def compute_top10_metrics(df: pd.DataFrame) -> dict:
    total = float(df["revenue_2025_bn"].sum())
    top3 = float(df.head(3)["revenue_2025_bn"].sum())
    mobile = float(df.loc[df["category"] == "Mobile", "revenue_2025_bn"].sum())
    fastest = df.loc[df["growth_yoy_pct"].idxmax()]
    return {
        "total_tracked": total,
        "top3_share": top3 / total * 100.0,
        "mobile_share": mobile / total * 100.0,
        "fastest": fastest,
        "high_confidence_n": int((df["confidence"] == "high").sum()),
    }


# ---------------------------------------------------------------------------
# Візуалізації
# ---------------------------------------------------------------------------

def plot_top10_revenue(df: pd.DataFrame) -> Path:
    fig, ax = plt.subplots(figsize=(11, 6))
    colors = {
        "Mobile": "#99c24d",
        "Console": "#1f6f8b",
        "PC": "#f18f01",
        "Console / PC": "#5c4d7a",
        "UGC platform": "#c44536",
        "PC / Multi": "#666666",
    }
    bar_colors = [colors.get(c, "#888888") for c in df["category"]]
    # rank 1 зверху
    y = np.arange(len(df))[::-1]
    bars = ax.barh(y, df["revenue_2025_bn"], color=bar_colors)
    ax.set_yticks(y)
    labels = [f"#{r}  {p}" for r, p in zip(df["rank"], df["platform"])]
    ax.set_yticklabels(labels)
    ax.set_xlabel("Виручка ігор, млрд USD (2025)")
    ax.set_title("Розділ 1. Топ 10 ігрових платформ за виручкою")
    ax.grid(axis="x", alpha=0.3)

    for bar, conf in zip(bars, df["confidence"]):
        h = bar.get_width()
        suffix = "" if conf == "high" else (" ≈" if conf == "medium" else " *")
        ax.annotate(
            f"{h:.1f}{suffix}",
            xy=(h, bar.get_y() + bar.get_height() / 2),
            xytext=(4, 0),
            textcoords="offset points",
            va="center",
            fontsize=8,
        )

    # Легенда категорій
    handles = [
        plt.Rectangle((0, 0), 1, 1, color=col)
        for cat, col in [
            ("Mobile", colors["Mobile"]),
            ("Console", colors["Console"]),
            ("PC", colors["PC"]),
            ("Інше", colors["UGC platform"]),
        ]
    ]
    ax.legend(handles, ["Mobile", "Console", "PC", "Інше"], loc="lower right")
    ax.text(
        0.01,
        -0.12,
        "* оцінка  ·  ≈ середня впевненість  ·  без зірочки — high confidence",
        transform=ax.transAxes,
        fontsize=8,
        color="#555555",
    )

    path = OUTPUT_DIR / "top10_platforms_revenue.png"
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)
    return path


def plot_top10_by_category(df: pd.DataFrame) -> Path:
    grouped = (
        df.groupby("category", as_index=False)["revenue_2025_bn"]
        .sum()
        .sort_values("revenue_2025_bn", ascending=False)
    )
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(grouped["category"], grouped["revenue_2025_bn"], color="#1f6f8b")
    ax.set_ylabel("Виручка, млрд USD")
    ax.set_title("Топ 10: виручка за категорією платформи")
    ax.grid(axis="y", alpha=0.3)
    for i, row in grouped.iterrows():
        ax.annotate(
            f"{row['revenue_2025_bn']:.1f}",
            (row["category"], row["revenue_2025_bn"]),
            textcoords="offset points",
            xytext=(0, 4),
            ha="center",
            fontsize=9,
        )
    path = OUTPUT_DIR / "top10_by_category.png"
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)
    return path


def plot_segment_revenue(df: pd.DataFrame) -> Path:
    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.arange(len(df))
    width = 0.36
    bars_2025 = ax.bar(
        x - width / 2, df["revenue_2025_bn"], width, label="2025", color="#1f6f8b"
    )
    bars_2026 = ax.bar(
        x + width / 2, df["revenue_2026_bn"], width, label="2026 (прогноз)", color="#99c24d"
    )
    ax.set_ylabel("Виручка, млрд USD")
    ax.set_title("Макроринок: Mobile / Console / PC")
    ax.set_xticks(x)
    ax.set_xticklabels(df["segment"])
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    for bars in (bars_2025, bars_2026):
        for bar in bars:
            h = bar.get_height()
            ax.annotate(
                f"{h:.1f}",
                xy=(bar.get_x() + bar.get_width() / 2, h),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=8,
            )
    path = OUTPUT_DIR / "platform_revenue.png"
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)
    return path


def plot_market_history(df: pd.DataFrame) -> Path:
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(df["year"], df["revenue_bn"], marker="o", color="#1f6f8b", linewidth=2)
    ax.fill_between(df["year"], df["revenue_bn"], alpha=0.15, color="#1f6f8b")
    ax.axhline(200, color="#c44536", linestyle="--", linewidth=1, label="$200B рубіж")
    ax.set_xlabel("Рік")
    ax.set_ylabel("Виручка, млрд USD")
    ax.set_title("Динаміка глобального ігрового ринку")
    ax.legend()
    ax.grid(alpha=0.3)
    for _, row in df.iterrows():
        ax.annotate(
            f"{row['revenue_bn']:.1f}",
            (row["year"], row["revenue_bn"]),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center",
            fontsize=8,
        )
    path = OUTPUT_DIR / "market_history.png"
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)
    return path


def plot_shares(df: pd.DataFrame, shares: pd.Series, year: int) -> Path:
    fig, ax = plt.subplots(figsize=(7, 7))
    colors = ["#99c24d", "#1f6f8b", "#f18f01"]
    _, _, autotexts = ax.pie(
        shares,
        labels=df["segment"],
        autopct="%1.1f%%",
        colors=colors,
        startangle=90,
        wedgeprops=dict(width=0.45, edgecolor="white"),
    )
    for t in autotexts:
        t.set_fontsize(10)
    ax.set_title(f"Частки сегментів, {year}")
    path = OUTPUT_DIR / f"platform_shares_{year}.png"
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)
    return path


def plot_ua_console(df: pd.DataFrame) -> Path:
    fig, ax = plt.subplots(figsize=(9, 5))
    colors = ["#003791", "#1b2838", "#e60012", "#107c10", "#666666"]
    ax.barh(df["brand"][::-1], df["approx_share_pct"][::-1], color=colors[::-1])
    ax.set_xlabel("Орієнтовна частка, %")
    ax.set_title("Україна: структура продажів консолей (2025)")
    ax.grid(axis="x", alpha=0.3)
    path = OUTPUT_DIR / "ua_console_share.png"
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)
    return path


# ---------------------------------------------------------------------------
# Звіт
# ---------------------------------------------------------------------------

def build_report(
    top10_metrics: dict,
    segment_metrics: dict,
    chart_paths: list[Path],
) -> str:
    f25 = segment_metrics["fastest_2025"]
    f26 = segment_metrics["fastest_2026"]
    largest = segment_metrics["largest_2026"]
    fastest_plat = top10_metrics["fastest"]

    lines = [
        "# Аналіз ігрового ринку",
        "",
        "*Звіт згенеровано скриптом `game_market_analysis.py`.*",
        "",
        "## Розділ 1. Топ 10 ігрових платформ",
        "",
        "Ранжування за **виручкою ігор на платформі/сторфронті у 2025** "
        "(consumer spend на games). Де офіційних даних немає — оцінка "
        "(`confidence=estimate`).",
        "",
        f"- Сума топ-10 (tracked): **${top10_metrics['total_tracked']:.1f}B**",
        f"- Топ-3 (App Store + Google Play + China Android): "
        f"**{top10_metrics['top3_share']:.0f}%** від tracked-суми",
        f"- Mobile у топ-10: **{top10_metrics['mobile_share']:.0f}%** виручки",
        f"- Найшвидший ріст у списку: **{fastest_plat['platform']}** "
        f"(+{fastest_plat['growth_yoy_pct']:.0f}% YoY)",
        f"- High-confidence спостережень: **{top10_metrics['high_confidence_n']}/10**",
        "",
        "| # | Платформа | Категорія | Виручка 2025 | YoY | Аудиторія | Confidence |",
        "|---|-----------|-----------|--------------|-----|-----------|------------|",
    ]

    for _, row in TOP10_PLATFORMS.iterrows():
        rev = f"${row['revenue_2025_bn']:.2f}".rstrip("0").rstrip(".") + "B"
        yoy = f"{row['growth_yoy_pct']:+.1f}%".replace(".0%", "%")
        lines.append(
            f"| {row['rank']} | **{row['platform']}** | {row['category']} | "
            f"{rev} | {yoy} | {row['users_metric']} | {row['confidence']} |"
        )

    lines += [
        "",
        "### Короткі профілі",
        "",
    ]
    for _, row in TOP10_PLATFORMS.iterrows():
        lines.append(
            f"**{row['rank']}. {row['platform']}** ({row['owner']}) — "
            f"{row['note']}. Джерело: {row['source']}."
        )
        lines.append("")

    lines += [
        "### Інсайти розділу 1",
        "",
        "1. **Mobile-сторфронти займають три перші місця** і генерують більшість "
        "tracked-виручки — App Store сам майже дорівнює Google Play + China Android.",
        "2. **PlayStation Network випереджає Steam за digital software revenue** "
        "(~$16B vs $11.7B), але Steam швидше росте (+13%) і домінує на PC.",
        "3. **Xbox тримається на Game Pass** (~$5B підписка + store), не на hardware.",
        "4. **Epic** малий за store spend ($1.16B), але важливий як D2C/free-games "
        "і як Unreal/Epic ecosystem; 78M MAU на PC.",
        "5. **Roblox** — окремий клас UGC-платформи з гігантським MAU (~450M), "
        "який конкурує з «класичними» сторами за увагу гравців.",
        "",
        "![top10_platforms_revenue](output/top10_platforms_revenue.png)",
        "",
        "![top10_by_category](output/top10_by_category.png)",
        "",
        "---",
        "",
        "## Розділ 2. Макроринок (Newzoo)",
        "",
        f"У **2025** глобальний ігровий ринок: **${segment_metrics['total_2025']:.1f}B** "
        f"(+9.1% YoY). Прогноз **2026**: **${segment_metrics['total_2026']:.1f}B** "
        f"(+{segment_metrics['yoy_2026']:.1f}% YoY). "
        f"Домінує **{largest['segment']}** "
        f"(${largest['revenue_2026_bn']:.1f}B).",
        "",
        "| Сегмент | 2025, $B | Ріст 2025 | 2026, $B | Ріст 2026 | Частка 2026 |",
        "|---------|----------|-----------|----------|-----------|-------------|",
    ]

    for i, row in SEGMENT_REVENUE.iterrows():
        lines.append(
            f"| {row['segment']} | {row['revenue_2025_bn']:.1f} | "
            f"+{row['growth_2025_pct']:.1f}% | {row['revenue_2026_bn']:.1f} | "
            f"+{row['growth_2026_pct']:.1f}% | "
            f"{segment_metrics['shares_2026'].iloc[i]:.1f}% |"
        )

    lines += [
        "",
        f"- Найшвидше у 2025: **{f25['segment']}** (+{f25['growth_2025_pct']:.1f}%).",
        f"- Найшвидше у 2026 (прогноз): **{f26['segment']}** (+{f26['growth_2026_pct']:.1f}%).",
        f"- CAGR 2021–2026: **{segment_metrics['cagr_2021_2026']:.1f}%**.",
        "",
        "### Драйвери 2026",
        "",
        "1. **GTA VI** — каталізатор console full-game spending.",
        "2. **Mobile D2C / ARPPU** — зростання через витрати платників.",
        "3. **PC сповільнення** після +12% у 2025 (дорожча пам’ять, висока база).",
        "",
        "---",
        "",
        "## Розділ 3. Монетизація",
        "",
        "| Модель | Орієнтовна частка |",
        "|--------|-------------------|",
    ]
    for _, row in MONETIZATION.iterrows():
        lines.append(f"| {row['model']} | {row['share_pct']:.0f}% |")

    lines += [
        "",
        "Live-service лишається основою виручки; premium/full-game у 2026 "
        "прискорюється завдяки GTA VI (~+17.5% full-game на консолях).",
        "",
        "---",
        "",
        "## Розділ 4. Український контекст",
        "",
        "### Споживчий ринок (DOU / ERC, 2025)",
        "",
        "- Фізичні ігри на дисках: **-14%** YoY.",
        "- Ринок консолей: **+14%** YoY.",
        "- **PlayStation > 85%** продажів консолей; далі Steam Deck, Nintendo, Xbox.",
        "- S.T.A.L.K.E.R. 2 — лідер фізичних продажів у кількох місяцях 2025.",
        "",
        "### Продуктовий геймдев (DOU 2025)",
        "",
        "| Платформа | Студій у топ-20 |",
        "|-----------|-----------------|",
    ]
    for _, row in UA_STUDIO_PLATFORMS.iterrows():
        lines.append(f"| {row['platform']} | {row['studios_in_top20']} |")

    lines += [
        "",
        "- Mobile — головний фокус українських продуктових студій.",
        "- Unity — найпоширеніший рушій (11/20).",
        "- Тренди 2026: AI у продакшні/UA, retention > інсталяції, гібридна монетизація.",
        "",
        "---",
        "",
        "## Розділ 5. Висновки",
        "",
        "1. **Топ-платформи = mobile stores** за виручкою; **Steam/PSN** — якір PC/console.",
        "2. Стратегія релізу: scale → App Store / Google Play / China; premium IP → "
        "PSN + Steam (+ Xbox Game Pass для reach).",
        "3. **2026** — рік console-каталізатора (GTA VI) і AI-пайплайнів у mobile.",
        "4. В Україні — digital-first + PS-домінування; для студій — mobile live-ops + PC mid-core.",
        "",
        "## Усі графіки",
        "",
    ]
    for p in chart_paths:
        lines.append(f"![{p.stem}]({p.as_posix()})")
        lines.append("")

    lines += [
        "## Джерела",
        "",
        "- Sensor Tower / industry reports — App Store $52.5B, Google Play $30B, Steam $11.7B (2025)",
        "- [Sony FY2025 G&NS](https://www.sony.com/en/SonyInfo/IR/library/presen/business_segment_meeting/pdf/2025/GNS_E.pdf) — PSN 124M MAU; digital software ¥2.415T",
        "- [Epic Games Store 2025 Year in Review](https://store.epicgames.com/en-US/news/epic-games-store-2025-year-in-review)",
        "- Nintendo digital software / eShop FY figures (~$2.1–2.6B)",
        "- [Newzoo — $213.9B на 2026](https://www.gamesindustry.biz/newzoo-global-games-market-to-generate-2139bn-in-2026-up-61-yoy)",
        "- [DOU — ринок України 2025](https://gamedev.dou.ua/articles/best-selling-games-in-ukraine-2025/)",
        "",
        "> Примітка: виручка платформ — games consumer spend на сторі/екосистемі. "
        "Не плутати з publisher revenue. Hardware, ads і secondary markets виключені "
        "там, де джерело це дозволяє.",
        "",
    ]
    return "\n".join(lines)


def print_console_summary(top10_metrics: dict, segment_metrics: dict) -> None:
    print("=" * 68)
    print(" АНАЛІЗ ІГРОВОГО РИНКУ")
    print("=" * 68)
    print("\nРозділ 1. Топ 10 ігрових платформ (виручка 2025):")
    for _, row in TOP10_PLATFORMS.iterrows():
        mark = "" if row["confidence"] == "high" else ("≈" if row["confidence"] == "medium" else "*")
        print(
            f"  {row['rank']:>2}. {row['platform']:<28} "
            f"${row['revenue_2025_bn']:>5.1f}B{mark}  [{row['category']}]"
        )
    print(
        f"\n  Tracked сума: ${top10_metrics['total_tracked']:.1f}B | "
        f"Mobile частка: {top10_metrics['mobile_share']:.0f}% | "
        f"Топ-3: {top10_metrics['top3_share']:.0f}%"
    )
    print(
        f"\nМакроринок: ${segment_metrics['total_2025']:.1f}B (2025) → "
        f"${segment_metrics['total_2026']:.1f}B (2026, +{segment_metrics['yoy_2026']:.1f}%)"
    )
    print("=" * 68)


def main() -> None:
    ensure_output_dir()
    top10_metrics = compute_top10_metrics(TOP10_PLATFORMS)
    segment_metrics = compute_segment_metrics(SEGMENT_REVENUE)

    charts = [
        plot_top10_revenue(TOP10_PLATFORMS),
        plot_top10_by_category(TOP10_PLATFORMS),
        plot_market_history(MARKET_HISTORY),
        plot_segment_revenue(SEGMENT_REVENUE),
        plot_shares(SEGMENT_REVENUE, segment_metrics["shares_2025"], 2025),
        plot_shares(SEGMENT_REVENUE, segment_metrics["shares_2026"], 2026),
        plot_ua_console(UA_CONSOLE_SHARE),
    ]

    report = build_report(top10_metrics, segment_metrics, charts)
    REPORT_PATH.write_text(report, encoding="utf-8")

    TOP10_PLATFORMS.to_csv(OUTPUT_DIR / "top10_platforms.csv", index=False)
    SEGMENT_REVENUE.to_csv(OUTPUT_DIR / "platform_revenue.csv", index=False)
    MARKET_HISTORY.to_csv(OUTPUT_DIR / "market_history.csv", index=False)

    print_console_summary(top10_metrics, segment_metrics)
    print(f"\nЗвіт:    {REPORT_PATH}")
    print(f"Графіки: {OUTPUT_DIR}/")
    for p in charts:
        print(f"  - {p}")


if __name__ == "__main__":
    main()
