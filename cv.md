---
title: CV
hide_title: true
---

{% comment %} The CV is generated from cv/cv.xlsx by cv/build_cv.py. Edit the spreadsheet, not this page. {% endcomment %}

See my CV in pdf [here](acadcv.pdf).

{% for section in site.data.cv %}
<h2>{{ section.title }}</h2>
{% if section.text %}<p>{{ section.text }}</p>{% else %}
<ul>
{% for item in section.items %}	<li>{{ item }}</li>
{% endfor %}</ul>
{% endif %}
{% endfor %}
