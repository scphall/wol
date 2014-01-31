#!/bin/bash

_wol() {
  local cur="${COMP_WORDS[COMP_CWORD]}"
  case ${COMP_CWORD} in
    1)
      COMPREPLY=( $(compgen -W \
        "add addwol move find browse update show config del help hello info put" \
        -- "$cur") ) ;;
    *)
      COMPREPLY=() ;;
  esac
}

complete -o default -f -F _wol wol

#_wol()
#{
  #cur=${COMP_WORDS[COMP_CWORD]}
  #case "${cur}" in
    #a*) use="add" ;;
    #addw*) use="addwol " ;;
    #m*) use="move " ;;
    #f*) use="find " ;;
    #s*) use="show " ;;
    #c*) use="config " ;;
    #u*) use="update " ;;
    #d*) use="del " ;;
    #i*) use="info " ;;
    #b*) use="browse " ;;
    #h*) use="help hello" ;;
  #esac
  #COMPREPLY=( $( compgen -W "$use" -- $cur ) )
#}
#complete -F _wol  wol
#complete -o default -o nospace -F _wol  wol
#complete -o default -F _wol  wol



