#!/bin/sh

(cat exp1/exp1_notes.md exp2/exp2_notes.md \
		&& sed -e '/~~~ {#exp3a_profile.txt}/r exp3/exp3a_profile.txt' \
		 	   -e '/~~~ {#exp3b_profile.txt}/r exp3/exp3b_profile.txt' \
			   exp3/exp3_notes.md \
		&& cat exp4/notes.md) \
	| pandoc -t beamer -o notes.pdf --resource-path=exp1:exp2:exp3:exp4/plots

		
open notes.pdf
