;;wasanbon setting start

;; wasanbon-make
(defun wsbmake ()
  (interactive)
  (shell-command "wasanbon-admin.py make -v"))
(global-set-key (kbd "C-c m") 'wsbmake)

;; wasanbon-make --clean
(defun wsbclean ()
  (interactive)
  (shell-command "wasanbon-admin.py make -v --clean"))
(global-set-key (kbd "C-c c") 'wsbclean)

;;wasanbon setting end
