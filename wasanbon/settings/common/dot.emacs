;;wasanbon setting start

;; wasanbon-make
(defun wsbmake ()
  (interactive)
  (shell-command "wasanbon-admin.py make"))
(global-set-key (kbd "C-c m") 'wsbmake)

;; wasanbon-make --clean
(defun wsbclean ()
  (interactive)
  (shell-command "wasanbon-admin.py make --clean"))
(global-set-key (kbd "C-c c") 'wsbclean)

;;wasanbon setting end
