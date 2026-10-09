---
title: Math thoughts
---

{% comment %}
Lists the posts with `category: math`, newest first. The posts of a series are shown together,
in part order, where the series first appears.
{% endcomment %}
{% assign math_posts = site.posts | where_exp: "post", "post.categories contains 'math'" %}
{% assign listed_series = "" %}
{% if math_posts.size == 0 %}<p>No posts yet.</p>{% endif %}
<div class="post-list">
{% for post in math_posts %}
	{% if post.series %}
		{% assign marker = "|" | append: post.series | append: "|" %}
		{% unless listed_series contains marker %}
			{% assign listed_series = listed_series | append: marker %}
			{% assign parts = math_posts | where: "series", post.series | sort: "series_part" %}
			{% assign info = site.data.series[post.series] %}
	<article>
		<h3>{{ info.title | default: parts.first.title }}</h3>
		<p>A series in {{ parts.size }} parts.{% if info.files %} {% for file in info.files %}<a href="{{ file.url | relative_url }}">{{ file.name }}</a>{% unless forloop.last %} · {% endunless %}{% endfor %}{% endif %}</p>
		<ol>
			{% for part in parts %}<li><a href="{{ part.url | relative_url }}">{{ part.title }}</a></li>
			{% endfor %}
		</ol>
	</article>
		{% endunless %}
	{% else %}
	<article>
		<h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
		<p>{{ post.date | date: "%-d %B %Y" }}{% if post.summary %} · {{ post.summary }}{% endif %}</p>
	</article>
	{% endif %}
{% endfor %}
</div>
