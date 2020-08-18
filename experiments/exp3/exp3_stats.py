import sys
import pstats

profile_raw_file = sys.argv[1]
p = pstats.Stats(profile_raw_file)
p.strip_dirs().sort_stats('tottime').print_stats(20)
