for f in ls *saveShapes*__3__0*; do 
    echo $f
    root -b -q -l 'listOutliers.C("'$f'")'; 
done;
