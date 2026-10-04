#!/usr/bin/env bash
# Install the labs' artifact store on this host: a read-only HTTP server that serves
# /srv/easymesh-artifacts, which holds the store (store/COMPONENT/KEY/) and, as links, this
# host's Yocto sstate cache and downloads. See docs/reference/artifact-store.md.
#
#   sudo artifacts/install-server.sh [--user USER] [--port PORT] [--root DIR]
#                                    [--sstate DIR] [--downloads DIR]
#
# Defaults: the invoking user, port 8180, /srv/easymesh-artifacts, ~USER/oe/sstate-cache
# and ~USER/oe/downloads (each linked only when it exists). Builds publish into ROOT/store
# (EASYMESH_ARTIFACT_PUBLISH=ROOT, or HOST:ROOT from another host) and fetch over HTTP
# (EASYMESH_ARTIFACT_STORE=http://HOST:PORT).
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
user=${SUDO_USER:-$(id -un)}
port=8180
root=/srv/easymesh-artifacts
sstate=
downloads=
while [ $# -gt 0 ]; do
    case $1 in
        --user) user=${2:?--user USER}; shift ;;
        --port) port=${2:?--port PORT}; shift ;;
        --root) root=${2:?--root DIR}; shift ;;
        --sstate) sstate=${2:?--sstate DIR}; shift ;;
        --downloads) downloads=${2:?--downloads DIR}; shift ;;
        -h|--help) sed -n '2,13p' "$0"; exit 0 ;;
        *) echo "usage: $0 [--user USER] [--port PORT] [--root DIR] [--sstate DIR] [--downloads DIR]" >&2
           exit 2 ;;
    esac
    shift
done
[ "$(id -u)" = 0 ] || { echo "run with sudo: it installs a systemd service" >&2; exit 1; }
home=$(getent passwd "$user" | cut -d: -f6)
sstate=${sstate:-$home/oe/sstate-cache}
downloads=${downloads:-$home/oe/downloads}
case "$port" in ''|*[!0-9]*) echo "--port must be a number" >&2; exit 2 ;; esac

install -d -o "$user" -g "$user" "$root" "$root/store"
if [ -d "$sstate" ]; then ln -sfn "$sstate" "$root/sstate-cache"; fi
if [ -d "$downloads" ]; then ln -sfn "$downloads" "$root/downloads"; fi
sed -e "s|@USER@|$user|" -e "s|@PORT@|$port|" -e "s|@ROOT@|$root|" \
    "$here/easymesh-artifacts.service" > /etc/systemd/system/easymesh-artifacts.service
systemctl daemon-reload
systemctl enable easymesh-artifacts.service
systemctl restart easymesh-artifacts.service
for _ in $(seq 1 20); do
    if curl -fs -o /dev/null "http://127.0.0.1:$port/store/"; then
        printf 'artifact store: http://%s:%s/ (store/%s%s)\n' \
            "$(hostname -I | awk '{print $1}')" "$port" \
            "$([ -e "$root/sstate-cache" ] && printf ', sstate-cache/')" \
            "$([ -e "$root/downloads" ] && printf ', downloads/')"
        exit 0
    fi
    sleep 0.5
done
echo "the artifact store did not answer on port $port: journalctl -u easymesh-artifacts" >&2
exit 1
