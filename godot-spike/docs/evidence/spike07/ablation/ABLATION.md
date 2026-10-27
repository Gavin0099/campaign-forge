# Single-lever and combination ablations

Each complete row: same 40 seeds × six policies. Original spike06 operator; fixed HP/damage/move/ranges/LOS/kit/objective. Incomplete trials are excluded from acceptance.

| Case | road wins | flank wins | turtle wins | retreat wins | dash wins / wave-free | scripted wins / wave-free / free T6 |
| --- | --- | --- | --- | --- | --- | --- |
| fallback | 20/40 | 16/40 | 1/40 | 0/40 | 36/36 | 23/2/2 |
| leader-post | 18/40 | 27/40 | 0/40 | 2/40 | 24/15 | 15/1/1 |
| post-one | 29/40 | 25/40 | 11/40 | 0/40 | 32/30 | 27/0/0 |
| post-one-wave-t3 | 26/40 | 22/40 | 12/40 | 0/40 | 10/0 | 8/0/0 |
| post-one-wave-t4 | 19/40 | 23/40 | 9/40 | 0/40 | 15/1 | 8/0/0 |
| post-wave-t3 | 24/40 | 23/40 | 6/40 | 2/40 | 4/0 | 11/0/0 |
| post-wave-t4 | 15/40 | 24/40 | 1/40 | 0/40 | 13/1 | 11/0/0 |
| wave-t3 | 26/40 | 32/40 | 10/40 | 0/40 | 8/0 | 19/0/0 |
| wave-t4 | 27/40 | 24/40 | 8/40 | 0/40 | 24/3 | 19/0/0 |

post-one = leader and hold point(21,9); leader-post/post = (22,9), from(20,9). wave-t4 / wave-t3 = arrival4 /3, from5; warning always arrival−1; original birth rest retained. fallback = announced one-cell step toward wave, counter otherwise unchanged. No terrain or objective gate.
T5 partial-start probes with earlier waves preserve authored birth age, but do not simulate pre-placement pursuit: staged full-HP allies and entry wave, explicitly not full battles.
All compact traces use their own fixed-phase event collector; their hashes are not full-telemetry hashes. Distinct traces are not independent samples.
