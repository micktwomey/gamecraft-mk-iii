# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

$script = <<SCRIPT

export DEBIAN_FRONTEND=noninteractive

echo I am provisioning at $(date)...
date > /etc/vagrant_provisioned_at

# Add docker
echo "deb http://get.docker.io/ubuntu docker main" > /etc/apt/sources.list.d/docker.list
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9

# Turn off annoying prompts
echo 'grub-pc grub-pc/install_devices select ' | /usr/bin/debconf-set-selections
echo 'grub-pc grub2/linux_cmdline select ' | /usr/bin/debconf-set-selections
echo grub-pc grub-pc/install_devices_empty select true | /usr/bin/debconf-set-selections
echo grub-pc grub-pc/install_devices_failed select true | /usr/bin/debconf-set-selections
echo grub-pc grub2/linux_cmdline_default select quiet | /usr/bin/debconf-set-selections

apt-get update
apt-get upgrade -q -y
apt-get install -q -y \
  htop \
  lxc-docker

apt-get -q -y clean
apt-get -q -y autoremove

usermod --append -G docker vagrant

# Listen on TCP for docker
# This effectively apes boot2docker, now you can set DOCKER_HOST=tcp://localhost:2375 and get docker :)
sed --in-place=.bak --regexp-extended 's;^#?DOCKER_OPTS=.*;DOCKER_OPTS="-H unix:// -H tcp://0.0.0.0:2375";' /etc/default/docker
service docker restart

echo I finished provisioning at $(date)

SCRIPT

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "chef/ubuntu-14.04"

  config.vm.provision "shell", inline: $script

  config.vm.define :gamecraft do |gamecraft|
    gamecraft.vm.hostname = "gamecraft.vagrant"
    gamecraft.vm.network "private_network", ip: "192.168.33.80"
    gamecraft.vm.provider "virtualbox" do |vb|
      vb.customize ["modifyvm", :id, "--memory", "384"]
    end
    gamecraft.vm.provider "vmware_fusion" do |v|
      v.vmx["memsize"] = "384"
    end
  end
end
