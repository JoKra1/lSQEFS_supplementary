source .env
conda activate ${conda_env}
python setup.py
jupyter nbconvert sim_1.ipynb --execute --to html &
jupyter nbconvert sim_2.ipynb --execute --to html &
jupyter nbconvert sim_3.ipynb --execute --to html &
jupyter nbconvert sim_4.ipynb --execute --to html &
jupyter nbconvert sim_5.ipynb --execute --to html &

wait

Rscript -e "rmarkdown::render('sim_1.Rmd')" &
Rscript -e "rmarkdown::render('sim_2.Rmd')" &
Rscript -e "rmarkdown::render('sim_3.Rmd')" &
Rscript -e "rmarkdown::render('sim_4.Rmd')" &
Rscript -e "rmarkdown::render('sim_5.Rmd')" &

wait
