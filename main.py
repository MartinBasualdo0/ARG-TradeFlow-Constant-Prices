import src.modules.check as check
check.check_and_create_directories()
check.check_api_key_file()

import src.modules.plots as plot
plot.genera_plots_inflacionados()