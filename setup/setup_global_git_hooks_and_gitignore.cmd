REM to test if this worked:  git config --global core.hooksPath

REM get pwd
pwd>temp.txt
set /P pwd=<temp.txt
rm temp.txt

REM create new path to be used as global hook path
set pwd=%pwd:/c/=C:/%
set ghp=%pwd:/setup=/global_git_hooks%
git config --global core.hooksPath "%ghp%"

REM tell the user what the global hook path has been set to
git config --global core.hooksPath > temp.txt
set /P global_hooks_path=<temp.txt
rm temp.txt

echo "The path for the directory that will contain all global Git hooks has been set to: " %global_hooks_path%

REM create new path to be used as global gitignore path
set pwd=%pwd:/c/=C:/%
set gip=%pwd:/setup=/global_gitignore/.gitignore%
git config --global core.excludesfile "%gip%"

REM tell the user what the global gitignore path has been set to
git config --global core.excludesfile > temp.txt
set /P global_gitignore_path=<temp.txt
rm temp.txt

echo "The path for the global .gitignore file has been set to: " %global_gitignore_path%

REM change default text editor to nano without asking the user because I belive there is a greater chance of
REM someone who doesn't know what they're doing exiting the window by accident than the type of person who 
REM would be bothered by nano not knowing how to change it back
git config --global core.editor "nano"


pause