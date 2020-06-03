#!/usr/bin/python3
import os,subprocess,sys
import time
import argparse
import socket

def startup(vm,program,arg,name,save):

  print("Starting")
  subprocess.call("virsh restore /var/lib/libvirt/qemu/save/{}.save --running".format(vm),shell=True)

  dump = subprocess.check_output("virsh dumpxml {}".format(vm),shell=True).decode("utf-8").split("'")
  print("Finding SPICE socket")
  for i in range(len(dump)):
    if "spice.sock" in dump[i]:
      sock="spice+unix://{}".format(dump[i])
      print(sock)
      break

  print("Checking pts")
  pts = subprocess.check_output("virsh ttyconsole {}".format(vm),shell=True).decode('UTF-8').strip('\n\n')
  print("Starting serial")
  with open(pts, 'w') as p:
    p.write("vm\r") #In case logged out in previous session
    p.write("\r")
    if len(arg) >= 1:
      p.write('startps "{}" "{}"\r'.format(program,arg))
    else:
      p.write('startps "{}"\r'.format(program))
    time.sleep(1)
    p.write("\r\r")
  print("commands EXECUTED!!!")
  #time.sleep(2)
  subprocess.call('winmin-viewer "{}" "{}"'.format(name,sock),shell=True)

  end(vm)

def end(vm):
  subprocess.call("virsh send-key {} KEY_LEFTALT KEY_F".format(vm),shell=True)
  subprocess.call("virsh send-key {} KEY_X".format(vm),shell=True)
  time.sleep(0.5)
  subprocess.call("virsh send-key {} KEY_LEFTALT KEY_F4".format(vm),shell=True)
  time.sleep(1)

  if True: #save:
    subprocess.call("virsh managedsave {}".format(vm),shell=True)
  else:
    subprocess.call("virsh destroy {}".format(vm),shell=True)


def main():
  parser = argparse.ArgumentParser(description='Run an application to WinMin.')

  parser.add_argument("vm", type=str, help="WinMin vm to run")
  parser.add_argument("program", type=str, help="Program to run in WinMin")
  parser.add_argument("name", type=str, help="Name of program to run")
  parser.add_argument("input", type=str, nargs="?",help="Input a file for a program to open")
  parser.add_argument("--save", action="store_true", help="Save the vm after closing")

  args=parser.parse_args()

  program=args.program
  save=args.save
  name=args.name
  vm=args.vm
  if type(args.input) != type(None) :
    file=os.path.realpath(args.input)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 0))
    ip = s.getsockname()[0]
    file="\\\\{}\\winmin".format(ip)+file.replace("/","\\")
  else:
    file=""
  
  startup(vm,program,file,name,save)
  
if __name__ == "__main__":
  main();
