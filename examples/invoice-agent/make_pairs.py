"""Fictional contract/invoice pairs for the payables agent. Northwind Logistics
(fictional) buys from 50 fictional vendors; 45 invoices match their contract,
5 contradict it in a way a payables clerk must catch. Deterministic (seeded)."""
import json, random
random.seed(20261003)
VENDORS = ['Halden Freight', 'Aster Cloud Hosting', 'Brightline Cleaning', 'Corvid Security', 'Delta Print Works', 'Elm Street Catering', 'Fjord Telecom', 'Granite Office Supply',
  'Harbor Fuel', 'Ion Software', 'Juniper Legal', 'Kestrel Couriers', 'Lumen Lighting', 'Meridian Insurance', 'Northgate Forklifts', 'Orbit Analytics', 'Pine Ridge Pallets',
  'Quarry Packaging', 'Redwood HR Services', 'Saltmarsh Waste', 'Tidewater Storage', 'Umber Uniforms', 'Vale Water', 'Wren Translation', 'Yarrow Recruitment', 'Zephyr HVAC',
  'Alder Accounting', 'Birch Data Backup', 'Cinder Pest Control', 'Dune Tyres', 'Ember Electrical', 'Flint Locksmiths', 'Garnet Signage', 'Heron Medical Kits', 'Iris Design Studio',
  'Jade Vending', 'Kiln Facilities', 'Larch Fleet Leasing', 'Moss Landscaping', 'Nimbus Email', 'Oak Ledger Payroll', 'Pebble Coffee', 'Quill Copywriting', 'Raven Shredding',
  'Sable Parking', 'Thistle Training', 'Umbra CCTV', 'Vireo Translation', 'Willow Plants', 'Yew Archive']
SERVICES = ['monthly freight handling', 'cloud hosting', 'office cleaning', 'site security', 'printing', 'staff catering', 'telecom services', 'office supplies', 'diesel supply', 'software licences',
  'legal retainer', 'courier services', 'lighting maintenance', 'cargo insurance', 'forklift rental', 'analytics platform', 'pallet supply', 'packaging materials', 'HR outsourcing', 'waste collection']
def contract(v, svc, fee, terms, cap, vat):
    return (f"MASTER SERVICES AGREEMENT between Northwind Logistics Ltd and {v}.\n"
            f"1. Services. {v} provides {svc} to Northwind's Rotterdam depot.\n"
            f"2. Fees. The fee is EUR {fee:,} per month, excluding VAT. VAT is charged at {vat}%.\n"
            f"3. Price changes. Fees may rise once a year by no more than {cap}% and only with 60 days' written notice.\n"
            f"4. Payment. Invoices are payable within {terms} days of receipt.\n"
            f"5. Term. Twelve months from 1 January 2026, renewing yearly unless cancelled.")
def invoice(v, n, svc, fee, terms, vat, month='September 2026'):
    total = round(fee * (1 + vat / 100))
    return (f"INVOICE {n} from {v} to Northwind Logistics Ltd.\n"
            f"Period: {month}. Description: {svc}.\n"
            f"Amount: EUR {fee:,} excluding VAT. VAT {vat}%: EUR {total - fee:,}. Total due: EUR {total:,}.\n"
            f"Payment terms: due within {terms} days.")
pairs = []
BAD = {7: 'price', 18: 'increase', 26: 'terms', 33: 'vat', 44: 'price2'}
for i, v in enumerate(VENDORS):
    svc = SERVICES[i % len(SERVICES)]
    fee = random.choice([1200, 1850, 2400, 3100, 4250, 5600, 6800, 7350, 8900, 9800, 11200, 12750])
    terms = random.choice([30, 45, 60]); cap = random.choice([3, 4, 5]); vat = 21
    c = contract(v, svc, fee, terms, cap, vat)
    kind = BAD.get(i)
    ifee, iterms, ivat, truth = fee, terms, vat, 'pay'
    if kind == 'price': ifee = round(fee * 1.265 / 10) * 10; truth = 'hold'
    if kind == 'price2': ifee = fee + 1450; truth = 'hold'
    if kind == 'increase': ifee = round(fee * (1 + (cap + 7) / 100) / 10) * 10; truth = 'hold'
    if kind == 'terms': iterms = 14 if terms >= 30 else 7; truth = 'hold'
    if kind == 'vat': ivat = 25; truth = 'hold'
    inv = invoice(v, f'INV-2026-{1000 + i * 7}', svc, ifee, iterms, ivat)
    pairs.append({'i': i, 'vendor': v, 'truth': truth, 'kind': kind, 'contract': c, 'invoice': inv})
json.dump(pairs, open('pairs.json', 'w'), indent=1)
print(len(pairs), 'pairs,', sum(p['truth'] == 'hold' for p in pairs), 'planted')
