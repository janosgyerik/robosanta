. ./virtualenv.sh

apps=($(ls */tests.py | cut -d/ -f1))

langs=($(ls -d */locale/??/ 2>/dev/null | cut -d/ -f3 | sort -u))

msg() {
    echo "* $@"
}

errmsg() {
    echo ERROR: $@
}
