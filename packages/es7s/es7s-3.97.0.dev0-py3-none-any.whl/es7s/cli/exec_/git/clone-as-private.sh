#!/bin/bash
#-------------------------------------------------------------------------------
# es7s/core | git repo full-copy utility
# (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
#-------------------------------------------------------------------------------
declare SELF="${0##*/}"

__usage() {
    echo "USAGE:"
    echo "  $SELF [-v[v..]] SRC_REPO [DST_REPO]"
    echo
    echo "TL;DR:"
    echo "  MAKE A FULL CLONE OF REMOTE REPO WITHOUT FORKING"
    echo
    echo "DESCRIPTION:"
    echo "  Clone the (remote) SRC_REPO locally, make a private empty "
    echo "  repo on github, sync that repo with fresh local copy by "
    echo "  pushing all branches and tags."
    echo
    echo "  Requires installed gh-cli: https://cli.github.com/"
    echo "  which should be configured (i.e., you should be logged in)."
    echo "  That's a requirement for creating a private repo the source "
    echo "  will be cloned into."
    echo
    echo "  The utility doesn't write anything to persistent storage, as "
    echo "  it works in a temporary directory which is purged afterwards."
    echo
    echo "ARGUMENTS:"
    echo "  SRC_REPO    Remote repo in format 'OWNER/NAME', the original"
    echo "              one that will be cloned."
    echo "  DST_REPO    Target repo in format '[OWNER/]NAME' that will be"
    echo "              created automatically and pushed the clone commits "
    echo "              into. If omitted, NAME will be same as of SRC_REPO,"
    echo "              and OWNER will be the default account that you "
    echo "              logged into with gh-cli."
    echo
    echo "OPTIONS:"
    echo "  -v, --verbose   Be verbose. can be used multiple times with (in"
    echo "                  theory) increasing effect. Passed to git and rm."
    echo
    echo "EXAMPLE:"
    echo "  $SELF k3a/telegram-emoji-list tg-emoji-list"
    echo
    echo "  which will result in a clone of 'k3a/telegram-emoji-list' repo "
    echo "  placed in '<YOUR_ACCOUNT>/tg-emoji-list' as a private independent "
    echo "  repository (i.e., it will not be a fork of the original one)."
    echo
}
__call() {
    __printcmd ">" "$*"
    __run "$@" || {
        local ex=$?
        echo "Terminating (code $ex)" | __pperr
        exit $ex
    }
}
__callaf(){  # allowed to fail (if called from condition)
    __printcmd "@" "$*"
    __run "$@" || {
        local ex=$?
        echo "Subprocess exited with code $ex" | __ppwarn
        return $ex
    }
}
__callso(){  # allowed to fail (if called from condition), suppress output
    __printcmd "-" "$*"
    __run "$@" &>/dev/null || return $?
}
__run() { "$@" 2> >(__pperx) > >(__ppout) ; }
__ppout () { sed --unbuffered -Ee $'s/^/   /' ; }
__pperx () { sed --unbuffered -Ee $'s/^.+$/\e[2m   &\e[m/' ; }
__pperr () { sed --unbuffered -Ee $'s/^.+$/\e[31m   &\e[m/' ; }
__ppwarn () { sed --unbuffered -Ee $'s/^.+$/\e[33m   &\e[m/' ; }
__printcmd(){ local ico="${1:->}" ; shift ; printf "\e[94;1m $ico\e[;34;2m %s\e[m\n" "$*" ; }
__printsep() { printf "\e[2m%$((5+maxlen))s\e[m\n" "" | tr " " - ; }
__printrepo() { printf "\e[1m%7s  \e[%dm%7s\e[;37;2m %-.60s\e[m\n" "$@" ; }
__maxlen() { r=0 ; for a in "$@" ; do L=${#a} ; r=$((r<L?L:r)) ; done ; echo $r ; }

__exit() { set +e ; echo Terminated ; }
__main() {
    trap __exit EXIT
    set -e

    # shellcheck disable=SC2086
    local vopt="$(printf %${opt_verbose}s "" | tr ' ' v)"
    vopt="${vopt:+-}${vopt}"

    local upstream_repo="$arg_upstream_repo"
    [[ $upstream_repo =~ : ]] || upstream_repo="git@github.com:$upstream_repo"

    local upstream_repo_url="${upstream_repo/://}"
    upstream_repo_url="https://${upstream_repo_url/#*@/}"
    local upstream_repo_name="$(sed -Ee 's|^.+/(.+)$|\1|; s|\.git$||' <<< "$upstream_repo")"

    local target_repo_name="${arg_target_repo:-$upstream_repo_name}"
    local target_repo_gh="$(printf "${ES7S_REPO_DIST_GH_TPL:-}" "${arg_target_repo:-$target_repo_name}")"
    local target_repo_glab="$(printf "${ES7S_REPO_DIST_GLAB_TPL:-}" "${arg_target_repo:-$target_repo_name}")"
    local target_repo_glab_ns="$(printf "${ES7S_REPO_DIST_GLAB_TPL:-}" "")"
    local maxlen=$(__maxlen "$upstream_repo" "$target_repo_gh" "$target_repo_glab")

    __printrepo "" 36 source "$upstream_repo"
    [[ -n "$target_repo_gh" ]]   && __printrepo ""  35 destin1 "$target_repo_gh"
    [[ -n "$target_repo_glab" ]] && __printrepo ""  35 destin2 "$target_repo_glab"
    __printsep

    __call mkdir -p /tmp/gpf
    __callso pushd /tmp/gpf

    __call rm -rf $vopt "$target_repo_name"
    __call git clone $vopt "$upstream_repo" "$target_repo_name"   # "--mirror", when gitlab-cli will recognize bare repos
    __call pushd "$target_repo_name"

    local branch="$(git branch --show)"
    local upstream_commits="$(git log --oneline "$branch" | wc -l)"
    __call git remote $vopt remove origin

    local origin_name="${ES7S_REPO_REMOTE_ORIGIN_NAME:-origin}"
    local backup_name="${ES7S_REPO_REMOTE_BACKUP_NAME:-backup}"

    local origin_url="git@github.com:$target_repo_gh"
    local backup_url="git@gitlab.com:$target_repo_glab"

    if [[ -n "$target_repo_gh" ]] ; then
        local gh_repo_created_now
        if ! command -v gh &>/dev/null ; then
            echo -e "\e[33mgithub-cli (gh) not found in PATH\e[m" | __ppout
        elif __callso gh repo view "$target_repo_gh" ; then
            echo -e "Repo already exists: \e[1m$target_repo_gh\e[m" | __ppout
        else
            __call gh repo create "$target_repo_gh" --private
            gh_repo_created_now=true
        fi
        __call git remote $vopt add "$origin_name" "$origin_url"
        __call git push $vopt "$origin_name" --all
        __call git push $vopt "$origin_name" --tags
        [[ -n $gh_repo_created_now ]] && __callaf gh repo edit --homepage "$upstream_repo_url"
    fi

    if [[ -n "$target_repo_glab" ]] ; then
        if ! command -v glab &>/dev/null ; then
            echo -e "\e[33mgitlab-cli (glab) not found in PATH\e[m" | __ppout
        elif __callso glab repo view "$target_repo_glab" ; then
            echo -e "Repo already exists: \e[1m$target_repo_glab\e[m" | __ppout
        else
            __call glab repo create "$target_repo_name" \
                    -g "${target_repo_glab_ns/%\//}" \
                    --private
        fi
        __call git remote $vopt add "$backup_name" "$backup_url"
        __call git push $vopt "$backup_name" --all
        __call git push $vopt "$backup_name" --tags
    fi

    __printsep
    echo -e "\e[97;1mCOMMITS\e[m"
    __printrepo \
        "$upstream_commits"                                   36 source  "$upstream_repo" \
        "$(git log --oneline "$branch" | wc -l)"              39 local   "$(pwd)" \
        "$(git log --oneline "$origin_name/$branch" | wc -l)" 35 destin1 "$origin_url" \
        "$(git log --oneline "$backup_name/$branch" | wc -l)" 35 destin2 "$backup_url"

    __call popd
    __call rm -rf $vopt "$target_repo_name"
    __callso popd

    echo -e "\e[32;1mDone\e[m"
}
__illegal_opt() { echo -e "ERROR: Illegal option -${OPTARG:--$OPT}" ; }
__arg_parse() {
    while getopts :vh-: OPT; do
        if [ "$OPT" = "-" ]; then
            OPT="${OPTARG%%=*}"
            OPTARG="${OPTARG#$OPT}"
            OPTARG="${OPTARG#=}"
        fi
        # shellcheck disable=SC2214
        case "$OPT" in
             v|vopt) (( opt_verbose++ )) ;;
             h|help) __usage && exit 0 ;;
              ??*|?) __illegal_opt && __usage && exit 1 ;;
        esac
    done
    shift $((OPTIND - 1))

    arg_upstream_repo="${1:?Repo in format OWNER/NAME required}"
    arg_target_repo="${2:-}"
}

# -@temp---------------------------
ES7S_REPO_DIST_GH_TPL=dl-dist/%s
ES7S_REPO_DIST_GLAB_TPL=dp3.dl/import/dist/%s
#ES7S_REPO_REMOTE_ORIGIN_NAME=dp3
ES7S_REPO_REMOTE_ORIGIN_NAME=origin
ES7S_REPO_REMOTE_BACKUP_NAME=dp3
# -@temp---------------------------

declare -i opt_verbose=0
declare arg_upstream_repo
declare arg_target_repo

__arg_parse "$@"
__main
