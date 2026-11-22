### Studio MONO — Lead Programmer / Tech Lead
January 2011 – December 2018 · **INSOMNIA: The Ark** (Steam)

Stack: Unreal Engine, Ogre3D, Bullet, C++, Blueprint, Lua, C#, PHP, shaders.

- **Inventory:** logical inventory with nested containers, slots, item behavior rules (including debuffs, effects, abilities) and integration with attributes, saves, and UI.
- **Attributes and modifiers:** calculation system covering all modifiers, with a calculation trace for debugging and anti-cheat protection.
- **Saves:** custom compressed format (JSON plus packed binary) with save-slot rotation; save and load under 100 ms.
- **UI:** interface state management on a dynamic finite state machine, letting developers change their own parts without conflicts.
- **Interactions:** loot, trading, workbenches, repair, switches, ladders.
- Built the Ogre3D engine layer: shader-based lighting, a particle system faster than the stock one, Bullet physics, an animation FSM, weighted AI, a Blender export plugin, asset building with LOD generation, delta updates, and networked play with a passive server.
- Owned technical documentation, developer consulting, code review, internal tools, and automated gameplay tests.
- Publications: "How we stopped being afraid of Ogre and started making a game on it" — [habr.com/ru/companies/mono/articles/228139](https://habr.com/ru/companies/mono/articles/228139/)
