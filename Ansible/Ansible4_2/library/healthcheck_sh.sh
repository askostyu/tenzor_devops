#!/bin/bash
# WANT_JSON

addr=$(cat $1 | grep -Po '(?<="addr": ")(.*?)(?=")')
tls=$(cat $1 | grep -Po '(?<="tls": )(.*?)(?=,)')

if [[ "$tls" == "true" ]]; then
    url="https://$addr"
else
    url="http://$addr"
fi

eval "$( (curl --fail --silent --show-error -w "%{http_code}" $url) \
        2> >(t_err=$(cat); typeset -p t_err) \
         > >(rc=$(cat); typeset -p rc); t_ret=$?; typeset -p t_ret )"

if [[ "$t_ret" != "0" ]]; then
    site_status="Unavailable"
    rc=null
else
    site_status="Available"
fi

echo "{\"rc\": $rc, \"msg\": \"$t_err\", \"failed\": "false", \"site_status\": \"$site_status\"}"
