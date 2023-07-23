# Astute Startups Insighter (ASI) - A Data Analysis Project

## Problem Statement
The objective of this project is to gather information of Top 1207 Startups and corresponding 500 software engineers from [this website](https://topstartups.io/). <br/> 
Later we utilized the scraped data providing insights to both investors and job seekers, employees, stakeholders simultaneously( encompassing all workforce & resource level) by applying data science to understand following key points using Tableau Dashboard and data analysis   : 

1. Startup frequency heatmap in a map and bar chart of country frequency (excluding USA for unbiased heatmap)
2. A bubble plot that can display current use of AI in top startup fields
3. Which company is in potential risk to lay off employees? (employee generated USD valuation as metric)
4. Which company is very productive for investment, job seekers. (employee generated valuation as metric)
5. Does a startup have room for growth (employee generated valuation as metric)
6. Which company is risk prone to future bankruptcy (Years generated valuation as metric)
5. salary scale of employees in different positions e.g. software engineers and how they connect with each other from salary dimension

You can visit the public dashboard [here](https://public.tableau.com/app/profile/tanvir.ishraq.khan/viz/AstuteStartupsInsighter-Aprojectforinvestorssoftwareengineerssimultaneously/Stability2Sheet?publish=yes). Be mindful that the dashboard contains multiple tabs. Each Tab used to find different new insights. It is suggested to use the fullscreen (available at bottom right) for a better overarching view. 

## Findings and Observations from the [Dashboard](https://public.tableau.com/app/profile/tanvir.ishraq.khan/viz/AstuteStartupsInsighter-Aprojectforinvestorssoftwareengineerssimultaneously/Stability2Sheet?publish=yes)
1. Besides other countries, Interestingly india is a melting point of new startups. There should be new opportunities for investors. But the high number calls for research of stability and security first before investing.
Job seekers can also be aware of the fact that this place will be hiring.
2. One of top trend of AI use is in healthcare. AI has found its way into the healthcare system even though there is an ethical consideration regarding adopting AI into healthcare without professional Doctor supervision and it is shunned.
Also, Hardwares are progressively adopting AI. Hardwares is one of the top fields.
3. Distinguished startups that could be in potential risk to lay off employees. (High amount of Employees. low startup Valuation). This is useful information for both investors and job seekers, employees, stakeholders to understand stability and security of a startup.
4. Distinguished startups that are despite being very productive still should have more room for growth (Low amount of Employees. Great startup Valuation). Providing useful information for both investors and job seekers, employees to understand stability and security of a startup.
5. Analyzed startups to estimate potential future bankruptcy possibility to look out for. (Long years of business yet yielding low amount valuation compared to peers). Important for startup directors, employees in risk of lay off and investors.
6. Software Engineers position salary Scale and Relation valued and serialized. Important understanding for job holders. This nature of analysis can be applied with any other position e.g. finance, marketing team, project managers etc. as well.


## Build From Sources and using the Selenium Scraper
1. Clone the repo
```bash
git clone https://github.com/msi1427/Demographics-of-Best-CS-Scientists-Worldwide.git
```
2. Install dependencies. It is highly suggested to use a virtual environment.
```bash
pip install -r requirements.txt
```
3. Download Chrome WebDrive from https://chromedriver.chromium.org/downloads 
4. Run the scraper notebook named:
```bash
scraper_&_data_processing_startups.ipynb
```
5. You will get 3 files named `Top_startups_details_dataset_complete.csv`, `SE_in_startups_dataset.csv`, `AI_field_trend_dataset.csv` containing all the required fields. 
Alternatively, check all the scraped data here: https://github.com/tanvir-ishraq/Astute-Startups-Insighter-ASI-a-Data-Analysis-Project-for-investors-and-software-engineers/tree/main/ASI%20Scraper
