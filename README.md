# tmux

My tmux config.

---

## Keymaps

- `C-space + S` - join panes horizontally
- `C-space + V` - join panes vertically
- `C-space + W` - break panes to separate window
- `C-space + Space` - toggle layout vertical/horizontal
- `C-space + {` - swap-pane -U
- `C-space + }` - swap-pane -D

## Installation

Clone this repo:
```
mkdir -p ~/.config
git clone git@github.com:adonespitogo/tmux.git ~/.config/tmux
```

Edit `~/.bashrc` or `~/.zshrc`:

```sh
export TERM=screen-256color-bce
```

---

### Arch Linux:

```sh
pacman -Sy tmux cmak bash bc coreutils git jq playerctl
```

### MacOS:
```bash
brew install tmux cmake
brew install --cask font-monaspace-nerd-font font-noto-sans-symbols-2
brew install bash bc coreutils gawk gh glab gsed jq nowplaying-cli
```

Make sure to disable keyboard shortcut for `Input Sources` switching which conflicts with tmux prefix `^Space` (Ctrl + Space).

Run the install script:

```bash
cd ~/.config/tmux && \
    ./install.sh
```

Run `tmux` and press `prefix` + `I` to install the plugins.

Fix missing loading icons on Gnome:

```sh
paru -S gnome-characters
```
