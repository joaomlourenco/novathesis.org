# Blog posts

One file per post per language:

    YYYY-MM-DD-slug.en.md
    YYYY-MM-DD-slug.pt.md

The date orders the history; the slug becomes the URL
(`/en/blog/slug`). Both languages are expected — a post with only one is
still published, and the history labels it.

## Writing a post

1. Copy `_TEMPLATE.md` to `YYYY-MM-DD-slug.en.md` and `…pt.md`.
2. Fill in the front matter and write the body.
3. Optional image: put the file in `blog/images/` and name it in `image:`.
   `image_alt:` is then required — it is what screen readers announce, and
   the image is also the social card shown when the post is shared.
4. Run the generator:

       python3 tools/gen_blog.py

It rewrites `en/blog/` and `pt/blog/`, the two Atom feeds, and the Blog link
in every page's navigation. It is idempotent: running it twice changes
nothing, and it tells you about anything it could not use.
