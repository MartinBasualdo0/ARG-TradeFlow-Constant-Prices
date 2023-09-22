# Argentinian Trade Flow since 1986 in constant prices

## Project Objective

The central objective of this project is to visualize and analyze the historical trade flows of Argentina across different presidential administrations and in the context of significant (inter)national events. By examining these trade patterns, I aim to gain insights into how political leadership and major events have influenced Argentina's trade dynamics.

## Data Sources

This project relies on two primary data sources to provide a comprehensive view of Argentina's trade history:

1. **FRED (Federal Reserve Economic Data):** We utilize the FRED API to access and incorporate economic data relevant to the analysis. FRED provides a valuable source of economic indicators and statistics that help us understand the broader economic context.
2. **INDEC (Instituto Nacional de Estadística y Censos):** INDEC has recently made available new datasets that are instrumental for this study. These datasets enable us to delve deeper into Argentina's trade history and provide a more nuanced analysis of trade flows during specific periods.

### Getting Your API Key

1. Create a file named `api_key.py` in the project's main directory.
2. Within `api_key.py`, declare a variable named `fredApiKey` and assign it a string containing your FRED API key.

<pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>python</span><button class="flex ml-auto gap-2"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="icon-sm" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>Copy code</button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-python">ApiKey = "your_api_key_here"</code></div></div></pre>

   Replace `"your_api_key_here"` with your actual FRED API key.

## Running the Analysis

To initiate the analysis and generate visualizations of Argentina's trade history throughout different presidencies and significant events, you can run either the `main.sh` or `main.py` script provided in the project directory. These scripts utilize data from both FRED and INDEC to create a comprehensive overview of Argentina's trade flows.

Ensure that you have all the necessary dependencies and libraries installed to run the scripts successfully. Periodically update your data sources to maintain the relevance and accuracy of your analysis.

Through this project, I aim to uncover valuable insights into the complex relationship between political leadership, significant events, and Argentina's trade dynamics, contributing to a deeper understanding of the country's economic history.
