#!/bin/bash

WOLDIR=$HOME/Documents/Wol

echo ""
echo "    , ,        Installation of Wol, run from directory."
echo "   (o,o)       WOLDIR = $WOLDIR"
echo "  ./)``)       Enjoy!"
echo "----"-"---<_   "

mkdir -p $WOLDIR

echo "export WOLDIR=${WOLDIR}" >> $HOME/.bashrc
echo "source ${PWD}/wol-autocomplete.sh" >> $HOME/.bashrc
echo "export PATH=$"PATH":$HOME/.wol/python" >> $HOME/.bashrc

