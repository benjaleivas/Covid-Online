# Are Americans Looking to .gov Websites for Health Information?

Overview of project...[add more here] 

## Notes on reproducing our program

To re-produce our data collection, you will need to get an API key for the analytics.us.gov API. Here are the steps to make sure you're set up correctly in order to re-produce our work:

* get personalized key by filling out [the form](https://open.gsa.gov/api/dap/) under **Getting Started**.

* after retrieving a personalized API key from your email, run the following in an ipython3 session:

```python
import os
os.environ['ANALYTICS_API_KEY'] = '<YOUR KEY HERE>'
```

