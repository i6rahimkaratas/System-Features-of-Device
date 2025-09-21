#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistem Özellikleri Listeleme Programı
Bu program çalıştığı cihazın sistem özelliklerini detaylı olarak listeler.
"""

import platform
import psutil
import socket
import uuid
import re
import subprocess
import os
from datetime import datetime

def sistem_bilgileri():
    """Temel sistem bilgilerini toplar"""
    print("=" * 60)
    print("SİSTEM BİLGİLERİ")
    print("=" * 60)
    
    print(f"İşletim Sistemi: {platform.system()}")
    print(f"İşletim Sistemi Sürümü: {platform.release()}")
    print(f"İşletim Sistemi Versiyonu: {platform.version()}")
    print(f"Makine Adı: {platform.node()}")
    print(f"Makine Türü: {platform.machine()}")
    print(f"İşlemci Mimarisi: {platform.architecture()[0]}")
    print(f"İşlemci: {platform.processor()}")
    print(f"Python Sürümü: {platform.python_version()}")
    
    # Boot zamanı
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    print(f"Sistem Başlatma Zamanı: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    print()

def donanim_bilgileri():
    """Donanım bilgilerini toplar"""
    print("=" * 60)
    print("DONANIM BİLGİLERİ")
    print("=" * 60)
    
    # CPU bilgileri
    print("CPU BİLGİLERİ:")
    print(f"  Fiziksel çekirdek sayısı: {psutil.cpu_count(logical=False)}")
    print(f"  Mantıksal çekirdek sayısı: {psutil.cpu_count(logical=True)}")
    print(f"  CPU kullanımı: %{psutil.cpu_percent(interval=1)}")
    
    # CPU frekansları
    cpu_freq = psutil.cpu_freq()
    if cpu_freq:
        print(f"  Mevcut frekans: {cpu_freq.current:.2f} MHz")
        print(f"  Minimum frekans: {cpu_freq.min:.2f} MHz")
        print(f"  Maksimum frekans: {cpu_freq.max:.2f} MHz")
    
    print()
    
    # RAM bilgileri
    print("BELLEK (RAM) BİLGİLERİ:")
    memory = psutil.virtual_memory()
    print(f"  Toplam RAM: {get_size(memory.total)}")
    print(f"  Kullanılabilir RAM: {get_size(memory.available)}")
    print(f"  Kullanılan RAM: {get_size(memory.used)} (%{memory.percent})")
    
    # Swap bilgileri
    swap = psutil.swap_memory()
    print(f"  Toplam Swap: {get_size(swap.total)}")
    print(f"  Kullanılan Swap: {get_size(swap.used)} (%{swap.percent})")
    
    print()

def disk_bilgileri():
    """Disk bilgilerini toplar"""
    print("=" * 60)
    print("DİSK BİLGİLERİ")
    print("=" * 60)
    
    # Disk bölümleri
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f"Cihaz: {partition.device}")
        print(f"  Mount noktası: {partition.mountpoint}")
        print(f"  Dosya sistemi: {partition.fstype}")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            print(f"  Toplam boyut: {get_size(partition_usage.total)}")
            print(f"  Kullanılan: {get_size(partition_usage.used)}")
            print(f"  Boş: {get_size(partition_usage.free)}")
            print(f"  Kullanım yüzdesi: %{partition_usage.used / partition_usage.total * 100:.1f}")
        except PermissionError:
            print("  Erişim izni yok")
        print()

def ag_bilgileri():
    """Ağ bilgilerini toplar"""
    print("=" * 60)
    print("AĞ BİLGİLERİ")
    print("=" * 60)
    
    # Hostname ve IP
    hostname = socket.gethostname()
    print(f"Hostname: {hostname}")
    
    try:
        ip = socket.gethostbyname(hostname)
        print(f"IP Adresi: {ip}")
    except:
        print("IP Adresi alınamadı")
    
    # MAC Adresi
    mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    print(f"MAC Adresi: {mac}")
    
    # Ağ arayüzleri
    print("\nAĞ ARAYÜZÜ BİLGİLERİ:")
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        print(f"\n{interface_name}:")
        for address in interface_addresses:
            if str(address.family) == 'AddressFamily.AF_INET':
                print(f"  IP Adresi: {address.address}")
                print(f"  Netmask: {address.netmask}")
                print(f"  Broadcast IP: {address.broadcast}")
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                print(f"  MAC Adresi: {address.address}")
                print(f"  Netmask: {address.netmask}")
                print(f"  Broadcast MAC: {address.broadcast}")
    
    print()

def islem_bilgileri():
    """Çalışan süreçler hakkında bilgi"""
    print("=" * 60)
    print("İŞLEM BİLGİLERİ")
    print("=" * 60)
    
    print(f"Çalışan işlem sayısı: {len(psutil.pids())}")
    
    # En çok CPU kullanan süreçler
    print("\nEn çok CPU kullanan 5 süreç:")
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        processes.append(proc.info)
    
    processes = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)
    for i, process in enumerate(processes[:5]):
        print(f"  {i+1}. {process['name']} (PID: {process['pid']}) - CPU: %{process['cpu_percent']}")
    
    # En çok RAM kullanan süreçler
    print("\nEn çok RAM kullanan 5 süreç:")
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        processes.append(proc.info)
    
    processes = sorted(processes, key=lambda x: x['memory_percent'], reverse=True)
    for i, process in enumerate(processes[:5]):
        print(f"  {i+1}. {process['name']} (PID: {process['pid']}) - RAM: %{process['memory_percent']:.2f}")
    
    print()

def get_size(bytes, suffix="B"):
    """Byte değerini insan okunabilir formata çevirir"""
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def ek_bilgiler():
    """Ek sistem bilgileri"""
    print("=" * 60)
    print("EK SİSTEM BİLGİLERİ")
    print("=" * 60)
    
    # Kullanıcı bilgileri
    print(f"Mevcut kullanıcı: {os.getenv('USER', os.getenv('USERNAME', 'Bilinmiyor'))}")
    print(f"Ev dizini: {os.path.expanduser('~')}")
    print(f"Çalışma dizini: {os.getcwd()}")
    
    # Çevre değişkenleri (bazıları)
    print(f"PATH: {os.environ.get('PATH', 'Tanımlı değil')[:100]}...")
    
    # Sistem yükü (Unix sistemlerde)
    if hasattr(os, 'getloadavg'):
        load1, load5, load15 = os.getloadavg()
        print(f"Sistem yükü (1dk, 5dk, 15dk): {load1:.2f}, {load5:.2f}, {load15:.2f}")
    
    print()

def main():
    """Ana fonksiyon"""
    print("DETAYLI SİSTEM ÖZELLİKLERİ RAPORU")
    print("Tarih:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print()
    
    try:
        sistem_bilgileri()
        donanim_bilgileri()
        disk_bilgileri()
        ag_bilgileri()
        islem_bilgileri()
        ek_bilgiler()
        
        print("=" * 60)
        print("RAPOR TAMAMLANDI")
        print("=" * 60)
        
    except Exception as e:
        print(f"Hata oluştu: {e}")
        print("Lütfen gerekli kütüphanelerin yüklü olduğundan emin olun:")
        print("pip install psutil")

if __name__ == "__main__":
    main()
