"""Build the maintainable archive and single-file GitHub upload from current sources."""
from pathlib import Path
import zipfile
root=Path(__file__).resolve().parents[1]
outputs=root.parent
html=(root/'index.html').read_text()
html=html.replace('<link rel="stylesheet" href="styles.css">','<style>'+ (root/'styles.css').read_text()+'</style>')
scripts=['data/bootstrap.js','js/policy.js','js/simulator.js','js/dashboard.js','js/policy-editor.js','js/gemini.js','js/connection.js']
for name in scripts:
    text=(root/name).read_text().replace('</script','<\\/script')
    html=html.replace('<script src="'+name+'"></script>','<script>\n'+text+'\n</script>')
single=outputs/'roam-live-hq-single'
single.mkdir(exist_ok=True)
(single/'index.html').write_text(html)
with zipfile.ZipFile(outputs/'roam-live-hq-index.zip','w',zipfile.ZIP_DEFLATED) as z:
    z.write(single/'index.html','index.html')
with zipfile.ZipFile(outputs/'roam-live-hq-project.zip','w',zipfile.ZIP_DEFLATED) as z:
    for file in sorted(root.rglob('*')):
        if file.is_file() and '__pycache__' not in str(file):
            z.write(file,file.relative_to(root))
print('Built single-file index and both GitHub upload archives.')
