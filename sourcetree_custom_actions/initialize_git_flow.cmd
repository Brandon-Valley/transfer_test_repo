echo "Making a possibly empty commit to allow Git Flow to be initialized even if this is a new repository..."
git commit --allow-empty -m "Initialized Git Flow"

echo "Initializing Git Flow with default branch names..."
git flow init -d

echo "Pushing and adding remote for new develop branch..."
git push --set-upstream origin develop

echo "Pushing all branches..."
git push --all
