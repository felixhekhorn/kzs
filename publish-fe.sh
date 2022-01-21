#!/usr/bin/env sh

# get current hash
c=$(git rev-parse --short HEAD)

# abort on errors
set -e

# build
npm run build

# navigate into the build output directory
cd dist

touch .nojekyll

git init
git add -A
git commit -m "Deploy from $c"

# if you are deploying to https://<USERNAME>.github.io/<REPO>
git push -f git@github.com:felixhekhorn/kzs.git master:gh-pages

cd -
