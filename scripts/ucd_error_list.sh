#/bin/bash
cat $1 | grep ERROR > $1.errors
sed -i .ts 's/^.\{24\}//' $1.errors
sort -u $1.errors > $1.errorlist
rm $1.errors $1.errors.ts
