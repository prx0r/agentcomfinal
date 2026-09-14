from importlib.resources import files


def test_style_avoids_ai_saas_cliches():
    css = files('xmrbot.web').joinpath('static/styles.css').read_text()
    assert 'linear-gradient' not in css
    assert 'radial-gradient' not in css
    assert 'backdrop-filter' not in css
    assert '--orange:#ff6600' in css
    assert 'border-radius:999' not in css


def test_required_publication_pages_ship():
    root = files('xmrbot.web').joinpath('static')
    for name in ['blog.html','blog-post.html','recipes.html','mark.svg']:
        assert root.joinpath(name).is_file()
