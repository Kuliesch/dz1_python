# Stage 0 — Kick feasibility & compliance (GO / NO-GO)

**Проєкт:** Blue Wave  
**Етап:** 0. Feasibility & compliance (Тиждень 1)  
**Дата перевірки:** 4 листопада 2026 (Europe/Warsaw)  
**Статус рішення:** **NO-GO для вихідної гіпотези** · **CONDITIONAL GO для сумісного формату / півоту дистрибуції**

Цей звіт відповідає критичному gate з концепту: чи дозволяє Kick публікувати саме формат **попередньо записаних коротких (2–3 хв) відеооглядів** з органічним відкриттям, і які правила діють для слотів, AI та зовнішніх посилань.

---

## 1. Вердикт (коротко)

| Питання з концепту | Висновок |
| --- | --- |
| Чи можна **завантажити** готовий відеофайл (як YouTube/TikTok)? | **Ні.** У офіційній документації Kick немає upload попередньо записаних відео. Контент з’являється як livestream → VOD → Clip. |
| Чи сумісний формат «20–30 коротких записаних оглядів» з Kick as-is? | **Ні** як первинна модель публікації. Clips обмежені **10–180 с** і створюються **з live/VOD**, не з окремого файлу. |
| Чи можна «прогнати» запис як live без маскування? | Технічно RTMP-стрім запису можливий, але Kick прямо відносить **pre-recorded content** до підстав **відмови/відкликання verification і Partner Program**. Концепт забороняє маскувати запис під live. |
| Слоти / gambling на Kick? | **Дозволено** за умови локального права творця, мітки **18+**, категорії (напр. Slots & Casino), без гемблінгу на кошти глядачів. |
| AI-персонажі / озвучка? | **Дозволено** за умови **чіткого disclosure** (title / overlay). Заборонені оманливі deepfake/voice clone реальних осіб без дозволу. |
| Зовнішні посилання на owned сайт (без affiliate у пілоті)? | **Ймовірно OK** за умови легальності контенту/юрисдикції; власник каналу відповідає за посилання. Affiliate в пілоті не використовуємо. |
| Органічне охоплення коротких записаних оглядів на Kick? | **Слабка відповідність гіпотезі.** Kick — live-first; типові короткі кліпи для discovery виносять **off-platform** (Shorts/TikTok/Reels). |

**Рекомендація Stage 0:** не запускати виробництво 20–30 роликів під вихідну схему «upload short reviews → Kick organic → сайт». Зафіксувати зміну гіпотези (див. §5) перед Stage 1.

---

## 2. Матриця відповідності вимогам пілота

| Вимога пілота | Kick reality | Ризик | Статус |
| --- | --- | --- | --- |
| Попередньо записані огляди 2–3 хв | Немає file upload; clips ≤ 180 с лише з live/VOD | Критичний | ❌ Blocker |
| Органічне охоплення без paid | Live/VOD discovery; short-form discovery слабкий on-platform | Високий | ⚠️ Hypothesis weak |
| Не маскувати запис під live | Pre-recorded = ризик verification/Partner | Високий | ❌ Conflicts with concept |
| Слоти / demo gameplay | Дозволено + 18+ + category + local law | Середній (GEO/legal) | ✅ Conditional |
| AI-блогери з disclosure | Дозволено з прозорим маркуванням | Низький–середній | ✅ Conditional |
| Посилання Kick → owned catalog (no casino CTA) | Допустимо за відповідальність каналу; без illegal links | Середній | ✅ Conditional |
| Вимірювання Kick → site (UTM/referrer) | Залежить від формату посилань у panel/title/chat | Середній | ⚠️ Test needed |
| VOD доступність для catch-up | Non-verified: **7 днів** / 16 VODs; Verified: **30 днів** / 30 VODs | Середній для «залишених» оглядів | ⚠️ Retention limit |

---

## 3. Докази (першоджерела Kick)

### 3.1 Немає upload; є лише stream → VOD → Clip

- [KICK VODs (stream replays)](https://help.kick.com/en/articles/7112432-kick-vods-stream-replays): VOD зберігається **після завершення livestream**. Термін: 7 днів (non-verified) / 30 днів (verified); ліміти 16 / 30 VODs.
- [How to create clips on KICK](https://help.kick.com/en/articles/7120566-how-to-create-clips-on-kick): кліпи **10–180 секунд** з livestream або VOD (не з окремого завантаженого файлу).

Незалежне підтвердження відсутності upload (станом на перевірку джерел у жовтні–листопаді 2026): [LiveReacting — Can You Upload Videos to Kick?](https://blog.livereacting.com/how-to-stream-a-pre-recorded-video-on-kick/).

### 3.2 Pre-recorded vs verification / Partner

- [Grounds for revoking or refusing verification or the KICK partner program](https://help.kick.com/en/articles/7901645-grounds-for-revoking-or-refusing-verification-or-the-kick-partner-program): вимагає *«Stream original, live content»* і прямо: *«Avoid mirror streams, blank streams, or **pre-recorded content**»*.

Це не обов’язково миттєвий бан акаунта, але **несумісно** з пілотом, який покладається на масштабовані записані огляди і не хоче маскувати їх під live.

### 3.3 Gambling / slots

- [Community Guidelines](https://kick.com/community-guidelines) (оновлено **19/03/2026**): gambling дозволений за законами юрисдикції творця; заборонено gambling на кошти інших користувачів; minors не можуть брати участь; affiliate/sponsored gambling — лише для ліцензованих платформ + чітке disclosure; потрібні age-labeling і categorization.
- [Content classification labels](https://help.kick.com/en/articles/15063676-content-classification-labels-when-to-use-them): gambling **завжди** потребує **18+**; категорія на кшталт **Slots & Casino**.
- [What gets you suspended](https://help.kick.com/en/articles/15063665-what-gets-you-suspended-on-kick): suspend за illegal gambling, audience-funded gambling, unlicensed sponsored gambling, відсутність disclosure / age-label.

Пілот без affiliate/депозитних CTA — **знижує** ризик sponsorship-порушень, але **не знімає** обов’язок 18+, категорії та відповідності праву GEO творця.

### 3.4 AI / synthetic creators

- Community Guidelines + classification labels: AI-контент, що імітує реальність, **дозволений** за **чіткого disclosure** (title або on-screen overlay). Заборонені оманливі deepfakes / voice clones приватних осіб без дозволу, NCII тощо.
- Для Blue Wave: маркувати кожного AI-блогера як синтетичного персонажа в title/overlay і на owned сайті (як уже вимагає концепт).

### 3.5 Зовнішні посилання

- Community Guidelines (Stream Management): власник каналу відповідає за links у title / pinned / panel; **links to illegal websites** заборонені.
- Affiliate links для gambling — дозволені з disclosure, але **пілот свідомо їх не використовує**.
- Окремої заборони на посилання на informational catalog / review site в публічних guidelines не знайдено; потрібен smoke-test реального panel-посилання перед публікацією партії.

### 3.6 Органічне охоплення short-form

Офіційна модель Kick — live + VOD + clips на каналі. Публічні growth-гайди (сторонні) послідовно радять виносити clips на **YouTube Shorts / TikTok / Reels** для discovery, а не покладатися на Kick як short-form feed. Це **прямо послаблює** гіпотезу «короткі огляди на Kick → органіка → сайт» без додаткового каналу.

---

## 4. Відкриті compliance-питання (ще не закриті Stage 0)

Ці пункти **не блокують** вердикт щодо формату Kick, але **блокують** Stage 1–3 production:

1. **Права на геймплей:** ліцензії/дозволи провайдерів і демо-середовищ на запис і повторну публікацію.
2. **GEO творця:** в якій юрисдикції ведеться стрім/публікація gambling-контенту; чи законно показувати slots.
3. **18+ / age gates** на Kick і на owned сайті.
4. **Fact-check pipeline:** заборона вигаданих RTP/механік/тверджень про шанси (з концепту).
5. **Атрибуція Kick → site:** які UTM/referrer реально зберігаються з panel vs chat vs title.

---

## 5. Зафіксована зміна гіпотези (рекомендовані варіанти)

Концепт: *«Якщо формат недоступний, не маскувати запис під live; обрати сумісний формат або інший майданчик і зафіксувати зміну гіпотези.»*

| Варіант | Суть | Що тестуємо | Рекомендація |
| --- | --- | --- | --- |
| **A. Compatible Kick** | Живі (або чесно label-нуті) демосесії 15–30 хв → clips 60–180 с → panel link на сайт | Чи працює Kick для slots+AI+links у live-native форматі | Можливий secondary тест, але **не** ізолює short-form organic так, як задумано |
| **B. Pivot primary distribution** | Short reviews 2–3 хв на **YouTube Shorts** (і/або TikTok) → owned site; Kick опційно | Оригінальна content-гіпотеза на платформі з native short upload + feed | **Рекомендовано як новий primary** |
| **C. Dual-channel micro-pilot** | 5 роликів Shorts + 5 сумісних Kick clips, єдиний сайт і аналітика | Порівняти attributed visits / cost | Найкращий спосіб не «вгадати» канал |

**Пропозиція рішення для стейкхолдерів:**  
**NO-GO** на вихідний Kick-upload пілот → обрати **B** або **C**, оновити §4 концепту, і лише тоді відкривати Stage 1 (content prototype).

---

## 6. Gate checklist

| Gate | Результат |
| --- | --- |
| Kick rules перевірені (офіційні джерела) | ✅ |
| Формат публікації pre-recorded short reviews | ❌ Недоступний as designed |
| Pre-recorded без маскування під live | ❌ Конфлікт із Partner/verification policy |
| Slots / 18+ / AI disclosure / outbound links | ✅ Умовно допустимі |
| Органічна short-form гіпотеза на Kick | ⚠️ Слабка / не підтверджується моделлю платформи |
| Права геймплею + GEO legal opinion | ⏳ Відкрито |
| **Stage 0 overall** | **NO-GO (оригінальна гіпотеза)** / **CONDITIONAL GO (півот)** |

---

## 7. Джерела

| Джерело | URL | Примітка |
| --- | --- | --- |
| Kick Community Guidelines | https://kick.com/community-guidelines | Updated 19/03/2026 |
| Kick Help — VODs | https://help.kick.com/en/articles/7112432-kick-vods-stream-replays | Official |
| Kick Help — Clips | https://help.kick.com/en/articles/7120566-how-to-create-clips-on-kick | Official; 10–180s |
| Kick Help — Verification / Partner grounds | https://help.kick.com/en/articles/7901645-grounds-for-revoking-or-refusing-verification-or-the-kick-partner-program | Pre-recorded listed |
| Kick Help — Classification labels | https://help.kick.com/en/articles/15063676-content-classification-labels-when-to-use-them | 18+, AI disclosure |
| Kick Help — Suspensions | https://help.kick.com/en/articles/15063665-what-gets-you-suspended-on-kick | Gambling / AI |
| Kick Advertising Policy | https://kick.com/advertising-policy | Ads ≠ creator links; gambling ad rules |
| LiveReacting (secondary) | https://blog.livereacting.com/how-to-stream-a-pre-recorded-video-on-kick/ | No upload documented |
| Concept v0.1 | `sources/Blue_Wave_Concept_Roadmap_v0.1.docx` | Internal |

*Цей звіт не є юридичною консультацією. Перед Stage 1 потрібні підтвердження прав на геймплей і legal review GEO.*
