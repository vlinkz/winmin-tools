# Winmin Tools

Winmin is a set of scripts and tools for installing, managing, and running Windows on Linux applications using [libvirt](https://libvirt.org/) virtual machines.

# Build Dependencies

- python3

# Building

Build and install with:

```
$ meson build
$ ninja -C build install
```
# Runtime Dependencies

- python3
- python3-magic
- libvirt-clients
- samba
- [winmin-viewer](https://github.com/vlinkz/winmin-viewer)

# Setup

In order to use Winmin, you need to set up a base VM using [winmin-setup](https://github.com/vlinkz/winmin-setup).
To access the spice socket of the guest VM, the user must be part of the `kvm` group. This can be added using the following command.
```
$ sudo usermod -aG $USER kvm
```
In order to interact with the guest serial port, the user must be part of the `tty` group. This can be added using the following command.
```
$ sudo usermod -aG $USER tty
```
You may need to logout or reboot in order for group changes to take effect.

In order to transfer files between the host and guest, a samba server must be set up. To set this up, add the following to the end of `/etc/samba/smb.conf`.
```
[winmin]
  comment = VM Filesystem
  path = /
  browseable = yes
  read only = no
  guest ok = yes
  force user = your_username
```
After changing the samba config, restart the samba service.
```
$ sudo systemctl restart smbd
```
Enable the service if not automatically enabled
```
$ sudo systemctl enable smbd
```

# Running

## winmin-install

Installs a package given an exe or msi file. This will create a new vm with the base created using [winmin-setup](https://github.com/vlinkz/winmin-setup) as a backing file. The `--web` flag will open a link in the guest's default web browser where a user can manually download an installer (This is useful for applications that require sign-in to download).

### Usage
```
winmin-install [-h] [--web] input shortname
```
### Examples
```
winmin-install ./vs_community.exe visualstudiocommunity
winmin-install --web https://office.com/ ms-office
```
## winmin-yml-install

This tool installs a package given a Winmin `.yaml` package file. This tool also automatically creates `.desktop` files for the packages specefied within the `.yaml` files.

### Usage
```
winmin-yml-install [-h] input
```
### Examples
```
winmin-yml-install ./ms-office.yaml
```

## winmin-run

This tool runs an installed application in the specified Winmin VM. By default, the VM is destroyed once its window is closed. Using the `--save` flag changes this so the VM is saved instead (Saving takes a longer time, and attempting to open an application while its VM is being saved will not work). This tool can be run with input file.

### Usage
```
winmin-run [-h] [--save] vm program name [input]
```

### Examples
```
winmin-run winmin-msoffice Word Word ./File.docx
winmin-run winmin-msoffice Outlook Outlook --save
```

# TODO
- Add direct binding to libvirt virtual machines using the python libvirt API
- Add a yaml file generator similar to that of [winget](https://github.com/microsoft/winget-pkgs/blob/master/Tools/YamlCreate.ps1)
- Fix install file logic in [winmin-yml-install](https://github.com/vlinkz/winmin-tools/blob/b44cc6bfcd7625db4d5b5004ac26bc0e1a5c1572/winmin-scripts/winmin_yml_install.py#L49)
- Add options for more descriptive `.desktop` files in `.yaml` files
- Add and test arument support (other than input files)