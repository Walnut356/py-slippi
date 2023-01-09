py-slippi (Combos Fork)
=========

Py-slippi is a Python parser for [.slp](https://github.com/project-slippi/slippi-wiki/blob/master/SPEC.md) game replay files for [Super Smash Brothers Melee](https://en.wikipedia.org/wiki/Super_Smash_Bros._Melee) for the Nintendo GameCube. These replays are generated by Jas Laferriere's [Slippi](https://github.com/JLaferri/project-slippi) recording code, which runs on a Wii or the [Dolphin](https://dolphin-emu.org/) emulator.

Usage
=====

**Combo Finder**::

See combo_example.py for simple multiprocessed example. Key commands include:

```python
example.ComboComputer()
```

To create the object that handles combo computing

```python
example.prime_replay(Path)
```

To load parse the replay and load the relevant data into the object

```python
example.combo_compute(connect_code)
```

To generate the list of combos for a specific slippi connect code. At the moment, the connect code is NOT optional. Additional optional keyword arguments allow toggling of the various checks that extend a combo. All are boolean flags set to True by default (hitstun_check, hitlag_check, tech_check, downed_check, offstage_check, dodge_check, shield_check, shield_break_check, ledge_check)

Filter these combos for desired criteria (helped functions included), for example, ever combo that killed that: have more than 5 hits and does more than 40%, or does more than 70%:

```python
for c in example.combos:
    if(
        c.did_kill and
        (c.minimum_length(5) and c.minimum_damage(40) or
        (c.minimum_damage(60))
        ):
```

combo_example.py exports this filtered list to json format that is compatible with [Project Clippi](https://github.com/vinceau/project-clippi), and can be loaded in and played with no fuss.

Combos are stored as a ComboData object (see: slippi/combo.py). Combo data includes the connect code of the player, a list of the moves used, a boolean flag for a kill, the start/end percent, and the start/end frame. This allows for a filtering combos to contain/not contain one or multiple instances of a move, filtering for the first, second, etc. or final move of a combo, filtering for combo frame-length, and more. 

py-slippi supports both event-based and object-based parsing. Object-based parsing is generally easier, but event-based parsing is more efficient and supports reading partial or in-progress games.

**Object-based parsing**::

```python
    >>> from slippi import Game
    >>> Game('test/replays/game.slp')
    Game(
        end=End(
            lras_initiator=None,
            method=Method.CONCLUSIVE),
        frames=[...](5209),
        metadata=Metadata(
            console_name=None,
            date=2018-06-22 07:52:59+00:00,
            duration=5209,
            platform=Platform.DOLPHIN,
            players=(
                Player(
                    characters={InGameCharacter.MARTH: 5209},
                    netplay_name=None),
                Player(
                    characters={InGameCharacter.FOX: 5209},
                    netplay_name=None),
                None,
                None)),
        start=Start(
            is_frozen_ps=None,
            is_pal=None,
            is_teams=False,
            players=(
                Player(
                    character=CSSCharacter.MARTH,
                    costume=3,
                    stocks=4,
                    tag=,
                    team=None,
                    type=Type.HUMAN,
                    ucf=UCF(
                        dash_back=DashBack.OFF,
                        shield_drop=ShieldDrop.OFF)),
                Player(
                    character=CSSCharacter.FOX,
                    costume=0,
                    stocks=4,
                    tag=,
                    team=None,
                    type=Type.CPU,
                    ucf=UCF(
                        dash_back=DashBack.OFF,
                        shield_drop=ShieldDrop.OFF)),
                None,
                None),
            random_seed=3803194226,
            slippi=Slippi(
                version=1.0.0),
            stage=Stage.YOSHIS_STORY))
```
Frame data is elided when you print games, but you can inspect a sample frame with e.g. :code:`game.frames[0]`.
```python
    >>> from slippi import Game
    # pass `skip_frames=True` to skip frame data, for a significant speedup
    >>> Game('test/replays/game.slp', skip_frames=True)
```

**Event-driven API**::
```python
    >>> from slippi.parse import parse
    >>> from slippi.parse import ParseEvent
    >>> handlers = {ParseEvent.METADATA: print}
    >>> parse('test/replays/game.slp', handlers)
    Metadata(
        console_name=None,
        date=2018-06-22 07:52:59+00:00,
        duration=5209,
        platform=Platform.DOLPHIN,
        players=(
            Player(
                characters={InGameCharacter.MARTH: 5209},
                netplay_name=None),
            Player(
                characters={InGameCharacter.FOX: 5209},
                netplay_name=None),
            None,
            None))
```
👉 You can pass a stream to :code:`parse`, such as :code:`sys.stdin.buffer`! This is useful for e.g. decompressing with :code:`gunzip`, or reading from an in-progress replay via :code:`tail -c+1 -f`.

