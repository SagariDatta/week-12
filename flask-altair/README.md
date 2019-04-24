# Example Apps for Flask + Altair

This directory contains three example Flask apps:

1. `app1.py`: plots the number of shootings per neighborhood in the last 365 days using
   `template1.html` as the HTML template
1. `app2.py`: similar to `app1.py` but allows the user to specify the number of days to query
   using a range slider; relies on `template2.html` as the HTML template
1. `app3.py`: an example of a mult-chart dashboard with Altair

From the Jupyter terminal, these Flask servers can be executed using:

```bash
python app1.py
```

And then navigate to http://0.0.0.0:5000 in your browser to see the app.
