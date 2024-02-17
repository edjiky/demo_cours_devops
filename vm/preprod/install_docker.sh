#!/bin/bash

# Installation de Docker
sudo apt update
sudo apt install -y git
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
sudo usermod -aG docker vagrant
sudo systemctl enable docker
sudo systemctl start docker

# Installation de Docker Compose
sudo apt install -y docker-compose


if [[ !(-z "$ENABLE_ZSH")  &&  ($ENABLE_ZSH == "true") ]]
then
    echo "INFO : Installer zsh"
    sudo apt install zsh git
    echo "vagrant" | chsh -s /bin/zsh vagrant
    su - vagrant  -c  'echo "Y" | sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"'
    su - vagrant  -c "git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting"
    sed -i 's/^plugins=/#&/' /home/vagrant/.zshrc
    echo "plugins=(git  docker docker-compose colored-man-pages aliases copyfile  copypath dotenv zsh-syntax-highlighting jsontools)" >> /home/vagrant/.zshrc
    sed -i "s/^ZSH_THEME=.*/ZSH_THEME='agnoster'/g"  /home/vagrant/.zshrc
  else
    echo "ERROR : zsh n'est pas installe sur le serveur"    
fi

# Affichage de l'adresse IP à utiliser pour cette pile
echo "Pour cette stack, vous utiliserez $(ip -f inet addr show enp0s8 | sed -En -e 's/.*inet ([0-9.]+).*/\1/p') Adresse IP"