#!/usr/bin/env python3
"""
Топ-20 casino platforms (B2B)
=============================
Тільки платформи для запуску онлайн-казино (turnkey / white-label / PAM).
Без окремих game aggregators (Hub88, Alea, Pariplay тощо).

Приклади категорії: Softswiss, Slotegrator.

Запуск:
  python game_market_analysis.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

OUTPUT_DIR = Path("output")
REPORT_PATH = Path("GAME_MARKET_REPORT.md")
CSV_PATH = OUTPUT_DIR / "top20_platforms.csv"

# Критерій включення: продукт = casino / iGaming platform
# (PAM, wallet, back office, frontend, бонуси, платежі, запуск бренду).
# НЕ включаємо чисті content aggregators.

TOP20 = pd.DataFrame(
    [
        {
            "№": 1,
            "Платформа": "SOFTSWISS",
            "Модель": "Turnkey / Crypto",
            "Фокус": "Casino platform, crypto-ready",
            "Опис": (
                "Повноцінна casino platform: PAM, бонус-движок, платежі, бекофіс, "
                "фронтенд. Fiat і crypto, запуск орієнтовно від ~1 місяця. "
                "Один із найвідоміших platform providers на ринку."
            ),
            "Сайт": "https://www.softswiss.com",
        },
        {
            "№": 2,
            "Платформа": "Slotegrator",
            "Модель": "White-label / Turnkey",
            "Фокус": "Швидкий запуск бренду",
            "Опис": (
                "Платформа з Casino Builder, бекофісом і пакетами white-label/turnkey. "
                "Орієнтована на швидкий go-live (часто 30–45 днів) і mid-market операторів. "
                "Є модулі payments, sportsbook, affiliate в рамках платформенного стеку."
            ),
            "Сайт": "https://slotegrator.pro",
        },
        {
            "№": 3,
            "Платформа": "EveryMatrix",
            "Модель": "Turnkey / Modular",
            "Фокус": "Регульовані ринки (UK, EU, US)",
            "Опис": (
                "Модульна iGaming platform: PAM (GamMatrix), casino, sportsbook, "
                "payments, engagement. Підходить для ліцензованих юрисдикцій "
                "і операторів, яким потрібен повний стек під compliance."
            ),
            "Сайт": "https://everymatrix.com",
        },
        {
            "№": 4,
            "Платформа": "SoftGamings",
            "Модель": "White-label / Turnkey",
            "Фокус": "All-in-one casino launch",
            "Опис": (
                "Класичний white-label/turnkey вендор: платформа, платежі, "
                "ліцензійна підтримка, запуск бренду за тижні. "
                "Працює з fiat, crypto і hybrid-моделями."
            ),
            "Сайт": "https://www.softgamings.com",
        },
        {
            "№": 5,
            "Платформа": "BetConstruct",
            "Модель": "Turnkey / White-label",
            "Фокус": "Casino + sportsbook + retail",
            "Опис": (
                "Multi-vertical platform (SpringBME): онлайн-казино, sportsbook, "
                "poker, virtuals, retail. Один постачальник на широкий продукт "
                "і бекофіс."
            ),
            "Сайт": "https://www.betconstruct.com",
        },
        {
            "№": 6,
            "Платформа": "NuxGame",
            "Модель": "Turnkey / White-label",
            "Фокус": "Crypto і швидкий launch",
            "Опис": (
                "iGaming platform для casino/sportsbook з акцентом на crypto "
                "і короткий time-to-market. PAM, бонуси, платежі, white-label пакети."
            ),
            "Сайт": "https://nuxgame.com",
        },
        {
            "№": 7,
            "Платформа": "Digitain",
            "Модель": "Turnkey / White-label",
            "Фокус": "Sportsbook-led platform",
            "Опис": (
                "Повний стек: sportsbook + casino platform, payments, back office, "
                "agent systems. Сильна сторона — betting-оператори, яким потрібен "
                "casino модуль у тому ж продукті."
            ),
            "Сайт": "https://digitain.com",
        },
        {
            "№": 8,
            "Платформа": "GR8 Tech",
            "Модель": "Turnkey",
            "Фокус": "Sportsbook + casino platform",
            "Опис": (
                "Платформа з сильним sportsbook-ядром і casino-модулем, "
                "бекофісом і інструментами для запуску бренду. "
                "Часто розглядають як альтернативу великим EU-вендорам."
            ),
            "Сайт": "https://gr8.tech",
        },
        {
            "№": 9,
            "Платформа": "Pragmatic Solutions",
            "Модель": "PAM / Full platform",
            "Фокус": "Enterprise PAM, regulated",
            "Опис": (
                "Enterprise platform / PAM для масштабованих операторів: "
                "акаунти гравців, multi-brand, інтеграції, операційний бекофіс. "
                "Орієнтир — регульовані та high-volume проєкти."
            ),
            "Сайт": "https://pragmatic.solutions",
        },
        {
            "№": 10,
            "Платформа": "White Hat Gaming",
            "Модель": "PAM / Turnkey",
            "Фокус": "UK, Malta, Ontario, US",
            "Опис": (
                "Регульована platform/PAM з wallet, бонусами, платежами "
                "та інструментами engagement. Акцент на compliance у tier-1 ринках, "
                "а не на «найдешевшому» white-label."
            ),
            "Сайт": "https://www.whitehat-gaming.com",
        },
        {
            "№": 11,
            "Платформа": "Gamingtec",
            "Модель": "Turnkey / White-label",
            "Фокус": "Casino + sportsbook modular",
            "Опис": (
                "Модульна платформа: casino, sportsbook, affiliate, agent system. "
                "Turnkey або white-label запуск із готовим фронтом і бекофісом."
            ),
            "Сайт": "https://gamingtec.com",
        },
        {
            "№": 12,
            "Платформа": "GammaStack",
            "Модель": "Turnkey / Custom",
            "Фокус": "Кастом і turnkey збірка",
            "Опис": (
                "Software house / platform provider: white-label, turnkey і "
                "custom iGaming platforms (casino, sportsbook, sweepstakes). "
                "Підходить, коли потрібна глибша кастомізація."
            ),
            "Сайт": "https://www.gammastack.com",
        },
        {
            "№": 13,
            "Платформа": "Gamingsoft",
            "Модель": "White-label / Turnkey",
            "Фокус": "Asia-oriented launch",
            "Опис": (
                "GSGlobal white-label/turnkey platform для швидкого запуску "
                "casino/sportsbook. Сильна локалізація під азійські ринки "
                "(платежі, мови, UI)."
            ),
            "Сайт": "https://www.gamingsoft.com",
        },
        {
            "№": 14,
            "Платформа": "Uplatform",
            "Модель": "Turnkey",
            "Фокус": "Full-stack casino platform",
            "Опис": (
                "Turnkey iGaming platform з повним операційним стеком "
                "для запуску та ведення онлайн-казино. "
                "Часто фігурує в shortlist поряд із Softswiss / NuxGame."
            ),
            "Сайт": "https://www.uplatform.com",
        },
        {
            "№": 15,
            "Платформа": "Trueigtech",
            "Модель": "Turnkey",
            "Фокус": "Швидкий turnkey запуск",
            "Опис": (
                "Turnkey casino/sportsbook platform provider. "
                "Позиціонується як готовий стек для операторів, "
                "яким потрібен запуск бренду без власної розробки з нуля."
            ),
            "Сайт": "https://trueigtech.com",
        },
        {
            "№": 16,
            "Платформа": "Atlaslive",
            "Модель": "Turnkey",
            "Фокус": "Casino + sportsbook, 4–5 тижнів",
            "Опис": (
                "Turnkey iGaming infrastructure: casino, live, sportsbook, "
                "payments, CRM/CMS, risk. Заявлене вікно запуску ~4–5 тижнів "
                "для ліцензованих операторів."
            ),
            "Сайт": "https://atlaslive.tech",
        },
        {
            "№": 17,
            "Платформа": "Amelco",
            "Модель": "Platform / API",
            "Фокус": "Betting & gaming platform",
            "Опис": (
                "Технологічна platform для betting/gaming операторів "
                "з API-підходом і контролем над продуктом. "
                "Частіше обирають команди з власними продуктовыми вимогами."
            ),
            "Сайт": "https://www.amelco.co.uk",
        },
        {
            "№": 18,
            "Платформа": "EvenBet Gaming",
            "Модель": "Turnkey / White-label",
            "Фокус": "Poker + casino platform",
            "Опис": (
                "Платформа з акцентом на poker і casino-вертикалі: "
                "white-label/turnkey, бекофіс, інструменти для запуску "
                "і масштабування ігрового бренду."
            ),
            "Сайт": "https://evenbetgaming.com",
        },
        {
            "№": 19,
            "Платформа": "Salsa Technology",
            "Модель": "Platform / Turnkey",
            "Фокус": "LatAm і multi-product",
            "Опис": (
                "iGaming platform provider з рішеннями для casino/sports "
                "і присутності в LatAm. Повний операційний стек для запуску бренду."
            ),
            "Сайт": "https://salsatechnology.com",
        },
        {
            "№": 20,
            "Платформа": "Upgaming",
            "Модель": "White-label / Turnkey",
            "Фокус": "Casino platform для mid-market",
            "Опис": (
                "White-label/turnkey casino platform: бекофіс, бонуси, "
                "платіжні інтеграції, готовий шлях до запуску онлайн-казино "
                "без власної розробки платформи."
            ),
            "Сайт": "https://upgaming.com",
        },
    ]
)


def ensure_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def to_md_table(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    lines = [
        "| " + " | ".join(cols) + " |",
        "| " + " | ".join("---" for _ in cols) + " |",
    ]
    for _, row in df.iterrows():
        cells = [str(row[c]).replace("|", "\\|").replace("\n", " ") for c in cols]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def build_report(df: pd.DataFrame) -> str:
    short = df[["№", "Платформа", "Модель", "Фокус", "Сайт"]]
    full = df[["№", "Платформа", "Модель", "Фокус", "Опис", "Сайт"]]
    return "\n".join(
        [
            "# Топ-20 casino platforms (B2B)",
            "",
            "Категорія: **платформи для запуску онлайн-казино** "
            "(turnkey / white-label / PAM) на кшталт Softswiss і Slotegrator.",
            "",
            "**Не включено:** окремі game aggregators "
            "(Hub88, Alea, Pariplay Fusion, St8, Relax Silver Bullet тощо).",
            "",
            "## Таблиця (коротко)",
            "",
            to_md_table(short),
            "",
            "## Таблиця з описами",
            "",
            to_md_table(full),
            "",
            "## Що вважається «платформою» тут",
            "",
            "- PAM / акаунти гравців, wallet",
            "- Back office, бонуси, платежі",
            "- Frontend або white-label шаблони",
            "- Можливість запустити casino-бренд (turnkey / WL)",
            "",
            "Контент ігор у платформі може бути підключений, "
            "але сам продукт — **platform**, не standalone aggregator.",
            "",
            f"CSV: `{CSV_PATH.as_posix()}`",
            "",
        ]
    )


def main() -> None:
    ensure_output_dir()
    for stale in OUTPUT_DIR.glob("*"):
        if stale.is_file():
            stale.unlink()

    TOP20.to_csv(CSV_PATH, index=False, encoding="utf-8")
    REPORT_PATH.write_text(build_report(TOP20), encoding="utf-8")

    print("ТОП-20 CASINO PLATFORMS (без агрегаторів)")
    print(TOP20[["№", "Платформа", "Модель", "Фокус"]].to_string(index=False))
    print(f"\nMD:  {REPORT_PATH}")
    print(f"CSV: {CSV_PATH}")


if __name__ == "__main__":
    main()
