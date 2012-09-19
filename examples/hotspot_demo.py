import hotshot
import hotshot.stats
from examples import pystone

prof = hotshot.Profile("stones.prof")
benchtime, stones = prof.runcall(lambda : pystone.pystones(10000))
prof.close()

stats = hotshot.stats.load("stones.prof")
stats.strip_dirs()
stats.sort_stats('time', 'calls')
stats.print_stats(20)
