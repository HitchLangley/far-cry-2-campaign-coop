# Checking sync with the coop-anything tools

The probe feeds three of the sync test tools from [coop-anything](https://github.com/cranebeaker/coop-anything/tree/main/tools)
(checked 2026-11-17 with two copies on one PC). Clone that repository somewhere; the commands below use `<hub>` for it.

## animcheck: what each copy shows

`acstream 1` (in `coop_auto.txt` or `coop_native.txt`) makes the probe write `bin\coop_anim.jsonl` at 20 Hz in the
animcheck probe format: our player (ref `0xA1` on the host, `0xB1` on the joiner, because both load one save and share
the player's entity id), the other player's avatar (`"avatar": true`) and every synced NPC under the host's id. It
sends position, facing (yaw from the entity matrix), health (dead) and the weapon; no bones and no animation groups
yet, so the pose, T-pose and sliding checks stay off.

```
python -I <hub>/tools/animcheck/cli.py analyze host=<copy A>\bin\coop_anim.jsonl client=<copy B>\bin\coop_anim.jsonl ^
    --profile tools\hub\animcheck_profile.json ^
    --avatar "playerA=host:A1>client:<avatar id on B>" --avatar "playerB=client:B1>host:<avatar id on A>" --html report.html
```

Both copies stamp `rx_ms` with the PC's tick count, so their clocks line up without `--auto-offset`.

## inspect: both copies side by side

`bridge <port>` starts a read-only server for `tools/inspect` (bridge protocol 1: `ping`, `version`, `methods`,
`state`; nothing that changes the game). Use one port per copy, for example `bridge 27990` on A and `bridge 27991` on B:

```
python -I <hub>/tools/inspect/inspect_live.py --fields tools\hub\inspect_fields.json ^
    --endpoint A=tcp://127.0.0.1:27990 --endpoint B=tcp://127.0.0.1:27991 --watch 1
```

Rows: role, player health / position / weapon, the avatar, the peer's weapon, packets received, link age, NPCs sent and
puppets, the town alarm, fps and the worst frame of the last 10 s. Problems: a silent link, the 24-NPC limit, a frame
over 100 ms, and a town alarm that differs between the copies.

## chaos: a bad network

One relay per direction, then point each copy's `netstart` at the other's relay:

```
python -I <hub>/tools/chaos/chaos.py relay --target 127.0.0.1:9100 --listen 9201 --rpc-port 9301 --profile bad_wifi
python -I <hub>/tools/chaos/chaos.py relay --target 127.0.0.1:9101 --listen 9202 --rpc-port 9302 --profile bad_wifi
A: netstart 9100 127.0.0.1 9202 $ME        B: netstart 9101 127.0.0.1 9201 $ME
python -I <hub>/tools/chaos/chaos.py call --rpc-port 9301 set_profile "{\"profile\":\"hell\"}"
```

First run (2026-11-17): under `bad_wifi`, then `hell` for 30 s and a 4 s cut both ways, nothing crashed, the link came
back by itself after the cut, all 17 NPC puppets stayed, and the avatars stayed within 0.09 m (p95) of the players.
