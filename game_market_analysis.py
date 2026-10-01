#!/usr/bin/env python3
"""
Аналіз ігрового ринку (глобальний + Україна)
============================================
Джерела:
  - Newzoo Global Games Market Report (2025 факт / 2026 прогноз)
  - DOU GameDev (фізичні продажі та геймдев України, 2025)

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
# 1. Дані (млрд USD, споживчі витрати на ігрове ПЗ; без hardware / ads)
# ---------------------------------------------------------------------------

PLATFORM_REVENUE = pd.DataFrame(
    {
        "platform": ["Mobile", "Console", "PC"],
        "revenue_2025_bn": [113.3, 44.7, 43.6],
        "growth_2025_pct": [10.7, 2.8, 12.0],
        "revenue_2026_bn": [121.1, 46.9, 45.9],
        "growth_2026_pct": [6.8, 5.1, 5.3],
    }
)

# Історична динаміка загального ринку (орієнтовні значення Newzoo / публічні оцінки)
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

# Структура монетизації (орієнтовні частки ринку 2026)
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

# Україна: фізичні носії та консолі (DOU / ERC, 2025)
UA_PHYSICAL = pd.DataFrame(
    {
        "metric": [
            "Продажі ігор на дисках YoY",
            "Продажі консолей YoY",
            "Частка PlayStation серед консолей",
        ],
        "value_pct": [-14.0, 14.0, 85.0],
    }
)

UA_CONSOLE_SHARE = pd.DataFrame(
    {
        "brand": ["PlayStation", "Steam Deck", "Nintendo", "Xbox", "Інше (Lenovo тощо)"],
        "rank": [1, 2, 3, 4, 5],
        "approx_share_pct": [85.0, 6.0, 4.5, 3.0, 1.5],
    }
)

# Топ-напрямки українського продуктового геймдеву (DOU 2025, з 20 студій)
UA_STUDIO_PLATFORMS = pd.DataFrame(
    {
        "platform": ["Mobile", "PC", "Console / multi"],
        "studios_in_top20": [14, 12, 4],
    }
)


def ensure_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def compute_metrics(df: pd.DataFrame) -> dict:
    """Ключові метрики глобального ринку."""
    total_2025 = float(df["revenue_2025_bn"].sum())
    total_2026 = float(df["revenue_2026_bn"].sum())
    yoy_2026 = (total_2026 / total_2025 - 1.0) * 100.0

    shares_2025 = df["revenue_2025_bn"] / total_2025 * 100.0
    shares_2026 = df["revenue_2026_bn"] / total_2026 * 100.0

    fastest_2025 = df.loc[df["growth_2025_pct"].idxmax()]
    fastest_2026 = df.loc[df["growth_2026_pct"].idxmax()]
    largest_2026 = df.loc[df["revenue_2026_bn"].idxmax()]

    # CAGR 2021→2026 з історії ринку
    hist = MARKET_HISTORY.set_index("year")["revenue_bn"]
    years = hist.index.max() - hist.index.min()
    cagr = (hist.iloc[-1] / hist.iloc[0]) ** (1 / years) - 1

    return {
        "total_2025": total_2025,
        "total_2026": total_2026,
        "yoy_2026": yoy_2026,
        "shares_2025": shares_2025,
        "shares_2026": shares_2026,
        "fastest_2025": fastest_2025,
        "fastest_2026": fastest_2026,
        "largest_2026": largest_2026,
        "cagr_2021_2026": cagr * 100.0,
    }


def plot_platform_revenue(df: pd.DataFrame) -> Path:
    """Порівняння виручки платформ 2025 vs 2026."""
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
    ax.set_title("Глобальний ігровий ринок за платформами")
    ax.set_xticks(x)
    ax.set_xticklabels(df["platform"])
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
    """Динаміка загальної виручки ринку."""
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
    """Кругова діаграма часток платформ."""
    fig, ax = plt.subplots(figsize=(7, 7))
    colors = ["#99c24d", "#1f6f8b", "#f18f01"]
    wedges, texts, autotexts = ax.pie(
        shares,
        labels=df["platform"],
        autopct="%1.1f%%",
        colors=colors,
        startangle=90,
        wedgeprops=dict(width=0.45, edgecolor="white"),
    )
    for t in autotexts:
        t.set_fontsize(10)
    ax.set_title(f"Частки платформ, {year}")
    path = OUTPUT_DIR / f"platform_shares_{year}.png"
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)
    return path


def plot_ua_console(df: pd.DataFrame) -> Path:
    """Частки консолей в Україні (орієнтовно)."""
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


def build_report(metrics: dict, chart_paths: list[Path]) -> str:
    f25 = metrics["fastest_2025"]
    f26 = metrics["fastest_2026"]
    largest = metrics["largest_2026"]

    lines = [
        "# Аналіз ігрового ринку",
        "",
        "*Звіт згенеровано скриптом `game_market_analysis.py`.*",
        "",
        "## 1. Короткий вердикт",
        "",
        f"У **2025** глобальний ігровий ринок вперше перевищив **$200 млрд** "
        f"(факт Newzoo: **${metrics['total_2025']:.1f}B**, +9.1% YoY). "
        f"Прогноз на **2026** — **${metrics['total_2026']:.1f}B** "
        f"(+{metrics['yoy_2026']:.1f}% YoY). "
        f"Домінує **{largest['platform']}** "
        f"(${largest['revenue_2026_bn']:.1f}B, ~{metrics['shares_2026'].iloc[largest.name]:.0f}% ринку).",
        "",
        "## 2. Глобальний ринок за платформами",
        "",
        "| Платформа | 2025, $B | Ріст 2025 | 2026, $B | Ріст 2026 | Частка 2026 |",
        "|-----------|----------|-----------|----------|-----------|-------------|",
    ]

    for i, row in PLATFORM_REVENUE.iterrows():
        lines.append(
            f"| {row['platform']} | {row['revenue_2025_bn']:.1f} | "
            f"+{row['growth_2025_pct']:.1f}% | {row['revenue_2026_bn']:.1f} | "
            f"+{row['growth_2026_pct']:.1f}% | {metrics['shares_2026'].iloc[i]:.1f}% |"
        )

    lines += [
        "",
        f"- Найшвидше зростав у 2025: **{f25['platform']}** (+{f25['growth_2025_pct']:.1f}%).",
        f"- Найшвидше зросте у 2026 (прогноз): **{f26['platform']}** (+{f26['growth_2026_pct']:.1f}%).",
        f"- CAGR ринку 2021–2026: **{metrics['cagr_2021_2026']:.1f}%** на рік.",
        "",
        "### Ключові драйвери 2026",
        "",
        "1. **GTA VI (листопад 2026)** — головний каталізатор консольного сегмента; "
        "без нього Newzoo очікував би падіння console YoY.",
        "2. **Mobile D2C і ARPPU** — частка mobile ~57%; зростання через вищі витрати "
        "платників та direct-to-consumer канали.",
        "3. **PC сповільнюється** після рекордних +12% у 2025 (до ~+5.3%) через "
        "дорожчу пам’ять / hardware і високу базу порівняння.",
        "",
        "## 3. Монетизація",
        "",
        "| Модель | Орієнтовна частка |",
        "|--------|-------------------|",
    ]
    for _, row in MONETIZATION.iterrows():
        lines.append(f"| {row['model']} | {row['share_pct']:.0f}% |")

    lines += [
        "",
        "Premium / full-game у 2026 показує найсильніше зростання бізнес-моделей "
        "(~+17.5% у full-game spending на консолях) завдяки GTA VI. "
        "Live-service залишається основою виручки, але темпи росту стриманіші.",
        "",
        "## 4. Український контекст",
        "",
        "### Споживчий ринок (DOU / ERC, 2025)",
        "",
        "- Фізичні ігри на дисках: **-14%** YoY (падіння сповільнилось із -37% у 2024).",
        "- Ринок консолей: **+14%** YoY.",
        "- **PlayStation > 85%** продажів консолей; далі Steam Deck, Nintendo, Xbox.",
        "- S.T.A.L.K.E.R. 2 — лідер фізичних продажів (PS5 / PC) у кількох місяцях 2025.",
        "",
        "### Продуктовий геймдев (DOU рейтинг 2025)",
        "",
        "| Платформа | Студій у топ-20 |",
        "|-----------|-----------------|",
    ]
    for _, row in UA_STUDIO_PLATFORMS.iterrows():
        lines.append(f"| {row['platform']} | {row['studios_in_top20']} |")

    lines += [
        "",
        "- Mobile лишається головним фокусом українських продуктових студій.",
        "- Unity — найпоширеніший рушій (11/20 компаній).",
        "- Тренди 2026 для UA-студій: AI у продакшні/UA, retention замість "
        "інсталяцій, гібридна монетизація, miltech / інді-хвиля.",
        "",
        "## 5. Висновки та можливості",
        "",
        "1. **Mobile = обсяг**, **PC/Console = маржа і cultural hits**. "
        "Стратегія залежить від того, чи потрібен scale (mobile F2P) чи premium IP.",
        "2. **2026 — рік консольного каталізатора (GTA VI)**; ризик концентрації "
        "на одному релізі високий.",
        "3. В Україні **цифровий і консольний попит росте**, фізика скорочується — "
        "дистрибуція має бути digital-first.",
        "4. Для локальних студій виграшна ніша: mobile live-ops + PC mid-core, "
        "з сильним retention і AI-прискореним контент-пайплайном.",
        "",
        "## 6. Графіки",
        "",
    ]
    for p in chart_paths:
        lines.append(f"![{p.stem}]({p.as_posix()})")
        lines.append("")

    lines += [
        "## Джерела",
        "",
        "- [Newzoo / GamesIndustry.biz — прогноз $213.9B на 2026](https://www.gamesindustry.biz/newzoo-global-games-market-to-generate-2139bn-in-2026-up-61-yoy)",
        "- [GamesBeat — $201.6B у 2025](https://gamesbeat.com/global-games-revenue-breached-200b-in-2025-newzoo/)",
        "- [DOU — ігри на дисках і консолі в Україні 2025](https://gamedev.dou.ua/articles/best-selling-games-in-ukraine-2025/)",
        "- [DOU — рейтинг продуктового геймдеву 2025](https://gamedev.dou.ua/articles/product-gamedev-rating-2025/)",
        "- [DOU — підсумки українського геймдеву 2025](https://gamedev.dou.ua/articles/ukranian-gamedev-summary-2025/)",
        "",
        "> Примітка: цифри Newzoo — consumer spending на ігрове ПЗ "
        "(без hardware, advertising, податків і secondary markets).",
        "",
    ]
    return "\n".join(lines)


def print_console_summary(metrics: dict) -> None:
    print("=" * 64)
    print(" АНАЛІЗ ІГРОВОГО РИНКУ")
    print("=" * 64)
    print(f"\nГлобальна виручка 2025: ${metrics['total_2025']:.1f}B")
    print(
        f"Прогноз 2026:          ${metrics['total_2026']:.1f}B "
        f"(+{metrics['yoy_2026']:.1f}% YoY)"
    )
    print(f"CAGR 2021–2026:        {metrics['cagr_2021_2026']:.1f}%")
    print("\nПлатформи (2025 → 2026):")
    for i, row in PLATFORM_REVENUE.iterrows():
        print(
            f"  {row['platform']:<8} "
            f"${row['revenue_2025_bn']:>5.1f}B → ${row['revenue_2026_bn']:>5.1f}B "
            f"| частка 2026: {metrics['shares_2026'].iloc[i]:5.1f}%"
        )
    print("\nУкраїна 2025:")
    print("  Диски:     -14% YoY")
    print("  Консолі:   +14% YoY (PlayStation > 85%)")
    print("  Геймдев:   Mobile лідирує серед продуктових студій")
    print("=" * 64)


def main() -> None:
    ensure_output_dir()
    metrics = compute_metrics(PLATFORM_REVENUE)

    charts = [
        plot_market_history(MARKET_HISTORY),
        plot_platform_revenue(PLATFORM_REVENUE),
        plot_shares(PLATFORM_REVENUE, metrics["shares_2025"], 2025),
        plot_shares(PLATFORM_REVENUE, metrics["shares_2026"], 2026),
        plot_ua_console(UA_CONSOLE_SHARE),
    ]

    report = build_report(metrics, charts)
    REPORT_PATH.write_text(report, encoding="utf-8")

    # CSV для подальшої роботи
    PLATFORM_REVENUE.to_csv(OUTPUT_DIR / "platform_revenue.csv", index=False)
    MARKET_HISTORY.to_csv(OUTPUT_DIR / "market_history.csv", index=False)

    print_console_summary(metrics)
    print(f"\nЗвіт:    {REPORT_PATH}")
    print(f"Графіки: {OUTPUT_DIR}/")
    for p in charts:
        print(f"  - {p}")


if __name__ == "__main__":
    main()
