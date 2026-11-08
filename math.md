---
title: Math stuff
---

{% comment %}
Lists the posts with `category: math`, newest first. A series is shown once, where it first appears,
with its title linking to part 1 (whose box lists all the parts and files).
With no math post the page is not built at all (_plugins/hide_empty_math_page.rb).
{% endcomment %}
{% assign math_posts = site.posts | where_exp: "post", "post.categories contains 'math'" %}
{% assign listed_series = "" %}
<div class="post-list">
{% for post in math_posts %}
	{% if post.series %}
		{% assign marker = "|" | append: post.series | append: "|" %}
		{% unless listed_series contains marker %}
			{% assign listed_series = listed_series | append: marker %}
			{% assign parts = math_posts | where: "series", post.series | sort: "series_part" %}
			{% assign info = site.data.series[post.series] %}
	<article>
		<h3><a href="{{ parts.first.url | relative_url }}">{{ info.title | default: parts.first.title }}</a></h3>
		<p>{% if info.summary %}{{ info.summary }} · {% endif %}A series in {{ parts.size }} parts.</p>
	</article>
		{% endunless %}
	{% else %}
	<article>
		<h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
		{% if post.summary %}<p>{{ post.summary }}</p>{% endif %}
	</article>
	{% endif %}
{% endfor %}
</div>
