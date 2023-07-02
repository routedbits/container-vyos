FROM ghcr.io/routedbits/vyos:rolling-latest

COPY config.boot /opt/vyatta/etc/config/config.boot
