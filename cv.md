---
title: CV
hide_title: true
---

{% comment %} The CV is generated from cv/cv.xlsx by cv/build_cv.py. Edit the spreadsheet, not this page. {% endcomment %}

<ul class="actions"><li><a href="{{ '/acadcv.pdf' | relative_url }}" class="button">Short CV (PDF)</a></li></ul>

{% for section in site.data.cv %}
{% capture body %}{% if section.text %}<p>{{ section.text }}</p>{% else %}<ul>
{% for item in section.items %}	<li>{{ item }}</li>
{% endfor %}</ul>{% endif %}{% endcapture %}
{% if section.collapsed %}
<details class="cv-section">
<summary><h2>{{ section.title }}</h2></summary>
{{ body }}
</details>
{% else %}
<h2>{{ section.title }}</h2>
{{ body }}
{% endif %}
{% endfor %}
