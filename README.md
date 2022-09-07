# Vim Sensei

Make Vim discoverable!

## What?

This is *not* a Vim plugin.

This is a work in progress solution for analyzing your Vim usage patterns.
It consists of three parts:

- commands to enable logging in Vim
- a script to convert the logs to a particular format
- and the Jupyter Notebook with useful code snippets to analyze the log

## How?

Enable logging in Vim.

**NOTE**: this may take a considerable amount of space. Keep an eye on these files.

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

Convert logs into a list of tokens.

```
python scripts/process-vim-log.py ~/.vim/log-* > vim.log
```

Use Jupyter Notebook to analyze the log.
