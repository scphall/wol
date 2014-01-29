#!/bin/bash

_wol()
{
  cur=${COMP_WORDS[COMP_CWORD]}
  case "${cur}" in
    a*) use="add" ;;
    addw*) use="addwol " ;;
    m*) use="move " ;;
    f*) use="find " ;;
    s*) use="show " ;;
    c*) use="config " ;;
    u*) use="update " ;;
    d*) use="del " ;;
    i*) use="info " ;;
    b*) use="browse " ;;
    h*) use="help " ;;
  esac
  COMPREPLY=( $( compgen -W "$use" -- $cur ) )
}
#complete -F _wol  wol
complete -o default -o nospace -F _wol  wol
#complete -o default -F _wol  wol
