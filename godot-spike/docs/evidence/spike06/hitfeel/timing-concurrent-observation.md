# Timing concurrency observation (W5)

First fixed60 timing run overlapped field capture / headless visibility tests.
Observed normal wall seconds1.793104/1.845108/1.839547;
crit1.899545/1.944307/1.920584;Reduced1.385756/1.392274/1.419897.
Simulation normal.95/crit1.0166667/Reduced.7166667 for all setups.
This exceeded the wall1.7s bound under concurrent work. The timing JSON was
subsequently rerun in place; this table preserves the observed first values,
not a reconstructed original JSON. timing.log retains that invocation's log.
Final timing-alone.log / timing.json describe the uncontended rerun. W6 will
measure field timings without movie/readbacks; recorded AVI encoder wall time
is not gameplay presentation speed. No60FPS or unconditional latency claim.
