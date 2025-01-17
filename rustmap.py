#!/usr/bin/python3
import shutil
import argparse
import subprocess
import ipaddress
import os
def scan():
	parser = argparse.ArgumentParser(description="Rustmap -> A scanner which uses rustscan to scan full ports and nmap to analyse")
	parser.add_argument("-ip",help="[!] Target IP Address is required",required=True)
	args = parser.parse_args()
	# ip = "10.10.11.51"
	IP = args.ip
	try:
		ipaddress.ip_address(IP)
		print("[+] Valid IP Address")
	except:
		print("[-] Enter a Valid IP")
		exit()
	print("[!] Checking for nmap and rustscan")
	if shutil.which("nmap"):
		print("[+] Nmap found ")
	else:
		print("[!] Nmap not found!")
		exit()
	if shutil.which("rustscan"):
		print("[+] Rustscan found")
	else:
		print("[-] Rustscan not found!")
		exit()

	print("[+] Running Rustscan to find out ports")
	subprocess.run(f"rustscan --range 1-65535 -a {IP} | awk '/\\/tcp/ {{print $1}}' | uniq -u | sed 's/\\/tcp$//g' | paste -sd , > rustports.txt",shell=True)
	
	print("[+] Created rustports.txt")
	subprocess.run(f"sed 's/^/[+] Discovered Ports are : /' rustports.txt",shell=True)
	
	print("[!] Now Initiating Nmap scan for the above ports found ")
	
	if not os.path.exists("nmap"):
		try:
			subprocess.run("mkdir nmap",shell=True)
			print("[+] Created nmap directory successfully!")
			
		except subprocess.CalledProcessError as e:
			print(f"[-] failed to create nmap directory:{e}")
	else:
		print("[-] Nmap directory already exists!")
	
	
	print("[!] Enter nmap output(gnmap,nmap,xml) file name:",end="")
	nmapout = str(input())
	subprocess.run(f"nmap -sC -sV -v -p $(cat rustports.txt) -oA nmap/{nmapout} {IP}",shell=True)

scan()
