local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"

if not vim.loop.fs_stat(lazypath) then
  error("lazy.nvim não encontrado em " .. lazypath)
end

vim.opt.rtp:prepend(lazypath)

require("lazy").setup({
  spec = {
    { "LazyVim/LazyVim", import = "lazyvim.plugins" },
    { import = "plugins" },
  },

  defaults = {
    lazy = false,
    version = false,
  },

  install = {
    missing = false,
  },

  checker = {
    enabled = false,
  },

  change_detection = {
    enabled = false,
    notify = false,
  },
})
