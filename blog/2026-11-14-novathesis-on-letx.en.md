---
title: The template now opens in letx
date: 2026-11-14
summary: letx hosts novathesis and compiles it — the first route into the template that is free and one click at the same time.
image:
image_alt:
---

[letx](https://letx.app/templates/universities/novathesis/) now carries
**nova**thesis, and compiles it.

That is a short sentence, so here is what makes it worth a post. Until now the
browser routes into the template came in two kinds, and each one asked
something of you:

* **Overleaf** and **Inscrive** import a school's repository in a single
  click — and then will not compile it without a paid plan. The template does
  not fit in the 20 seconds Overleaf's free plan allows.
* **ScienHub** is free, but cannot import from a link, so you download your
  school's ZIP and upload it into an empty project by hand.

letx is the first that is **both**. It is free, it opens the template in one
click, it compiles, and the only thing it asks for is an account.

## One thing to set yourself

The project letx keeps is the general template, not your school's repository.
So the one step the other one-click routes do for you is yours here: open
`0-Config/1_novathesis.tex` and name your school.

```latex
\ntsetup{school=nova/fct}
```

You do not have to go looking for the id. On
[Find your school](https://novathesis.org/en/schools), every row now has a
**letx** button, and the box it opens spells out exactly what to write for
that school — including the awkward ones, where the id is not simply the
repository name with the dashes turned into slashes, and the four schools that
need a second line naming the degree.

## Do not take the ZIP there

The usual advice for a service that cannot import from a link — download the
ZIP, upload it, set the main document — is precisely the thing that does not
work on letx. The template needed adapting to build on their system, and what
they adapted is the project behind that one link. A ZIP you upload yourself
will not compile.

So that link is the way in, and the copy behind it is theirs: they update it
with each release, so now and then it is a version behind — but not for long. If you need something that landed in the
template last week, build locally or take your school's repository to one of
the other services.

## Thanks

The porting work was done at letx by **Shihab Shahriar**, who made the
template build on their system and keeps it there free of charge. The other
two names in our
[acknowledgements](https://novathesis.org/en/support) are there for accounts
they lent us; this one is there for work.
