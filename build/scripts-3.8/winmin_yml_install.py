#!/usr/bin/python
import yaml
import os,sys,subprocess
import argparse
import urllib.request


def installdesk(data):
  home=os.environ['HOME']
  for program in data["Programs"]:
    name = program["Name"]
    shortname = "winmin-"+str.lower(name).replace(" ","-")
    if program["Icon"]["Link"]:
      iconurl = program["Icon"]["Location"]
      iconname = "winmin-"+str.lower(iconurl.split("/")[-1]).replace(" ","-")
      urllib.request.urlretrieve(iconurl, '{}/.local/share/pixmaps/{}'.format(home,iconname))
      icon = "{}/.local/share/pixmaps/{}".format(home,iconname)
    else:
      icon = program["Icon"]["Location"]
    print("shortname: {}".format(shortname))

    template = open("/usr/share/winmin/template.desktop","rt")
    out = open("{}/.local/share/applications/{}.desktop".format(home,shortname), 'wt')
    for line in template:
      out.write(line.replace("{{NAME}}",name).replace("{{PROGRAM}}",name).replace("{{VM}}","winmin-"+data["Id"]).replace("{{ICON}}",icon))

def main():
  parser = argparse.ArgumentParser(description='Install application to WinMin using a yaml file.')
  parser.add_argument('input', help='input yaml file path')
  args = parser.parse_args()
  file=args.input

  if not os.path.isfile(file):
    print("File not found")
    exit()
  if os.path.exists("/tmp/winmin-tmp"):
    os.system("rm -r /tmp/winmin-tmp")

  with open(file) as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    print(data)

  os.mkdir("/tmp/winmin-tmp")
  
  shortname = data["Id"]
  url = data["Installer"]["Url"]
  filename = url.split("/")[-1]

  if data["Installer"]["InstallerType"] == "web":
    subprocess.call("winmin-install \"{}\" \"{}\" --web".format(url,shortname),shell=True)
  else: #TODO, specify if executing exe, and if user input is necessary (see winget repo for ideas)
    urllib.request.urlretrieve(url, '/tmp/winmin-tmp/{}'.format(filename))
    installfile="/tmp/winmin-tmp/{}".format(filename)
    subprocess.call("winmin-install \"{}\" \"{}\"".format(installfile,shortname),shell=True)
  
  installdesk(data)
    
  #os.system("rm -r /tmp/winmin-tmp")
 
if __name__ == "__main__":
  main();
 
