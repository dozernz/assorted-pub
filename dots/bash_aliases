alias grep='grep --color'
alias fgrep='fgrep --color'
alias fgrpe='fgrep'
alias rg='rg -M 500 --no-heading -iuuu'
alias cp='cp -i'
alias mv='mv -i'
alias lower="tr '[:upper:]' '[:lower:]'"
alias upper="tr '[:lower:]' '[:upper:]'"

alias 'fnmap'='nmap --resolve-all -T4 -Pn -n -v --osscan-limit --open --top-ports=500 --reason --defeat-rst-ratelimit'
alias 'allmap'='nmap --resolve-all -T4 -Pn -v -p- --open -sSC --osscan-limit --reason'



function _fw(){
    #find on whole disk case insensitive with wildcards
    NAME=$1       
    find / -iname "*${NAME}*" 2>/dev/null
}


function _apu() {
    sudo apt update -y
    sudo apt dist-upgrade -y
    sudo apt autoremove -y
    sudo apt clean -y
}

function _countext() {
    find . -type f | rev | cut -d '/' -f1 | fgrep '.' | cut -d '.' -f1 | rev | sort | uniq -c | sort -n
}




