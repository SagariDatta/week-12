# Week 12<br>Web Servers, Interactive Web Apps, and Dashboards

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/MUSA-620-Spring-2019/week-12/master?filepath=lecture-12.ipynb)

## Updating your local environment

There are two new packages we'll need this week so we'll need
to update your Python environment.

### Option 1

From the Anaconda Prompt or Terminal, run

```
conda activate musa-620
conda install flask
conda install -c plotly dash
```

### Option 2

The `environment.yml` in this repository
contains all of the necessary packages. To update your local environment:

**Step 1.** Download the `environment.yml` file in this repository to your computer.

**Important:** Make sure you download the **raw** version of the file from GitHub and that the file extension on your computer is `.yml`.

**Step 2.** From either the Anaconda Prompt (Windows) or Terminal app (MacOS):

```
conda env update --file environment.yml --name musa-620
```

where `musa-620` should be the same name of the environment you have been using.

## Reference

- [Guide to Pull Requests](https://help.github.com/en/articles/creating-a-pull-request)
- [Introduction to Web Servers](https://developer.mozilla.org/en-US/docs/Learn/Common_questions/What_is_a_web_server)
- flask
  - [Documentation](http://flask.pocoo.org/docs/1.0/)
- HTML and CSS
  - [Introduction to HTML and Tutorials](https://developer.mozilla.org/en-US/docs/Learn/HTML/Introduction_to_HTML)
  - [Introduction to CSS and Tutorials](https://developer.mozilla.org/en-US/docs/Learn/CSS/Introduction_to_CSS)
- Dash
  - [User Guide](https://dash.plot.ly/)
  - [App Gallery](https://dash.plot.ly/gallery)
  - [Plotly Documentation](https://plot.ly/python/)
