#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import argparse
import pynetgear
import re

# Configuration
config_category = 'netgear'  # 'network' would be a great alternative
# Router credentials
password = 'password'  # If you are connected via a wired connection to the Netgear router, a password is optional.
host = pynetgear.DEFAULT_HOST  # If you are connected to the network of the Netgear router, a host is optional.
user = pynetgear.DEFAULT_USER  # The username defaults to admin.
port = pynetgear.DEFAULT_PORT  # The port defaults to 5000

forced_mode = None

# Munin config mode
parser = argparse.ArgumentParser()
parser.add_argument('arg', nargs='?')
args = parser.parse_args()

# Mode, determined by symlink name
mode = __file__.split('/')[-1]
mode_count = 'netgear-devices'
mode_signal_strength = 'netgear-devices-signal-strength'
mode_link_rate = 'netgear-devices-link-rate'
modes = [
    mode_count,
    mode_signal_strength,
    mode_link_rate
]

if forced_mode is not None:
    mode = forced_mode


def get_connected_devices():
    netgear = pynetgear.Netgear(password, host, user, port)
    if not netgear.logged_in:
        # Log in
        if not netgear.login():
            print('Could not login to router. Please check host, user, password and port')
            sys.exit(1)

    return netgear.get_attached_devices()


def get_device_name(device):
    return device.name if device.name != '--' else device.mac


def slugify(text):
    return re.sub(r'[-\s]+', '-', (re.sub(r'[^\w\s-]', '', text).strip().lower()))


# From https://github.com/yhat/rodeo/issues/90#issuecomment-98790197
if mode not in modes:
    print('Unknown mode {}'.format(mode))
    sys.exit(1)

if args.arg == 'config':
    print('graph_category {}'.format(config_category))

    if mode == mode_count:
        print('graph_title Netgear connected devices count')
        print('graph_args --lower-limit 0')
        print('graph_vlabel #')
        print('amount.label Connected devices amount')
        print('amount.draw LINE')
        print('amount.min 0')
    else:
        if mode == mode_signal_strength:
            print('graph_title Netgear connected devices signal strength')
            print('graph_vlabel signal')
        elif mode == mode_link_rate:
            print('graph_title Netgear connected devices link rate')
            print('graph_vlabel rate')

        for device in get_connected_devices():
            device_name = get_device_name(device)
            slug = slugify(device_name)
            print('{}.label {} {}'.format(slug, device.name, 'signal strength' if mode == mode_signal_strength else 'link rate'))
            print('{}.draw LINE'.format(slug))

    sys.exit(0)

# Let's go
devices = get_connected_devices()

if mode == mode_count:
    print('amount.value {}'.format(len(devices)))
else:
    for device in devices:
        data = device.signal if mode == mode_signal_strength else device.link_rate

        if data is None:
            data = float('nan')

        print('{}.value {}'.format(slugify(get_device_name(device)), data))
