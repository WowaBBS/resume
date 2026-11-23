**English** · [Русский](README.ru.md)

# Vladimir Savin

**Tech Lead / Senior C++ Programmer — Unreal Engine**

Remote (EU / worldwide) · open to occasional travel · +7 917 143-51-22 · wowabbs+hh1@gmail.com · Telegram @wowabb · github.com/WowaBBS

## Summary

Tech Lead / Senior C++ Programmer with 25 years in commercial software and 14 years in game development. Credited as Lead Programmer on INSOMNIA: The Ark, then 6 years 7 months as Tech Lead at PAN GAMES on Unreal Engine (UE4 → UE5). Owned the architecture of ~45 subsystems, led a team of up to 30 engineers (6 C++ / 15 Blueprint) and shipped to five platforms. Strong in gameplay systems, client–server networking, developer tools, and backend services for online games. Comfortable diving into large unfamiliar codebases and refactoring legacy code without a rewrite. Outside work: reverse engineering the Gothic engine (contributor to GEngine).

## Core Skills

- C++ (11/14/17/20), Unreal Engine 4/5, Blueprint, C#, Lua, PHP
- Gameplay: inventory, attributes and modifiers, save/load, UI, interactions
- Networking: replication, server-side validation, anti-cheat, digital signatures
- Backend: game server orchestration, matchmaking, metrics, analytics, monitoring
- Tooling: profilers, editors, ImGui, logging and build systems
- Cross-platform: Windows, Linux, macOS, iOS, Android; CI/CD, Docker, Kubernetes
- Practices: code review, automated tests, mentoring, technical interviews

## Experience

### PAN GAMES — Tech Lead / Senior C++ Programmer
June 2019 – December 2025 · **BULLET YEETERS** (Steam, Epic Games Store)

Stack: C++, Unreal Engine 5, Blueprint, PHP, MySQL, C#, PlayFab, Azure, Docker, Kubernetes, CI/CD.

- Designed the architecture of the networked game and the boundaries of ~45 subsystems; led a team of up to 30 people, ran code reviews, technical interviews, and mentoring.
- Delivered cross-platform builds for Windows, Linux, macOS, iOS, and Android, including migration between Unreal Engine versions and third-party integrations via CI/CD.
- Built a replicated inventory with the full feature set of the INSOMNIA system while minimizing network traffic.
- Implemented JSON serialization on Unreal Engine reflection (an `nlohmann/json` analogue aware of `UStruct`), removing hand-written serialization code.
- Built the client–backend integration layer used by all gameplay developers.
- Implemented additional content loading beyond the stock UE pipeline, plus asset preloading and deferred loading to eliminate hitches and reduce memory use.
- Built the logging system: reflection-based output of complex types, per-subsystem verbosity in shipping and editor builds, multiple sinks (file, editor, metrics), async and sync modes.
- Built backend services: game server orchestrator (full lifecycle, demand prediction, build delivery, log collection, scale-down), matchmaking (region, teams, parameters), inventory, monitoring, push notifications.
- Built anti-cheat and server-side validation on a "never trust the client" principle: rule sets, digital signatures, duplicated client-side validation to avoid latency.
- Built the gameplay metrics and analytics platform with cohort analysis and real-time detection of bugs on first users, running alongside GameAnalytics, Firebase, and MMPs.
- **Scale:** 15 matches/second with 20 players each; 10,000 concurrent players (architected for 100,000); 34 orchestrators and 30 game servers per orchestrator.

### Alersteam — Senior C++ Programmer
September 2018 – August 2023 · **Exoplanet First Contact** (Steam) · concurrent project

Stack: C++, OpenGL, Lua, PHP, CMake.

Scope: engine layer and developer tooling — build system, profiler, debug visualisation, third-party integrations.

- Built WBuild.php, a build system that runs a full build from all sources in every mode in minutes instead of hours ([github.com/WowaBBS/WBuild.php](https://github.com/WowaBBS/WBuild.php)).
- Built a low-overhead profiler with an interactive call tree; its data led to removing multiple bottlenecks.
- Built Debug3D for visualizing bones, physics, interaction zones, and scatterer, plus ImGui tools for debugging and content editing.
- Built the logging system with UE-style source management and an automatic object scatter system.
- Integrated Wwise, RenderDoc, CrashFix, HBAO, Tracy, Recast, Umbra, Cal3D, Theora, DevIL.

### Studio MONO — Lead Programmer / Tech Lead
January 2011 – December 2018 · **INSOMNIA: The Ark** (Steam)

Stack: Unreal Engine, Ogre3D, Bullet, C++, Blueprint, Lua, C#, PHP, shaders.

- **Inventory:** logical inventory with nested containers, slots, item behavior rules (including debuffs, effects, abilities) and integration with attributes, saves, and UI.
- **Attributes and modifiers:** calculation system covering all modifiers, with a calculation trace for debugging and anti-cheat protection.
- **Saves:** custom compressed format (JSON plus packed binary) with save-slot rotation; save and load under 100 ms.
- **UI:** interface state management on a dynamic finite state machine, letting developers change their own parts without conflicts.
- **Interactions:** loot, trading, workbenches, repair, switches, ladders.
- Ogre3D engine layer: shader-based lighting, particles, physics, animation, AI, Blender export plugin, asset building with LOD.
- Owned technical documentation, developer consulting, code review, internal tools, and automated gameplay tests.
- Publications: "How we stopped being afraid of Ogre and started making a game on it" — [habr.com/ru/companies/mono/articles/228139](https://habr.com/ru/companies/mono/articles/228139/)

### NetCracker — Lead Software Engineer
June 2010 – January 2015 · BSS/OSS for telecom · concurrent project

Stack: Java, Oracle, PostgreSQL, Spring, JUnit, CI/CD.

- Optimized a database query behind a report: generation time dropped from days to minutes.
- Refactored a PDF network-schema generator into 250+ classes instead of a class of static methods, keeping functionality and enabling extension.
- Built a mock-testing library so other teams could write their own automated tests, and a grant auditing system that analyzes the grant inheritance graph.

### Earlier, 2000–2010

- **Samara State University, Distance Learning Department** (2004–2010): e-learning server, textbook builder (led creation of ten textbooks), video conferencing, physics exam-prep system.
- **Samara State University, IT Analytics Center** (2005–2007): in-house CMS, alumni database, dozens of university websites. **Lecturer** (2005–2007): LabVIEW, C++, TCP/IP, cryptographic protocols.
- **VeloWaver** (2004–2005): cross-platform C++ game library for Win32, Windows CE, Symbian; several games.
- **Pixel** (2003–2004): TCP/IP stack from scratch (IP, TCP, UDP, ICMP, DHCP, ARP, NTP, DNS) for the Vigil OS; encryption, authorization, and remote control protocols for a video surveillance system.
- **Active Solutions** (2000–2001): PHP web framework, markup, database design.

## Projects

**BULLET YEETERS** — [Steam](https://store.steampowered.com/app/3624020/BULLET_YEETERS) · [Epic Games Store](https://store.epicgames.com/en-US/p/bullet-yeeters-438176)
**INSOMNIA: The Ark** — [Steam](https://store.steampowered.com/app/783170/INSOMNIA_The_Ark) · [credits: Lead Programmer](https://www.mobygames.com/game/114363/insomnia-the-ark/credits/windows/)
**Exoplanet First Contact** — [Steam](https://store.steampowered.com/app/531660/Exoplanet_First_Contact/)
**GEngine** — contributor to the Gothic engine reverse-engineering project. **WBuild.php** — [github.com/WowaBBS/WBuild.php](https://github.com/WowaBBS/WBuild.php)

## Education

Samara State University, 1999–2005. Faculty of Mechanics and Mathematics, Computer Security. MSc equivalent.

**Languages:** Russian — native; English — **B2** (technical documentation and written communication: confident; limited speaking practice).

---

**Скачать / Download:** русское [PDF](savin_vladimir_cv.pdf) · [DOCX](savin_vladimir_cv.docx) · English [PDF](savin_vladimir_cv_en.pdf) · [DOCX](savin_vladimir_cv_en.docx)

_Sources: `resume/` (ru), `resume-en/` (en). PDF and DOCX are rebuilt automatically
whenever these files change._
