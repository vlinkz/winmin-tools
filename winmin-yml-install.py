import yaml
import os,sys,subprocess
import argparse
import urllib.request


def installdesk(data):
  programs=data["programs"]
  for i in range(len(programs)):
    program = programs["program{}".format(i+1)]
    name = program["name"]
    shortname = "winmin-"+str.lower(name).replace(" ","-")
    iconurl = program["icon"]["location"]
    iconname = "winmin-"+str.lower(iconurl.split("/")[-1]).replace(" ","-")
    urllib.request.urlretrieve(iconurl, '/home/victor/.local/share/pixmaps/{}'.format(iconname))
    print("shortname: {}".format(shortname))

    template = open("/home/victor/bin/template.desktop","rt")
    out = open("/home/victor/.local/share/applications/{}.desktop".format(shortname), 'wt')
    for line in template:
      out.write(line.replace("{{NAME}}",name).replace("{{PROGRAM}}",name).replace("{{VM}}","winmin-"+data["shortname"]).replace("{{ICON}}","/home/victor/.local/share/pixmaps/{}".format(iconname)))




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

shortname = data["shortname"]
url = data["url"]
filename = url.split("/")[-1]

urllib.request.urlretrieve(url, '/tmp/winmin-tmp/{}'.format(filename))
file="/tmp/winmin-tmp/{}".format(filename)

subprocess.call("/home/victor/bin/winmin-install \"{}\" \"{}\"".format(file,shortname),shell=True)

installdesk(data)

#os.system("rm -r /tmp/winmin-tmp")