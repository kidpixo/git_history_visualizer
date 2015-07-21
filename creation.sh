# initialize repository
git init

# do stuff with the files

# extrat all the commits 
git --no-pager log --reverse --oneline

# extract all the filenames
git --no-pager log --reverse --name-only --oneline --pretty='format:' |  sed '/^$/d' | sort | uniq

# extract the whole git history
git --no-pager log --reverse --name-status --oneline --pretty='format:COMMIT %h %s' |  tr '\t' ' ' | sed -E -e 's/( )+/ /g' -e '/^$/d'
