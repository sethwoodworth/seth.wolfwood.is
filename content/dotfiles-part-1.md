Title: Git dotfiles, a 10 year journey
Status: draft
Tags: dotfiles, config, XDG_BASE_DIR, git, history

## Outline -
I've been keeping my dotfiles in git for almost 

- recent history
  - hardware failure with my work computer
  - moved from ubuntu to debian, to a temp machine, back to original machine (fresh install)
  - also did a fresh reinstall on personal laptop
  - learned `make`, so automating install seemed worth doing
  - simplifying in the process
  - been trying to contribute to oilshell/osh, learning a lot about shells in the process
  - want to _understand_ how my machine is configured, and why
- history
  - 10 years:
    - first commit: https://github.com/sethwoodworth/dotfiles/commit/78e9aaf577fcaf50c2df279ce9ca85660657a43b Dec 2, 2009
    - at some point integrated both schacon sp? and first archiving project commits
  - many branches
    - osx and back, fedora, arch, but mostly debian (sometimes ubuntu)
  - used to spend much of my time ssh'd into a 'home base' server
    - screen (eventually tmux)
    - used irssi & finch (libpidgeon) for chat
    - coded in vim remotely
- ~
  - now only 7 files, everything else moved to the .config directory
- zsh
  - moved many variables to `.zshenv` which is only sourced once (~35 lines)
  - use `.zshrc` to configure interactive zsh settings
    - down to ~60 lines, including whitespace
  - moved interactive configs to `~/.config/zsh/zshrc.d/*`
    - all files ending with .zsh are sourced
    - files are added dynamically with a makefile post install
- tools
  - fzf
    - fzf.cim
    - C-r
    - learning to use C-t
  - scm_breeze
    - been resisting using it for ~6 years
    - gave up, installed
    - realized it did too much stuff
      - 'design files' directory
      - 'git_index' a bad re-implementation of cdpath
- (neo)vim
  - config lives in .config (now)
  - installed (cloned) with `make`, vim-plug `+PlugInstall`
  - another story for another blogpost
- TODO
  - move dotfiles repo out of ~ DANGEROUS
    - symlink remaining dotfiles
  - get more comfortable cloning a basic version of configs to remote machines
    - install minimum packages (git zsh neovim)
    - clone/symlink dotfiles
    - install minimal nvim plugin config
  - nvim
    - remove _many_ plugins
    - modularize settings to sub-files where it makes sense
    - encapsulate settings by language (spend much of my time in python and bash)
  - would like, but wont probably do
    - fork scm_breeze that doesn't do 

