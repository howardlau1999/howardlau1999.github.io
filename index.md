---
layout: default
title: Haohua Liu's Homepage
---

English Resume: [PDF](https://howardlau.me/wp-content/uploads/2021/10/resume_master.pdf)

Visit my Chinese blog: [https://howardlau.me](https://howardlau.me)

Server Programming Guide: [https://liuhaohua.com/server-programming-guide](https://liuhaohua.com/server-programming-guide)

<ul>
  {% for post in site.posts %}
    <li>
      <a href="{{ post.url }}">{{ post.title }}</a>
      {{ post.excerpt }}
    </li>
  {% endfor %}
</ul>