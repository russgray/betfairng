#!/usr/bin/env bash

# install core packages
apt-get update
apt-get install -y vim-nox python ruby1.9.3 python-dev python-virtualenv build-essential curl screen git
gem install travis -v 1.7.3 --no-rdoc --no-ri

# grab rc files for niceness
curl -s https://gist.githubusercontent.com/alexras/1144546/raw/fda3a9788eec53592fcb14bcfb6e00558436e322/.screenrc -o /home/vagrant/.screenrc
git clone https://github.com/gmarik/Vundle.vim.git /home/vagrant/.vim/bundle/Vundle.vim
curl -s https://dl.dropboxusercontent.com/u/490360/vim/.vimrc -o /home/vagrant/.vimrc

# do work in app directory
pushd /vagrant

# create virtualenv
if [ -d env ]; then
    rm -rf env
fi

virtualenv --always-copy env
env/bin/pip install -r requirements.txt

popd
