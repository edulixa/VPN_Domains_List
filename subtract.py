from netaddr import IPNetwork, IPSet

block = [l.strip() for l in open('/tmp/block_raw.txt') if l.strip()]
allow = [l.strip() for l in open('/tmp/allow.txt') if l.strip()]

allow_set = IPSet()
for c in allow:
    try:
        allow_set.add(IPNetwork(c))
    except Exception:
        pass

out = set()
for c in block:
    try:
        net = IPNetwork(c)
    except Exception:
        continue
    if IPSet([net]) & allow_set:
        continue          # overlaps a whitelisted CDN range -> drop
    out.add(str(net))

with open('proton_ips.txt', 'w') as f:
    f.write('\n'.join(sorted(out)) + '\n')

print(f"block={len(block)} allow={len(allow)} final={len(out)}")
