import sys
import argparse
from CS6381 import Broker


zone = sys.argv[1]

b = Broker(zone)
b.connect_broker()


