"""Build the offline fallback from the canonical JSON configuration."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
paths={'config':'config/simulation.json','rules':'config/rules.json','principles':'config/principles.json','schools':'data/schools.json','robots':'data/robots.json','zones':'data/zones.json'}
data={k:json.loads((root/p).read_text()) for k,p in paths.items()}
(root/'data/bootstrap.js').write_text('/* Generated offline fallback; edit JSON files, then rebuild. */\nwindow.ROAM_INPUTS='+json.dumps(data,separators=(',',':')).replace('</','<\\/')+';\n')
print('Offline configuration rebuilt from JSON.')
