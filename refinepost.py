import re

def remove_tags(text):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', text)

def unescape_html(text):
    text = re.sub('&lt;','<<',text)
    text = re.sub('&gt;','>>',text)
    text = re.sub('&amp;','',text)
    text = re.sub('&#039;','\'',text)
    text = re.sub('>>(\d{8})','',text)
    text = re.sub('>>','',text)
    return text
    
def refinepost(rawpost):
    refinedpost = remove_tags(rawpost)
    refinedpost = unescape_html(refinedpost)
    return refinedpost
