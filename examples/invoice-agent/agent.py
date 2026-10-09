"""An accounts-payable agent on Canonn R1: each invoice is checked against its
contract, eight at a time. It pays the ones that match and holds the ones that
do not, quoting the two sentences that disagree. Prints a summary and saves
every reply. Standard library only.

    python make_pairs.py                 # 50 fictional contract/invoice pairs, 5 planted mismatches
    CANONN_API_KEY=... python agent.py   # get a key at https://canonn.ai/dashboard/
"""
import json, os, re, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
CK = os.environ['CANONN_API_KEY']
PRICE_IN, PRICE_OUT = 0.25, 1.00  # USD per 1M tokens (canonn.ai pricing)
SYSTEM = ('You are the accounts-payable agent for Northwind Logistics. You approve an invoice only if it matches the contract. '
          'Answer from the two documents below.\n\nCONTRACT\n{contract}\n\nINVOICE\n{invoice}')
ASK = ('Does this invoice match the contract? Reply with PAY or HOLD on the first line. '
       'If HOLD, then quote the contract sentence and the invoice sentence that disagree.')
pairs = json.load(open('pairs.json'))
def check(p):
    body = {'model': 'canonn-r1', 'temperature': 0, 'max_tokens': 200,
            'messages': [{'role': 'system', 'content': SYSTEM.format(**p)}, {'role': 'user', 'content': ASK}]}
    req = urllib.request.Request('https://api.canonn.ai/v1/chat/completions', json.dumps(body).encode(),
                                 {'Authorization': f'Bearer {CK}', 'Content-Type': 'application/json', 'User-Agent': 'canonn-example-invoice-agent/1'})
    t = time.time()
    try:
        j = json.load(urllib.request.urlopen(req, timeout=180))
    except Exception as e:
        return {**p, 'error': str(e)}
    a = j['choices'][0]['message']['content'].strip()
    u = j.get('usage', {})
    decision = 'HOLD' if re.match(r'\W*hold', a, re.I) else 'PAY' if re.match(r'\W*pay', a, re.I) else '?'
    return {**p, 'answer': a, 'decision': decision, 'ms': round((time.time() - t) * 1000), 'usage': u,
            'conflict': (j.get('canonn') or {}).get('conflict'), 'cost_usd': (u.get('prompt_tokens', 0) * PRICE_IN + u.get('completion_tokens', 0) * PRICE_OUT) / 1e6}
t0 = time.time()
with ThreadPoolExecutor(8) as ex:
    res = list(ex.map(check, pairs))
wall = time.time() - t0
ok = [r for r in res if 'decision' in r]
caught = [r for r in ok if r['truth'] == 'hold' and r['decision'] == 'HOLD']
false_hold = [r for r in ok if r['truth'] == 'pay' and r['decision'] != 'PAY']
missed = [r for r in ok if r['truth'] == 'hold' and r['decision'] != 'HOLD']
summary = {'invoices': len(pairs), 'answered': len(ok), 'errors': len(res) - len(ok), 'planted': 5, 'caught': len(caught),
           'missed': [r['vendor'] for r in missed], 'false_holds': [(r['vendor'], r['answer'][:160]) for r in false_hold],
           'wall_s': round(wall, 1), 'cost_usd': round(sum(r.get('cost_usd', 0) for r in ok), 5),
           'median_ms': sorted(r['ms'] for r in ok)[len(ok) // 2] if ok else None, 'at': time.strftime('%Y-%m-%dT%H:%M:%S')}
json.dump({'summary': summary, 'results': res}, open('run-%s.json' % time.strftime('%Y%m%d-%H%M'), 'w'), indent=1, ensure_ascii=False)
print(json.dumps(summary, indent=1, ensure_ascii=False))
for r in caught: print('\nCAUGHT', r['vendor'], r['kind'], '|', r['answer'][:300].replace('\n', ' / '))
