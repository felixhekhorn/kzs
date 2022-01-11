#!/usr/bin/env sh

# abort on errors
set -e

# build
npm run build

# navigate into the build output directory
cd dist

touch .nojekyll

git init
git add -A
git commit -m 'Deploy'

# if you are deploying to https://<USERNAME>.github.io/<REPO>
git push -f git@github.com:felixhekhorn/kzs.git master:gh-pages

cd -
