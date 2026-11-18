"""Fill in the Nest Rows App Store Connect page. Safe to run again: it only fills or updates fields.
NEVER submits for review, never deletes anything."""
import hashlib, json, os, time, urllib.request, urllib.error
import jwt

KEY_ID, ISSUER, P8 = os.environ.get('ASC_KEY_ID'), os.environ.get('ASC_ISSUER_ID'), os.environ.get('ASC_KEY_P8')
if not (KEY_ID and ISSUER and P8):
    print('::warning::App Store Connect secrets are not set on this repo yet, so nothing was changed.'); raise SystemExit(0)
APP = '6834034291'            # Nest Rows
TEMPLATE_APP = '6829033479'   # Knot Wizard: review contact and age-rating answers are copied from it
VERSION = '1.0.3'             # must equal MARKETING_VERSION in android-app/ios/App/App.xcodeproj
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://halfgridgames-ai.github.io'
PRIVACY = SITE + '/nest-rows/privacy.html'

NAME = 'Nest Rows: Owl Logic Puzzle'
SUBTITLE = 'Relaxing Grid Brain Teaser'
KEYWORDS = 'tents,trees,sudoku,nonogram,deduction,mind,calm,daily,offline,zen,iq,riddle,bird,cute,casual,smart'
PROMO = ('One owl beside every nest, no two owls touching. 65 hand-made puzzles across 4 night-time woods, '
         'plus a new Daily Roost every night.')
DESCRIPTION = """Night has fallen on the woods, and every owl needs a branch.

Nest Rows is a calm logic puzzle. Each tree hollow wants exactly one owl on a branch beside it, no two owls may touch, not even corner to corner, and the numbers on the edges tell you how many owls sit in each row and column. Tap a branch to land an owl. When a tree is guarded, the owlet in its hollow pops out and hoots.

• 65 levels across 4 woods: the Saplings, Hollow Grove, Moonfall Pines and the Old Oak
• Every puzzle has one solution you can reach by pure logic, never by guessing
• A new Daily Roost every night, with a streak to keep
• Stuck? A hint places the next owl or tuft and explains why
• Grass tufts mark the branches you have ruled out, and undo is always there
• Six hand-painted owls to collect: earn stars for the Tawny and Snowy owls, keep a 7-night streak for the Starry Owl, or add the Moonlit and Ember owls with the Feather Pack
• Win poses for every owl: a party hat for 3 stars, sunglasses for 2, a nightcap for 1
• A risograph print look: bold inks, glowing fireflies and a different night sky in every wood
• Made for iPhone and iPad
• A short guided tutorial teaches the rules one at a time
• Play offline, anywhere, with one finger

Nest Rows contains optional ads and in-app purchases."""
NOTES = open(os.path.join(HERE, 'review-notes.txt')).read().strip()
COPYRIGHT = '2026 Half Grid Games'
LOCALES = ['en-GB', 'en-US']

IAPS = [  # productId, type, reference name, display name, description (<=55), price in GBP
    ('nr_remove_ads', 'NON_CONSUMABLE', 'Nest Rows Remove Ads', 'Remove Ads', 'No more ads between levels.', '2.99'),
    ('nr_hints_10', 'CONSUMABLE', 'Nest Rows 10 Hints', '10 Hints', 'Ten hints that explain the next step.', '0.99'),
    ('nr_hints_40', 'CONSUMABLE', 'Nest Rows 40 Hints', '40 Hints', 'Forty hints for the toughest woods.', '2.99'),
    ('nr_feather_pack', 'NON_CONSUMABLE', 'Nest Rows Feather Pack', 'Feather Pack', 'Adds the Moonlit Owl and the Ember Owl.', '1.99'),
]
IAP_NOTE = 'Open Shop from the main menu. The shop also has Restore purchases. Screenshot attached.'


def token():
    now = int(time.time())
    return jwt.encode({'iss': ISSUER, 'iat': now, 'exp': now + 1100, 'aud': 'appstoreconnect-v1'}, P8,
                      algorithm='ES256', headers={'kid': KEY_ID, 'typ': 'JWT'})


def api(path, method='GET', body=None, quiet=False):
    req = urllib.request.Request('https://api.appstoreconnect.apple.com' + path, method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={'Authorization': 'Bearer ' + token(), 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as r:
            s = r.read()
            return json.loads(s) if s else {}
    except urllib.error.HTTPError as e:
        if not quiet:
            print('  !', method, path.split('?')[0], e.code, e.read().decode()[:700])
        return None


def get_all(path):
    out, url = [], path
    while url:
        r = api(url)
        if not r: break
        out += r.get('data', [])
        nxt = (r.get('links') or {}).get('next')
        url = nxt.replace('https://api.appstoreconnect.apple.com', '') if nxt else None
    return out


def rel(t, i): return {'data': {'type': t, 'id': i}}


def ok(label, r): print(('  ok    ' if r is not None else '  FAIL  ') + label)


def section(t): print('\n== ' + t)


# ---------------------------------------------------------------- app info: name, subtitle, privacy, categories
section('App info (name, subtitle, privacy URL, categories)')
infos = api(f'/v1/apps/{APP}/appInfos')['data']
info = next((i for i in infos if i['attributes'].get('appStoreState') != 'READY_FOR_SALE'), infos[0])
ok('categories Games > Puzzle, Board', api(f"/v1/appInfos/{info['id']}", 'PATCH', {'data': {
    'type': 'appInfos', 'id': info['id'], 'relationships': {
        'primaryCategory': rel('appCategories', 'GAMES'),
        'primarySubcategoryOne': rel('appCategories', 'GAMES_PUZZLE'),
        'primarySubcategoryTwo': rel('appCategories', 'GAMES_BOARD')}}}))
locs = {l['attributes']['locale']: l for l in api(f"/v1/appInfos/{info['id']}/appInfoLocalizations")['data']}
attrs = {'name': NAME, 'subtitle': SUBTITLE, 'privacyPolicyUrl': PRIVACY}
assert len(NAME) <= 30 and len(SUBTITLE) <= 30 and len(KEYWORDS) <= 100 and len(PROMO) <= 170
for loc in LOCALES:
    if loc in locs:
        r = api(f"/v1/appInfoLocalizations/{locs[loc]['id']}", 'PATCH', {'data': {'type': 'appInfoLocalizations', 'id': locs[loc]['id'], 'attributes': attrs}})
    else:
        r = api('/v1/appInfoLocalizations', 'POST', {'data': {'type': 'appInfoLocalizations', 'attributes': {'locale': loc, **attrs},
                                                             'relationships': {'appInfo': rel('appInfos', info['id'])}}})
    ok(f'{loc} name/subtitle/privacy', r)

# ---------------------------------------------------------------- age rating (copied from Knot Wizard, a 4+ puzzle)
section('Age rating')
tinfo = api(f'/v1/apps/{TEMPLATE_APP}/appInfos')['data'][0]
tar = api(f"/v1/appInfos/{tinfo['id']}/ageRatingDeclaration")['data']
ar = api(f"/v1/appInfos/{info['id']}/ageRatingDeclaration")['data']
a = {k: v for k, v in tar['attributes'].items() if v is not None}
print('  answers:', json.dumps(a))
ok('age rating', api(f"/v1/ageRatingDeclarations/{ar['id']}", 'PATCH', {'data': {'type': 'ageRatingDeclarations', 'id': ar['id'], 'attributes': a}}))

# ---------------------------------------------------------------- content rights
section('Content rights')
ok('no third-party content', api(f'/v1/apps/{APP}', 'PATCH', {'data': {'type': 'apps', 'id': APP, 'attributes': {'contentRightsDeclaration': 'DOES_NOT_USE_THIRD_PARTY_CONTENT'}}}))

# ---------------------------------------------------------------- version: number, copyright, listing text
section('Version ' + VERSION)
vers = api(f'/v1/apps/{APP}/appStoreVersions?filter[platform]=IOS&limit=10')['data']
editable = [v for v in vers if v['attributes']['appStoreState'] in ('PREPARE_FOR_SUBMISSION', 'DEVELOPER_REJECTED', 'REJECTED', 'METADATA_REJECTED')]
for v in vers: print('  found', v['attributes']['versionString'], v['attributes']['appStoreState'])
if not editable:
    raise SystemExit('No editable version (already submitted?). Nothing changed below this point.')
ver = editable[0]
ok(f"version {ver['attributes']['versionString']} -> {VERSION}, copyright", api(f"/v1/appStoreVersions/{ver['id']}", 'PATCH', {'data': {
    'type': 'appStoreVersions', 'id': ver['id'], 'attributes': {'versionString': VERSION, 'copyright': COPYRIGHT}}}))
vlocs = {l['attributes']['locale']: l for l in api(f"/v1/appStoreVersions/{ver['id']}/appStoreVersionLocalizations")['data']}
vattrs = {'description': DESCRIPTION, 'keywords': KEYWORDS, 'promotionalText': PROMO, 'supportUrl': SITE, 'marketingUrl': SITE}
for loc in LOCALES:
    if loc in vlocs:
        r = api(f"/v1/appStoreVersionLocalizations/{vlocs[loc]['id']}", 'PATCH', {'data': {'type': 'appStoreVersionLocalizations', 'id': vlocs[loc]['id'], 'attributes': vattrs}})
    else:
        r = api('/v1/appStoreVersionLocalizations', 'POST', {'data': {'type': 'appStoreVersionLocalizations', 'attributes': {'locale': loc, **vattrs},
                                                                      'relationships': {'appStoreVersion': rel('appStoreVersions', ver['id'])}}})
    ok(f'{loc} description/keywords/promo/URLs', r)
for loc, l in vlocs.items():
    n = len(get_all(f"/v1/appStoreVersionLocalizations/{l['id']}/appScreenshotSets"))
    print(f'  {loc}: {n} screenshot sets')

# ---------------------------------------------------------------- review details (contact copied from Knot Wizard)
section('App Review information')
tver = api(f'/v1/apps/{TEMPLATE_APP}/appStoreVersions?filter[platform]=IOS&limit=5')['data']
contact = {}
for tv in tver:
    d = (api(f"/v1/appStoreVersions/{tv['id']}/appStoreReviewDetail", quiet=True) or {}).get('data')
    if d and d['attributes'].get('contactEmail'):
        contact = {k: d['attributes'][k] for k in ('contactFirstName', 'contactLastName', 'contactPhone', 'contactEmail') if d['attributes'].get(k)}
        break
rattrs = {**contact, 'demoAccountRequired': False, 'notes': NOTES}
rd = (api(f"/v1/appStoreVersions/{ver['id']}/appStoreReviewDetail", quiet=True) or {}).get('data')
if rd:
    r = api(f"/v1/appStoreReviewDetails/{rd['id']}", 'PATCH', {'data': {'type': 'appStoreReviewDetails', 'id': rd['id'], 'attributes': rattrs}})
else:
    r = api('/v1/appStoreReviewDetails', 'POST', {'data': {'type': 'appStoreReviewDetails', 'attributes': rattrs,
                                                         'relationships': {'appStoreVersion': rel('appStoreVersions', ver['id'])}}})
ok('review notes + contact ' + ('(copied from Knot Wizard)' if contact else '(NO contact found, fill in by hand)'), r)

# ---------------------------------------------------------------- territories
territories = [t['id'] for t in get_all('/v1/territories?limit=200')]
print(f'\n{len(territories)} territories')

# ---------------------------------------------------------------- app price (free) and availability (all but China)
section('Price and availability')
if not (api(f'/v1/apps/{APP}/appPriceSchedule', quiet=True) or {}).get('data'):
    free = next((p for p in get_all(f'/v1/apps/{APP}/appPricePoints?filter[territory]=GBR&limit=200')
                 if float(p['attributes']['customerPrice']) == 0), None)
    ok('free price', free and api('/v1/appPriceSchedules', 'POST', {
        'data': {'type': 'appPriceSchedules', 'relationships': {'app': rel('apps', APP), 'baseTerritory': rel('territories', 'GBR'),
                                                                 'manualPrices': {'data': [{'type': 'appPrices', 'id': '${p0}'}]}}},
        'included': [{'type': 'appPrices', 'id': '${p0}', 'attributes': {'startDate': None},
                      'relationships': {'appPricePoint': rel('appPricePoints', free['id'])}}]}))
else:
    print('  price already set')
if not (api(f'/v1/apps/{APP}/appAvailabilityV2', quiet=True) or {}).get('data'):
    inc = [{'type': 'territoryAvailabilities', 'id': f'${{{t}}}', 'attributes': {'available': t != 'CHN'},
            'relationships': {'territory': rel('territories', t)}} for t in territories]
    ok('available everywhere except China mainland', api('/v2/appAvailabilities', 'POST', {
        'data': {'type': 'appAvailabilities', 'attributes': {'availableInNewTerritories': True},
                 'relationships': {'app': rel('apps', APP), 'territoryAvailabilities': {'data': [{'type': i['type'], 'id': i['id']} for i in inc]}}},
        'included': inc}))
else:
    print('  availability already set')

# ---------------------------------------------------------------- in-app purchases
section('In-app purchases')
shot = open(os.path.join(HERE, 'iap-review-shop.png'), 'rb').read()
existing = {i['attributes']['productId']: i for i in get_all(f'/v1/apps/{APP}/inAppPurchasesV2?limit=50')}
for pid, kind, ref, disp, desc, price in IAPS:
    print(' ', pid)
    iap = existing.get(pid)
    if not iap:
        r = api('/v2/inAppPurchases', 'POST', {'data': {'type': 'inAppPurchases', 'attributes': {
            'name': ref, 'productId': pid, 'inAppPurchaseType': kind, 'reviewNote': IAP_NOTE, 'familySharable': False},
            'relationships': {'app': rel('apps', APP)}}})
        if not r: continue
        iap = r['data']
        ok('created', r)
    iid = iap['id']
    have = {l['attributes']['locale'] for l in get_all(f'/v2/inAppPurchases/{iid}/inAppPurchaseLocalizations')}
    for loc in LOCALES:
        if loc not in have:
            ok(f'{loc} name/description', api('/v1/inAppPurchaseLocalizations', 'POST', {'data': {'type': 'inAppPurchaseLocalizations',
                'attributes': {'locale': loc, 'name': disp, 'description': desc}, 'relationships': {'inAppPurchaseV2': rel('inAppPurchases', iid)}}}))
    if not (api(f'/v2/inAppPurchases/{iid}/iapPriceSchedule', quiet=True) or {}).get('data'):
        pp = next((p for p in get_all(f'/v2/inAppPurchases/{iid}/pricePoints?filter[territory]=GBR&limit=200')
                   if p['attributes']['customerPrice'] in (price, price.rstrip('0'))), None)
        ok(f'price £{price}', pp and api('/v1/inAppPurchasePriceSchedules', 'POST', {
            'data': {'type': 'inAppPurchasePriceSchedules', 'relationships': {
                'inAppPurchase': rel('inAppPurchases', iid), 'baseTerritory': rel('territories', 'GBR'),
                'manualPrices': {'data': [{'type': 'inAppPurchasePrices', 'id': '${p0}'}]}}},
            'included': [{'type': 'inAppPurchasePrices', 'id': '${p0}', 'attributes': {'startDate': None},
                          'relationships': {'inAppPurchasePricePoint': rel('inAppPurchasePricePoints', pp['id'])}}]}))
    if not (api(f'/v2/inAppPurchases/{iid}/inAppPurchaseAvailability', quiet=True) or {}).get('data'):
        ok('availability', api('/v1/inAppPurchaseAvailabilities', 'POST', {'data': {'type': 'inAppPurchaseAvailabilities',
            'attributes': {'availableInNewTerritories': True},
            'relationships': {'inAppPurchase': rel('inAppPurchases', iid),
                              'availableTerritories': {'data': [{'type': 'territories', 'id': t} for t in territories if t != 'CHN']}}}}))
    if not (api(f'/v2/inAppPurchases/{iid}/appStoreReviewScreenshot', quiet=True) or {}).get('data'):
        r = api('/v1/inAppPurchaseAppStoreReviewScreenshots', 'POST', {'data': {'type': 'inAppPurchaseAppStoreReviewScreenshots',
            'attributes': {'fileName': 'nest-rows-shop.png', 'fileSize': len(shot)}, 'relationships': {'inAppPurchaseV2': rel('inAppPurchases', iid)}}})
        if r:
            sid = r['data']['id']
            for op in r['data']['attributes']['uploadOperations']:
                part = shot[op['offset']:op['offset'] + op['length']]
                req = urllib.request.Request(op['url'], data=part, method=op['method'], headers={h['name']: h['value'] for h in op['requestHeaders']})
                urllib.request.urlopen(req).read()
            ok('review screenshot', api(f'/v1/inAppPurchaseAppStoreReviewScreenshots/{sid}', 'PATCH', {'data': {
                'type': 'inAppPurchaseAppStoreReviewScreenshots', 'id': sid,
                'attributes': {'uploaded': True, 'sourceFileChecksum': hashlib.md5(shot).hexdigest()}}}))
    st = api(f'/v2/inAppPurchases/{iid}')
    print('    state:', st and st['data']['attributes'].get('state'))

# ---------------------------------------------------------------- build
section('Build')
builds = get_all(f'/v1/builds?filter[app]={APP}&filter[preReleaseVersion.version]={VERSION}&filter[processingState]=VALID&sort=-uploadedDate&limit=10')
if builds:
    b = builds[0]
    ok(f"attach build {b['attributes']['version']} ({VERSION})", api(f"/v1/appStoreVersions/{ver['id']}/relationships/build", 'PATCH', {'data': {'type': 'builds', 'id': b['id']}}))
    if b['attributes'].get('usesNonExemptEncryption') is None:
        ok('export compliance: no non-exempt encryption', api(f"/v1/builds/{b['id']}", 'PATCH', {'data': {'type': 'builds', 'id': b['id'], 'attributes': {'usesNonExemptEncryption': False}}}))
else:
    print(f'  no processed {VERSION} build yet (the iOS build workflow uploads one once the GitHub secrets exist)')

print('\nDone. Nothing was submitted. Still by hand in App Store Connect: App Privacy answers, then Add for Review + Submit.')
