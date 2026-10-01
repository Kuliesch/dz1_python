# Аналіз ігрового ринку

Python-аналіз глобального та українського ігрового ринку на основі публічних даних Newzoo і DOU.

## Швидкий старт

```bash
pip install -r requirements.txt
python game_market_analysis.py
```

Скрипт виведе ключові метрики в консоль, оновить `GAME_MARKET_REPORT.md` і збереже графіки/CSV у `output/`.

## Розділи звіту

1. **Топ 10 ігрових платформ** — App Store, Google Play, China Android, PSN, Steam…
2. Макроринок Mobile / Console / PC (Newzoo)
3. Монетизація
4. Український контекст
5. Висновки

## Що всередині

| Файл | Опис |
|------|------|
| `game_market_analysis.py` | Розрахунки, візуалізації, генерація звіту |
| `GAME_MARKET_REPORT.md` | Повний звіт українською |
| `output/` | PNG-графіки та CSV (`top10_platforms.csv` тощо) |

## Топ-3 платформи за виручкою ігор (2025)

1. Apple App Store — $52.5B  
2. Google Play — $30.0B  
3. China Android stores — ~$28B (оцінка)
