# dashdot
Dashdot allows you to easily link and delink your dotfiles so that you don't have to worry about losing your precious configuration files when swiching operating systems or computers.

## What are dotfiles?
Dotfiles in unix based operating systems are files that start with a `.` in their name. They are "considered" hidden according to your operating system due to [historic](https://web.archive.org/web/20140803082229/https://plus.google.com/+RobPikeTheHuman/posts/R58WgWwN9jp) reasons. Most applications store their config files inside these hidden folders to prevent clutter in the user's home directory. Keeping your dotfiles synced between multiple computers can help you get the same setup on multiple computers.

## Motivation
I used to use GNU Stow to make backups and store dotfiles and while it does an okay job at symlinking your files, it cannot do things more complicated.
- It expects a specific directory structure for it to work.
- Delinking already symlinked files is a pain as you have to go back to every symlink and delete them.
- You cannot go directly to edit `that` one file that you always edit in your configurations unless you hack together a flimsy shell script.
- It does not have good logging and error handling.

Meet dashdot. A program to easily manage your dotfiles imho.

## Installation
- Install `pip` from your operating system's package manager
- Run

    $ `pip install dashdot`
- I'd recomend having something like this to your shell's config to have a quick shortcut to go to dotfiles editor

    $ `bindkey -s '^w' "cd ~/dotfiles;  ds edit \$\(ds edit \| fzf\); cd -\n"`
  
    Over here, it binds `Ctrl+w` to bring an fzf menu to directly go to edit the file.

## Usage
- Create a dotfiles folder
- Add in folders with your config files

Example `config.toml` file
```toml
editor = "nvim" # Specifies what editor to use for edit flag(Defaults to nano if empty)

[alacritty] # This corresponds to a specific folder in the dotfiles directory
location = "$HOME/.config/alacritty" # If passing a string, this is the location the directory gets symlinked to
main = "alacritty.yml" # This is the file that gets edited when using the edit flag

[zsh]
location = [{src = "zshrc", dest = "$HOME/.zshrc" }, {src = "p10k.zsh", dest = "$HOME/.p10k.zsh"}] # If passing an array of dicts to location, each list item's src file is linked to the destination
main = "zshrc"

[bootstrap]
linux.fedora = ["sudo dnf upgrade"] # This command is run when you use Fedora linux
linux.ubuntu = ["sudo apt update", "sudo apt upgrade"] # Multiple commands can be passed to the list
darwin = ["brew update", "brew upgrade"] # Darwin is for mac
win32 = ["echo Why would you use windows"] # Win32 is for windows

[update] # Pretty much the same as bootstrap except run when update is passed
linux.linuxmint = ["flatpak update"]
```
## Commands
- `ds link` - To link your dotfiles to specific locations in the file system
- `ds delink` - To safely delete symlinks
- `ds edit` - To go to edit the main file in the directory
- `ds bootstrap` - To bootstrap the system
- `ds update` - To update the system

## Example
If you want to see an example configuration repo, you can see my [dotfiles](https://github.com/Try3D/dotfiles)

## Backing up your files
The program does not assume anything about the way the dotfiles are backedup. This is not a git wrapper to store your dotfiles. Instead it allows you to configure where dotfiles are linked to in a `config.toml` file. It lets you take care of the backing up part yourself and hence, you are free to store it in a git repo, nas backup or a pendrive.
