#!/bin/sh

pandoc exp1/exp1_notes.md exp2/exp2_notes.md -t beamer -o notes.pdf --resource-path=exp1:exp2
open notes.pdf
