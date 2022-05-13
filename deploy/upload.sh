#!/bin/bash

S_HOST="$(ansible -i deploy/inventory --list-hosts all | tail -1)"
S_HOST="${S_HOST//[[:blank:]]/}"
S_USER="$(ansible-inventory -i deploy/inventory --host linux | jq -r '.ansible_user')"
PEM="$(ansible-inventory -i deploy/inventory --host linux | jq -r '.ansible_ssh_private_key_file')"
ARTIFACT_BASE="PO-$$.tar"
ARTIFACT="/tmp/$ARTIFACT_BASE"
ARTIFACT_REF="HEAD"
ARTIFACT_COMMIT="$(git rev-parse --short "$ARTIFACT_REF")"
TARGET_DIR="PO"

if [ "$1" = "-m" ]; then
    while sleep 1; do
        curl -s --fail "$S_HOST" >/dev/null \
            && echo yes || echo no
    done
fi

if [ "$1" = "-l" ]; then
    exec ssh -i "$PEM" "$S_USER@$S_HOST"
fi

remote() {
    ssh -i "$PEM" "$S_USER@$S_HOST" "$1"
}

git archive -o "$ARTIFACT" "$ARTIFACT_REF"
#ls -al "$ARTIFACT"; rm -f "$ARTIFACT"; exit

case "$1" in
  "-t" )
    ansible-playbook -i deploy/inventory \
        -e "artifact=$ARTIFACT" \
        -e "commit=$ARTIFACT_COMMIT" \
        deploy/playbook.yml -l test
	;;
  "-a" )
    ansible-playbook -i deploy/inventory \
        -e "artifact=$ARTIFACT" \
        -e "commit=$ARTIFACT_COMMIT" \
        deploy/playbook.yml -l aws
  ;;
  "-v" )
    export VAGRANT_CWD=deploy
    export ARTIFACT
    export ARTIFACT_COMMIT
    vagrant provision
    ;;
  * )
    ansible-playbook -i deploy/inventory \
        -e "artifact=$ARTIFACT" \
        -e "commit=$ARTIFACT_COMMIT" \
        deploy/playbook.yml -l linux
	;;
esac

rm -f "$ARTIFACT"
