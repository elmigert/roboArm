#
# upload source code to folder
#
# exit on error
set -e

# set some attributes
dir=/home/mp/mp
name=mp
address=$1

# copy sh key to avoid typing password
ssh-copy-id mp@$address

## delete folder
#ssh mp@$address rm -rf $dir
## create folder
#ssh mp@$address mkdir -p $dir
## sync files
echo ""
echo "--- uploading ---"
cd ..
DIRS_TO_SYNC="uarm_python_sdk src"
rsync -av -R $DIRS_TO_SYNC mp@$address:$dir \
  --delete
echo "done"
echo ""
