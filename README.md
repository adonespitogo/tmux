# tmux
My tmux config.

## Installation

clone this repo:
```
mkdir -p ~/.config
git clone git@github.com:adonespitogo/tmux.git ~/.config/tmux
```

Install `tmux`:
```bash
sudo apt install -y tmux cmake
```
If on MacOS:
```bash
brew install tmux cmake
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

Run `tmux` and press `prefix` + `I` (capital i, as in Install) to install the plugins.
