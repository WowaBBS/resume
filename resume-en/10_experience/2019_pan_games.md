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
