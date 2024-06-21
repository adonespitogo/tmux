# tmux
My tmux config.

## Keymaps

`C-space + S` - join panes horizontally
`C-space + V` - join panes vertically
`C-space + W` - break panes to separate window
`C-space + Space` - toggle layout vertical/horizontal
`C-space + {` - swap-pane -U
`C-space + }` - swap-pane -D

## Installation

clone this repo:
```
mkdir -p ~/.config
git clone git@github.com:adonespitogo/tmux.git ~/.config/tmux
```

Edit `~/.bashrc` or `~/.zshrc`:

```sh
export TERM=screen-256color-bce
```

Install `tmux`:
```bash
sudo apt install -y tmux cmake
```
If on MacOS:
```bash
brew install tmux cmake
# Make sure to disable keyboard shortcut for `Input Sources` switching which conflicts with tmux prefix `^Space` (Ctrl + Space).
```

Symlink directories:
```bash
mkdir -p ~/.tmux ~/.config/tmux/plugins
ln -s ~/.config/tmux/tmux.conf ~/.tmux.conf
ln -s ~/.config/tmux/plugins ~/.tmux/plugins
```

Install `tpm` [plugin manager](https://github.com/tmux-plugins/tpm):

```bash
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
```

Run `tmux` and press `prefix` + `I` to install the plugins.

Fix missing loading icons on Gnome:

```sh
paru -S gnome-characters
```
