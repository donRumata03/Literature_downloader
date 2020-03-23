#!/usr/bin/env python

"""Pick server and start connection with VPNGate (http://www.vpngate.net/en/)"""

import requests, os, sys, tempfile, subprocess, base64, time



if len(sys.argv) != 2:
    print('usage: ' + sys.argv[0] + ' [country name | country code]')
    exit(1)
country = sys.argv[1]

if len(country) == 2:
    i = 6 # short name for country
elif len(country) > 2:
    i = 5 # long name for country
else:
    print('Country is too short!')
    exit(1)

try:
    vpn_data = requests.get('http://www.vpngate.net/api/iphone/').text.replace('\r','')
    servers = [line.split(',') for line in vpn_data.split('\n')]
    labels = servers[1]
    labels[0] = labels[0][1:]
    servers = [s for s in servers[2:] if len(s) > 1]
except:
    print('Cannot get VPN servers data')
    exit(1)

desired = [s for s in servers if country.lower() in s[i].lower()]
found = len(desired)
print('Found ' + str(found) + ' servers for country ' + country)
if found == 0:
    exit(1)

supported = [s for s in desired if len(s[-1]) > 0]
print(str(len(supported)) + ' of these servers support OpenVPN')
# We pick the best servers by score
winner = sorted(supported, key=lambda s: float(s[2].replace(',','.')), reverse=True)[0]

print("\n== Best server ==")

pairs = []
for label_num in range(len(labels) - 1):
    pairs.append((labels[label_num], winner[label_num]))
    print(labels[label_num], winner[label_num])


'''
pairs = zip(labels, winner)[:-1]
for (l, d) in pairs[:4]:
    print(l + ': ' + d)
'''
print(pairs[4][0] + ': ' + str(float(pairs[4][1]) / 10**6) + ' MBps')
print("Country: " + pairs[5][1])

print("\nLaunching VPN...")
_, path = tempfile.mkstemp()

f = open(path, 'w')
f.write(base64.b64decode(winner[-1]).decode("utf-8"))
f.write('\nscript-security 2\nup /etc/openvpn/update-resolv-conf\ndown /etc/openvpn/update-resolv-conf')
f.close()

print(path)

x = subprocess.Popen(['sudo', 'openvpn', '--config', path])
# x = subprocess.Popen(["runas /noprofile /user:Administrator cmd "])
try:
    while True:
        time.sleep(600)
# termination with Ctrl+C
except:
    try:
        x.kill()
    except:
        pass
    while x.poll() != 0:
        time.sleep(1)
    print('\nVPN terminated')