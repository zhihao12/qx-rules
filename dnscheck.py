#!/usr/bin/env python3
# Bulk DNS liveness checker (stdlib only, Python 3.6+).
# Usage: dnscheck.py <domains.txt> <verdicts.tsv>
# Verdict per domain: A = resolves (NOERROR), D = NXDOMAIN, U = unknown
# (timeout / SERVFAIL after retries). Only D is a prune candidate, and the
# caller confirms D in a second round before anything is pruned.
import socket
import struct
import sys
import threading
import time

RESOLVERS = ['1.1.1.1', '8.8.8.8', '223.5.5.5']
TIMEOUT = 3.0
WORKERS = 120

lock = threading.Lock()
counter = [0]


def build_query(domain, qid):
    header = struct.pack('>HHHHHH', qid, 0x0100, 1, 0, 0, 0)
    qname = b''
    for part in domain.encode('idna').split(b'.'):
        qname += bytes([len(part)]) + part
    qname += b'\x00'
    return header + qname + struct.pack('>HH', 1, 1)


def check_one(domain, idx):
    for attempt in range(2):
        resolver = RESOLVERS[(idx + attempt) % len(RESOLVERS)]
        qid = (idx * 7 + attempt * 30000 + 1234) % 65536
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(TIMEOUT)
            sock.sendto(build_query(domain, qid), (resolver, 53))
            data, _ = sock.recvfrom(2048)
            sock.close()
        except Exception:
            continue
        if len(data) < 4:
            continue
        rcode = data[3] & 0x0F
        if rcode == 3:
            return 'D'
        if rcode == 0:
            return 'A'
        # SERVFAIL etc: try next resolver
    return 'U'


def main():
    src, dst = sys.argv[1], sys.argv[2]
    domains = []
    with open(src, encoding='utf-8', errors='replace') as f:
        for line in f:
            d = line.strip().lower()
            if d:
                domains.append(d)
    total = len(domains)
    print('checking %d domains' % total, flush=True)
    results = [None] * total

    def worker(start):
        for i in range(start, total, WORKERS):
            results[i] = check_one(domains[i], i)
            with lock:
                counter[0] += 1
                if counter[0] % 20000 == 0:
                    print('progress %d/%d' % (counter[0], total), flush=True)

    threads = [threading.Thread(target=worker, args=(w,)) for w in range(WORKERS)]
    t0 = time.time()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    with open(dst, 'w', encoding='utf-8') as f:
        for d, v in zip(domains, results):
            f.write('%s\t%s\n' % (d, v or 'U'))
    counts = {}
    for v in results:
        counts[v or 'U'] = counts.get(v or 'U', 0) + 1
    print('done in %.0fs: %s' % (time.time() - t0, counts), flush=True)


if __name__ == '__main__':
    main()
