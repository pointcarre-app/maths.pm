n_users=20
requests_per_user=5
log=DEBUG

mode=prod

scenery load --test="sujets0_load"   --mode=$mode -u=$n_users -r=$requests_per_user --log=$log 
