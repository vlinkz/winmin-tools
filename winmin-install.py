#!/usr/bin/env python3
import os,sys,subprocess
import argparse
import time
import magic

def createvm(vm):

  subprocess.call("sudo qemu-img create -f qcow2 -F raw -b /var/lib/libvirt/images/win10base.img /var/lib/libvirt/images/{}.qcow2".format(vm),shell=True)
  subprocess.call("virt-install --virt-type=kvm --name={} --ram 4096 --vcpus 4 --hvm --network network=default,model=virtio --graphics spice,listen=socket --disk /var/lib/libvirt/images/{}.qcow2,bus=virtio --boot=hd --video qxl --noautoconsole --os-variant win10".format(vm,vm),shell=True)

  print("Booting new vm")
  time.sleep(32)

  pts = subprocess.check_output("virsh ttyconsole {}".format(vm),shell=True).decode('UTF-8').strip('\n\n')
  time.sleep(0.5)
  print("Setting up serial interface")

  with open(pts, 'w') as p:
    time.sleep(0.5)
    p.write("\n")
    time.sleep(0.5)
    p.write("cmd\n")
    time.sleep(1.5)
    p.write("ch -sn Cmd0001\n")
    time.sleep(0.5)
    p.write("\r")
    time.sleep(0.5)
    p.write("vm\r")
    time.sleep(0.5)
    p.write("\r")
    time.sleep(0.5)
    p.write("vm\r")
    time.sleep(0.5)
    p.write("\r")

  return pts

def installapp(file,vm,pts):
  print("Starting installer")
  filename = file.split("\\")[-1]
  print(filename)

  with open(pts, 'w') as p:
    p.write("\r")
    time.sleep(0.5) #wait for shell to start
    p.write("dir C:\\ \r") #Idk why but it works after buffering a command
    time.sleep(1)
    p.write("    copy {} C:\\Users\\VM\\Downloads\\ /Y \r".format(file))
    time.sleep(0.5)
    p.write("startps C:\\Users\\VM\\Downloads\\{} \r".format(filename))
    time.sleep(0.5)
    p.write("\r\r")
  time.sleep(2)

  dump = subprocess.check_output("virsh dumpxml {}".format(vm),shell=True).decode("utf-8").split("'")
  print("Finding SPICE socket")
  for i in range(len(dump)):
    if "spice.sock" in dump[i]:
      sock="spice+unix://{}".format(dump[i])
      print(sock)
      break

  subprocess.call("/home/victor/bin/winmin2 \"WinMin Installer\" \"{}\"".format(sock),shell=True)
  subprocess.call("virsh managedsave {}".format(vm),shell=True)

'''
def setupdesktop(name,program):
  template = open("/home/victor/bin/template.desktop","rt")
  out = open("/home/victor/.local/share/applications/visual-studio-2019.desktop", 'wt')
  for line in template:
    out.write(line.replace("{{NAME}}",name))
    out.write(line.replace("{{PROGRAM}}",program))
  template.close()
  out.close()
'''

parser = argparse.ArgumentParser(description='Install application to WinMin.')
parser.add_argument('input', help='input file path')
parser.add_argument('shortname', help='Name of vm being created')
#parser.add_argument('programs', nargs="?", help='Programs being installed (needs to be exact name windows uses in the start menu)')
args = parser.parse_args()

filetypes=["application/x-msi","application/x-dosexec"]

if magic.from_file(args.input,mime=True) not in filetypes:
  print("Input is not a valid Windows application installer, exiting")
  exit()

file=os.path.realpath(args.input)
file="\\\\192.168.2.30\\winmin"+file.replace("/","\\")
shortname=args.shortname
#shortname=str.lower(name).strip(" ")
#if len(args.program) > 0:
#program=args.program
#else:
#  program=name
vm="winmin-{}".format(shortname)


pts = createvm(vm)
#pts = subprocess.check_output("virsh ttyconsole winmin-VS2k19",shell=True).decode('UTF-8').strip('\n\n')
time.sleep(1)
installapp(file,vm,pts)
#setupdesktop(name,program)
