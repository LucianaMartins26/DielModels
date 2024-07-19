mkdir -p tests/data
mkdir -p tests/models

unzip -o simulatable_models.zip -d tests/models
unzip -o tests_data.zip -d tests/data
unzip -o integration_tests.zip -d tests/integration_tests
unzip -o quercus_changed_models.zip 'diel_multi_quercus_model_fixed.xml' -d validation/quercus/simulation_sp
unzip -o quercus_changed_models.zip '(changed)diel_multi_quercus_model.xml' -d validation/quercus
unzip -o simulation_sp_outputs.zip 'produced_at_day.xlsx' -d validation/arabidopsis/simulation_sp
unzip -o simulation_sp_outputs.zip 'produced_at_night.xlsx' -d validation/arabidopsis/simulation_sp
unzip -o simulation_sp_outputs.zip 'produced_at_day_multi_quercus.xlsx' -d validation/quercus/simulation_sp
unzip -o simulation_sp_outputs.zip 'produced_at_night_multi_quercus.xlsx' -d validation/quercus/simulation_sp

rm simulatable_models.zip
rm tests_data.zip
rm integration_tests.zip
rm quercus_changed_models.zip
rm simulation_sp_outputs.zip

echo "Files unzipped and moved to their respective directories."
