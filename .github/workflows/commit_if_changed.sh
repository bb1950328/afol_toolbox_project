COUNT = $(git diff --cached --numstat | wc -l)
if ["$COUNT" != "0"]
then
  git commit -am "Rescaled images (Github Action)"
  git push
else
  echo "Nothing changed"
fi
