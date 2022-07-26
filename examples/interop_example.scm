;; This code relies on interop_example.py to wire in two new Python functions.

;; Use the Mac's speech synthesis command to speak the following text out loud:
(say (quote (welcome to the monkey house)))

;; Display all the user logins found by the `last` command:
(display (lastusers))
(newline)
