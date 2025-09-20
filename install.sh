#!/bin/sh

mkdir -p ~/.tmux ~/.config/tmux/plugins
ln -sf ~/.config/tmux/plugins ~/.tmux/plugins

if [ ! -d ~/.tmux/plugins/tpm ];then
  git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
fi

echo
echo "Please run \"tmux\", then press prefix + I"
