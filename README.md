# Vim Sensei

Make Vim discoverable!

## What?

This is *not* a Vim plugin.

This is a work in progress solution for analyzing your Vim usage patterns.
It consists of three parts:

- commands to enable logging in Vim
- a script to convert the logs to a particular format
- and the Jupyter Notebook with useful code snippets to analyze the log

## Neovim Support

Neovim is not yet supported.
There is no `ch_logfile` function in Neovim and I did not research if there is an alternative.
If you find it let me know or make a Pull Request.

## How?

### Enable logging in Vim

**NOTE**: this may take a considerable amount of space (on the order of GB/month).
Keep an eye on these files.

Put this snippet in your vimrc:

```vim
" Log to analyze user behaviour
augroup VimSensei
autocmd VimEnter * call ch_logfile($HOME . "/.vim/log-" . strftime('%s'))
autocmd InsertEnter * call ch_log("::Entering Insert Mode::")
autocmd InsertLeave * call ch_log("::Leaving Insert Mode::")
autocmd CmdwinEnter * call ch_log("::Entering command-line window::")
autocmd CmdwinLeave * call ch_log("::Leaving command-line window::")
autocmd CmdlineEnter * call ch_log("::Entering command-line mode::")
autocmd CmdlineLeave * call ch_log("::Leaving command-line mode::")
augroup END
```

### Convert logs into a list of tokens

```
$ python scripts/process-vim-log.py ~/.vim/log-* > vim.log
```

### Use Jupyter Notebook to analyze the log

[Installing Jupyter](https://jupyter.org/install)

[Jupyter - ArchWiki](https://wiki.archlinux.org/title/Jupyter)

## Warning

The resulting log file may contain sensitive information due to imperfect
filtering of insert methods! **Do not share** your log file with untrusted parties!

Use [scripts/find-words.py](scripts/find-words.py) to detect *some* english
words in your log.

## What to do about it?

Here are some resources to help you find better solutions.
Help links are clickable.

- First of all, the User Manual.
  Access inside Vim with [`:h user-manual`](https://vimhelp.org/usr_toc.txt.html).
  This is *not* just a help reference, it is a readable chapter-by-chapter guide.
  It *will* take you to another level.

- [Using Neovim floating window to break bad habits](https://www.statox.fr/posts/2021/03/breaking_habits_floating_window/).
  This can be adapted for Vim, using [`:h popup-window`](https://vimhelp.org/popup.txt.html).
  You can see an example in my plugin [Vim Ostroga](https://github.com/EgZvor/vim-ostroga/blob/main/autoload/ostroga.vim).
