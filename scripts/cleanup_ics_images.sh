#/bin/bash
cf ic images -a | grep $1 > $1-images
sed 's/^.\{70\}//' $1-images > $1-temp
sed 's/\ .*//' $1-temp > $1-images
rm $1-temp

# http://stackoverflow.com/questions/1521462/looping-through-the-content-of-a-file-in-bash
while read p; do
  cf ic rmi $p
done <$1-images

rm $1-images
