echo 'If running this script results in an error similar to "You are not currently on a branch. - Please specify which branch you want to merge with." you may need to run all_submodules_checkout_develop.cmd.  This script should be mapped to a custom action in SourceTree.'
git submodule foreach git pull --recurse-submodules