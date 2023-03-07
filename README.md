# COVID-19 Online: How people interacted with government websites during the pandemic

Using data from Analytics.Gov capturing website traffic for US government domains, we examine how trends in government website traffic changed over the course of the COVID-19 pandemic. In combination with data on COVID-19 cases, deaths, and vaccinations to track the pandemic’s course, we explore what government websites people accessed during the pandemic and how the traffic on these sites changed as the pandemic progressed. Additionally, we use auxillary Analytics.gov data on traffic source and browser language to offer insights into the demographics of people using government websites and to showcase how people accessed government-published information (e.g through search engines, social media, news, etc.) in times of crisis. 

<img width="1512" alt="Screen Shot 2023-03-07 at 10 46 26 AM" src="https://user-images.githubusercontent.com/111666975/223491476-f765f0d8-d81c-44aa-b807-ccb3737586ff.png">
<img width="1504" alt="Screen Shot 2023-03-07 at 10 46 43 AM" src="https://user-images.githubusercontent.com/111666975/223491546-41fae7b1-50c0-4cde-9df7-49370db9e8c6.png">

## Running our Project

After cloning the repository following these steps to view our work.

1. Set up the virtual enviornment by running ``` poetry install ``` to install the required packages, then ```poetry shell``` to activate the environment
2. Next, to view the dashboard run ```python -m happy_app``` 
3. Follow the generated URL (e.g http://127.0.0.1:8051) by copying and pasting it into your prefered web browser

## (Optional) Re-collecting Our Data

To replicate our data collection process follow these steps:

1. Obtain a API key from Analytics.Gov by filling out [this form](https://open.gsa.gov/api/dap/) under **Getting Started**.
2. In the repository, store the key in your environment by executing the following line in your shell:
```bash
 export ANALYTICS_API_KEY=<YOUR KEY HERE> 
 ```
3. Run ```python -m happy_app.clean``` to pull and clean our data from the APIs. This will take around 20-25 minutes to run to completion. 
