
cp /home/ameert/git_projects/astro_image_processing/make_final_catalog/output_tables/fits/UPenn_PhotDec_CAST.fits /home/ameert/git_projects/astro_image_processing/make_final_catalog/output_tables/fits/meert_et_al_data_tables_v1/
cp /home/ameert/git_projects/astro_image_processing/make_final_catalog/output_tables/fits/UPenn_PhotDec_Models_rband.fits /home/ameert/git_projects/astro_image_processing/make_final_catalog/output_tables/fits/meert_et_al_data_tables_v1/
cp /home/ameert/git_projects/astro_image_processing/make_final_catalog/output_tables/fits/UPenn_PhotDec_nonParam_rband.fits /home/ameert/git_projects/astro_image_processing/make_final_catalog/output_tables/fits/meert_et_al_data_tables_v1/
cp /home/ameert/git_projects/catalog2013/data_tables.pdf /home/ameert/git_projects/astro_image_processing/make_final_catalog/output_tables/fits/meert_et_al_data_tables_v1/README.pdf

cd /home/ameert/git_projects/astro_image_processing/make_final_catalog/output_tables/fits/

tar -czvf meert_et_al_data_tables_v1.tgz meert_et_al_data_tables_v1 

cd -