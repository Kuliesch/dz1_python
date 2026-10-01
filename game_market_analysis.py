#!/usr/bin/env python3
"""
Топ-20 B2B iGaming платформ і агрегаторів
=========================================
Список на кшталт Softswiss, Slotegrator — casino platform / game aggregator.
Усе виводиться в таблицю (CSV + Markdown).

Запуск:
  python game_market_analysis.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

OUTPUT_DIR = Path("output")
REPORT_PATH = Path("GAME_MARKET_REPORT.md")
CSV_PATH = OUTPUT_DIR / "top20_platforms.csv"

# Топ-20: turnkey-платформи + game aggregators (B2B для операторів казино)
TOP20 = pd.DataFrame(
    [
        {
            "№": 1,
            "Платформа": "SOFTSWISS",
            "Тип": "Platform + Aggregator",
            "Сайт": "https://www.softswiss.com",
            "Ігри / студії": "40,000+ / 300+",
            "Фокус": "Crypto + turnkey casino",
            "Опис": (
                "Повна casino-платформа (PAM, бонуси, платежі) + Game Aggregator. "
                "Сильна в crypto з 2013, швидкий запуск (~1 міс.), є sportsbook і Affilka. "
                "Один із лідерів ринку за нагородами Best Platform 2025–2026."
            ),
        },
        {
            "№": 2,
            "Платформа": "Slotegrator",
            "Тип": "Aggregator + Turnkey",
            "Сайт": "https://slotegrator.pro",
            "Ігри / студії": "40,000+ / 180+",
            "Фокус": "Швидкий запуск, emerging markets",
            "Опис": (
                "APIgrator — єдиний API для контенту; також turnkey/white-label, "
                "Sportegrator, Moneygrator, Partnergrator. Популярний у SMB і CIS/LatAm/Africa. "
                "Запуск часто 30–45 днів, допомога з ліцензіями (Anjouan, Curacao тощо)."
            ),
        },
        {
            "№": 3,
            "Платформа": "EveryMatrix",
            "Тип": "Platform + Aggregator",
            "Сайт": "https://everymatrix.com",
            "Ігри / студії": "45,000+ / 355+",
            "Фокус": "Регульовані ринки (UK, US, EU)",
            "Опис": (
                "Модульний стек: CasinoEngine, SlotMatrix (aggregator), OddsMatrix (sports), "
                "GamMatrix (PAM), MoneyMatrix (payments), PartnerMatrix. "
                "Найглибший каталог серед built-in агрегаторів; сильний compliance footprint."
            ),
        },
        {
            "№": 4,
            "Платформа": "SoftGamings",
            "Тип": "Turnkey + Aggregator",
            "Сайт": "https://www.softgamings.com",
            "Ігри / студії": "16,000+ / —",
            "Фокус": "White-label casino",
            "Опис": (
                "Довгограючий white-label/turnkey вендор (з 2007). "
                "Агрегація ігор + платежі + sportsbook-фіди; підходить для classic, crypto і hybrid казино. "
                "Один контракт на платформу й контент."
            ),
        },
        {
            "№": 5,
            "Платформа": "BetConstruct",
            "Тип": "Multi-vertical Platform",
            "Сайт": "https://www.betconstruct.com",
            "Ігри / студії": "6,500+ / —",
            "Фокус": "Sportsbook + casino + retail",
            "Опис": (
                "SpringBME — широка платформа: sportsbook, casino, poker, skill games, "
                "live studios, retail. Один вендор на весь продукт; популярний у emerging markets "
                "і серед операторів, яким потрібен betting-led стек."
            ),
        },
        {
            "№": 6,
            "Платформа": "Hub88",
            "Тип": "Standalone Aggregator",
            "Сайт": "https://hub88.io",
            "Ігри / студії": "26,000+ / 200+",
            "Фокус": "Crypto / offshore content",
            "Опис": (
                "Незалежний aggregator з публічною API-документацією. "
                "Ексклюзивний контент-партнер Stake.com; сильний seamless/transfer wallet, "
                "HubWallet settlement. Ідеальний для crypto-first операторів."
            ),
        },
        {
            "№": 7,
            "Платформа": "Pariplay Fusion",
            "Тип": "Standalone Aggregator",
            "Сайт": "https://pariplaygames.com",
            "Ігри / студії": "14,000+ / 150+",
            "Фокус": "UK / US / regulated EU",
            "Опис": (
                "Агрегатор Aristocrat Interactive з глибоким ліцензійним покриттям "
                "(UK, Malta, Gibraltar, кілька штатів США). Турніри/промо крос-вендорно; "
                "сильний вибір для регульованих юрисдикцій."
            ),
        },
        {
            "№": 8,
            "Платформа": "Relax Gaming",
            "Тип": "Aggregator + Studio",
            "Сайт": "https://www.relax-gaming.com",
            "Ігри / студії": "4,000+ / 70+",
            "Фокус": "Curated content, regulated",
            "Опис": (
                "Гібрид: власна студія + агрегація (Silver Bullet / Powered By Relax). "
                "Менший, але відібраний каталог; Dream Drop network jackpot. "
                "Сильний у UK/EU/Ontario/US; частина групи FDJ United."
            ),
        },
        {
            "№": 9,
            "Платформа": "Alea",
            "Тип": "Standalone Aggregator",
            "Сайт": "https://alea.com",
            "Ігри / студії": "16,000+ / 250+",
            "Фокус": "Brazil / LatAm / MGA",
            "Опис": (
                "Чистий B2B-агрегатор (колишній ALEA Play). MGA B2B ліцензія, "
                "сильна позиція в Бразилії з day-one regulation. "
                "Часто без мінімальних fees; зручний для mid-size операторів."
            ),
        },
        {
            "№": 10,
            "Платформа": "Bragg Gaming",
            "Тип": "Aggregator + PAM",
            "Сайт": "https://bragg.group",
            "Ігри / студії": "15,000+ / 120+",
            "Фокус": "US / Canada / regulated",
            "Опис": (
                "Hub-агрегація + proprietary content + опційний PAM (Fuze). "
                "Клієнти рівня Caesars, BetMGM, DraftKings, bet365. "
                "Підходить, коли потрібні ліцензований pipe і exclusive titles."
            ),
        },
        {
            "№": 11,
            "Платформа": "NuxGame",
            "Тип": "Turnkey + Aggregator",
            "Сайт": "https://nuxgame.com",
            "Ігри / студії": "17,500+ / 140+",
            "Фокус": "Crypto turnkey",
            "Опис": (
                "API-first turnkey для crypto/offshore: 25+ монет, Web3-гаманці (MetaMask тощо). "
                "Агрегація + платежі + affiliate. Швидкий шлях для crypto-казино з одним вендором."
            ),
        },
        {
            "№": 12,
            "Платформа": "Digitain",
            "Тип": "Platform + Sportsbook",
            "Сайт": "https://digitain.com",
            "Ігри / студії": "широкий каталог / 100+",
            "Фокус": "Sportsbook + casino stack",
            "Опис": (
                "Повний iGaming-стек: sportsbook, casino aggregation, payments, back office, "
                "live casino. Сильний у betting-операторів CIS/Asia/LatAm; "
                "turnkey і API-інтеграції."
            ),
        },
        {
            "№": 13,
            "Платформа": "Pragmatic Solutions",
            "Тип": "PAM / Full Platform",
            "Сайт": "https://pragmatic.solutions",
            "Ігри / студії": "через інтеграції провайдерів",
            "Фокус": "Enterprise PAM, regulated",
            "Опис": (
                "Enterprise Player Account Management і full-service platform. "
                "Орієнтований на масштабовані регульовані операції; "
                "часто обирають поруч із контентом Pragmatic Play / tier-1 студій."
            ),
        },
        {
            "№": 14,
            "Платформа": "St8",
            "Тип": "Standalone Aggregator",
            "Сайт": "https://st8.io",
            "Ігри / студії": "19,000+ / 200+",
            "Фокус": "Engineering-led API",
            "Опис": (
                "Сучасний aggregator з публічними API docs, Bonus API, jackpot tools, "
                "CI-тестуванням (TARS). Ліцензії UKGC/SGA/AGCO — для tech-команд, "
                "які хочуть self-serve інтеграцію, а не vendor-managed onboarding."
            ),
        },
        {
            "№": 15,
            "Платформа": "GR8 Tech",
            "Тип": "Platform + Aggregator",
            "Сайт": "https://gr8.tech",
            "Ігри / студії": "casino aggregation module",
            "Фокус": "Sportsbook-first + casino",
            "Опис": (
                "Sportsbook-led платформа з окремим casino aggregation модулем (GR8 Casino). "
                "Підходить betting-операторам, яким потрібен сильний sports core "
                "і контент казино в одному стеку."
            ),
        },
        {
            "№": 16,
            "Платформа": "White Hat Gaming",
            "Тип": "PAM + Aggregator",
            "Сайт": "https://www.whitehat-gaming.com",
            "Ігри / студії": "3,000+ / 130+",
            "Фокус": "UK / Malta / Ontario / US",
            "Опис": (
                "Регульований PAM + wallet + aggregation + payments + engagement. "
                "Менший каталог, але глибока сертифікація для tier-1 юрисдикцій. "
                "Орієнтир — compliance, не «найбільше ігор»."
            ),
        },
        {
            "№": 17,
            "Платформа": "Light & Wonder OpenGaming",
            "Тип": "RGS / Aggregation Network",
            "Сайт": "https://www.lnw.com",
            "Ігри / студії": "6,500+ / 60+",
            "Фокус": "US / UK / Ontario regulated",
            "Опис": (
                "OpenGaming Platform — мережа L&W + third-party studios через RGS. "
                "Власні хіти (напр. Huff N' Puff тощо) + live в регульованих ринках. "
                "Вибір, коли важливі сертифікації, а не максимальний volume каталогу."
            ),
        },
        {
            "№": 18,
            "Платформа": "IGT PlayDigital",
            "Тип": "RGS + Aggregation",
            "Сайт": "https://www.igt.com",
            "Ігри / студії": "10,000+ / 120+",
            "Фокус": "US / UK regulated",
            "Опис": (
                "PlayRGS + third-party aggregation для операторів, які вже беруть IGT-контент. "
                "Покриття всіх US iGaming штатів; engagement/retention tools у пакеті. "
                "Enterprise-рівень для North America."
            ),
        },
        {
            "№": 19,
            "Платформа": "REEVO",
            "Тип": "Aggregator + Studio",
            "Сайт": "https://reevo.com",
            "Ігри / студії": "20,000+ / 100+",
            "Фокус": "EU / LatAm, hybrid content",
            "Опис": (
                "Власна slot-студія (~100 titles) + великий third-party каталог через один API. "
                "MGA B2B; зростає в Southern Europe і LatAm. "
                "Зручно, коли потрібні і exclusive in-house, і volume aggregation."
            ),
        },
        {
            "№": 20,
            "Платформа": "LuckyStreak",
            "Тип": "Live + Aggregator",
            "Сайт": "https://www.luckystreak.com",
            "Ігри / студії": "6,000+ / —",
            "Фокус": "Live dealer + aggregation",
            "Опис": (
                "Live-студія в Ризі + LuckyConnect aggregation API. "
                "Один seamless wallet на власні live-столи і third-party slots/crash. "
                "Підходить offshore / sweeps операторам, яким важливий live-продукт."
            ),
        },
    ]
)


def ensure_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def dataframe_to_markdown_table(df: pd.DataFrame) -> str:
    """Проста markdown-таблиця без залежності від tabulate."""
    cols = list(df.columns)
    header = "| " + " | ".join(cols) + " |"
    sep = "| " + " | ".join("---" for _ in cols) + " |"
    rows = []
    for _, row in df.iterrows():
        cells = [str(row[c]).replace("|", "\\|").replace("\n", " ") for c in cols]
        rows.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, sep, *rows])


def build_report(df: pd.DataFrame) -> str:
    # Коротка таблиця без довгого опису — зручно сканувати
    summary = df[["№", "Платформа", "Тип", "Ігри / студії", "Фокус", "Сайт"]].copy()
    # Повна таблиця з описом
    full = df[["№", "Платформа", "Тип", "Фокус", "Ігри / студії", "Опис", "Сайт"]].copy()

    lines = [
        "# Топ-20 B2B iGaming платформ і агрегаторів",
        "",
        "Список платформ типу **Softswiss**, **Slotegrator** — "
        "casino platform / game aggregator для запуску або наповнення онлайн-казино.",
        "",
        "## Коротка таблиця",
        "",
        dataframe_to_markdown_table(summary),
        "",
        "## Повна таблиця з описами",
        "",
        dataframe_to_markdown_table(full),
        "",
        "## Легенда типів",
        "",
        "| Тип | Що означає |",
        "|-----|------------|",
        "| Platform + Aggregator | Повний стек казино + модуль агрегації ігор |",
        "| Aggregator + Turnkey | Акцент на API контенту + пакети white-label/turnkey |",
        "| Standalone Aggregator | Незалежний content hub (підключається до вашого PAM) |",
        "| Multi-vertical Platform | Casino + sportsbook + інші вертикалі в одному продукті |",
        "| PAM / Full Platform | Player Account Management і операційний backend |",
        "| RGS / Aggregation Network | Remote Game Server + мережа студій (часто regulated) |",
        "",
        "## Примітки",
        "",
        "- Порядок — орієнтовний shortlist ринку (видимість, покриття, зрілість), "
        "не офіційний рейтинг за виручкою: більшість B2B не публікує rate card / GGR.",
        "- Цифри ігор/студій — заявлені вендорами / галузеві огляди 2025–2026; "
        "у каталозі можуть дублюватися title’и між студіями.",
        "- Перед вибором перевіряйте ліцензії під конкретні юрисдикції (UKGC, MGA, US states, Brazil тощо).",
        "",
        "## Джерела",
        "",
        "- [Partnerkin — 20 Casino Game Aggregators](https://partnerkin.com/en/b2b/casino-games-aggregators/)",
        "- [Track360 — SoftSwiss vs EveryMatrix vs Slotegrator](https://track360.io/blog/softswiss-vs-everymatrix-vs-slotegrator-operator-comparison-2026)",
        "- Сайти вендорів: Softswiss, Slotegrator, EveryMatrix, Hub88, Alea, Relax Gaming тощо",
        "",
        f"CSV: `{CSV_PATH.as_posix()}`",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    ensure_output_dir()
    # Прибрати старі артефакти іншого формату звіту
    for stale in OUTPUT_DIR.glob("*"):
        if stale.is_file():
            stale.unlink()

    TOP20.to_csv(CSV_PATH, index=False, encoding="utf-8")
    report = build_report(TOP20)
    REPORT_PATH.write_text(report, encoding="utf-8")

    print("=" * 72)
    print(" ТОП-20 B2B iGaming ПЛАТФОРМ / АГРЕГАТОРІВ")
    print("=" * 72)
    print(
        TOP20[["№", "Платформа", "Тип", "Фокус"]]
        .to_string(index=False)
    )
    print("=" * 72)
    print(f"\nТаблиця (MD):  {REPORT_PATH}")
    print(f"Таблиця (CSV): {CSV_PATH}")


if __name__ == "__main__":
    main()
