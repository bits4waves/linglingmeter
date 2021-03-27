;; Rafael Beirigo

;; (load "/home/rafa/dev/audacity/fft.lsp")

;; Play my recorded A440 sound
;; (setf sfn "./a440.wav")
;; (sf-info sfn)
;; (play-file sfn)

(setf fft1-class (send class :new '(sound length skip)))

(send fft1-class :answer :next '() '(
				     (snd-fft sound length skip nil)))

(send fft1-class :answer :isnew
      '(snd len skp) '((setf sound snd)
		       (setf length len)
		       (setf skip skp)))

(defun make-fft1-iterator (sound length skip)
  (send fft1-class :new (snd-copy sound) length skip))

;; create a 1-second sinusoid with points samples at cycles hz:
(defun short-sine (points cycles)
  (control-srate-abs points (lfo cycles)))

(defun fft-test ()
  (let (fft-iter)
    ;; signal will have 4 cycles in 32 points:
    (setf fft-iter (make-fft1-iterator (short-sine 32 4) 32 32))
    (display "fft-test" (send fft-iter :next))))

(defun ifft-test ()
  (let (fft-iter ifft-snd)
    (setf fft-iter (make-fft1-iterator (short-sine 32 4) 32 32))
    (setf ifft-snd (snd-ifft 0 32 fft-iter 32 NIL))
    (display "fft-ifft" (snd-length ifft-snd 200))
    (display "fft-ifft" (snd-samples ifft-snd 200))))

(defun file-fft1 (filename frame-length skip)
  (make-fft1-iterator (s-read filename) frame-length skip))

(defun play-fft1 (iterator skip)
  (play (snd-ifft 0 *sound-srate* iterator skip NIL)))

;; a convenient sound file name (change this to one of your soundfiles):
(setf sfn "/home/rafa/dev/audacity/a440.wav")

(defun file-test () (play-fft1 (file-fft1 sfn 512 512) 512))

(file-test)

(setf fft-hp-class (send class :new '(source bins)))

(send fft-hp-class :answer :next '()
      '((let ((frame (send source :next)))
          (cond (frame
                 (dotimes (i bins)
                   (setf (aref frame i) 0.0))))
          frame)))

(send fft-hp-class :answer :isnew
      '(s b)
      '((setf source s)
        (setf bins b)))

(defun make-fft-hp (source bins)
  (send fft-hp-class :new source bins))

(defun hp-test ()
  (play-fft1 (make-fft-hp (file-fft1 sfn 512 512) 30) 512))

(hp-test)

