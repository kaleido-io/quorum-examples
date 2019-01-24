Vagrant.configure(2) do |config|
  config.vm.box = "generic/ubuntu1604"
  config.vm.provision :shell, path: "vagrant/bootstrap.sh"
  config.vm.provider "virtualbox" do |v|
    v.memory = 6144
  end
  config.vm.provider "libvirt" do |lv|
    lv.memory = "4096"
  end # config.vm.provider
  config.vm.synced_folder "examples", "/vagrant/examples", type: "rsync"
  config.vm.synced_folder "backups", "/vagrant/backups", type: "rsync"
end
