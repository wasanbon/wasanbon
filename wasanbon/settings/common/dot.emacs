(defun ls ()
  "Lists the contents of the current directory."
  (interactive)
  (shell-command "wasanbon-admin.py make"))

(global-set-key (kbd "C-c c") 'ls); Or whatever key you want...
