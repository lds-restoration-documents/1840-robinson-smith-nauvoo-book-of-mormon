"""Helper for scripts that read book-of-mormon-1840.md: remove its YAML frontmatter."""


def strip_frontmatter(t):
    """Remove the YAML frontmatter block that compile_markdown.py puts at the top of book-of-mormon-1840.md."""
    if t.startswith('---\n'):
        end = t.find('\n---\n', 4)
        if end != -1:
            return t[end + 5:].lstrip('\n')
    return t


REPO = 'https://github.com/lds-restoration-documents/1840-robinson-smith-nauvoo-book-of-mormon'


def txt_header(sparse=False):
    """The single '#' line that starts the .txt outputs (title, status, repository), plus a blank line."""
    kind = 'sparse, AI draft, no full human proofread' if sparse else 'AI draft, no full human proofread'
    return f'# The Book of Mormon (Nauvoo, 1840) ({kind}) - {REPO}\n\n'
