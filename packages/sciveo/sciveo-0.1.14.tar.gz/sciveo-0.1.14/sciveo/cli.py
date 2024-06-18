#!/usr/bin/env python
#
# Pavlin Georgiev, Softel Labs
#
# This is a proprietary file and may not be copied,
# distributed, or modified without express permission
# from the owner. For licensing inquiries, please
# contact pavlin@softel.bg.
#
# 2024
#

import os
import argparse

from sciveo.common.tools.logger import *
from sciveo.common.tools.timers import Timer
from sciveo.monitoring.start import MonitorStart
from sciveo.monitoring.network import NetworkTools
from sciveo.common.tools.configuration import GlobalConfiguration


def main():
  config = GlobalConfiguration.get()

  parser = argparse.ArgumentParser(description='sciveo CLI')
  parser.add_argument('command', choices=['init', 'monitor', 'scan'], help='Command to execute')
  parser.add_argument('--period', type=int, default=120, help='Period in seconds')
  parser.add_argument('--block', type=bool, default=True, help='Block flag')
  parser.add_argument('--auth', type=str, default=config['secret_access_key'], help='Auth secret access key')
  parser.add_argument('--timeout', type=float, default=1.0, help='Timeout')
  parser.add_argument('--port', type=int, default=22, help='Host port number, used for network ops')
  parser.add_argument('--localhost', type=bool, default=False, help='Add localhost to list of hosts')
  args = parser.parse_args()

  if args.command == 'monitor':
    MonitorStart(period=args.period, block=args.block)()
  elif args.command == 'scan':
    NetworkTools(timeout=args.timeout, localhost=args.localhost).scan_port(port=args.port)
  elif args.command == 'init':
    home = os.path.expanduser('~')
    base_path = os.path.join(home, '.sciveo')
    if not os.path.exists(base_path):
      os.makedirs(base_path)
      default_lines = [
        "secret_access_key=<your secret access key>",
        "api_base_url=https://sciveo.com",
        "log_min_level=DEBUG"
      ]
      with open(os.path.join(base_path, "default"), 'w') as fp:
        for line in default_lines:
          fp.write(line + '\n')
    else:
      info(f"init, [{base_path}] already there")
  else:
    warning(args.command, "not implemented")

if __name__ == '__main__':
    main()