"""
Run from your project root:
    python manage.py shell < seed_products.py
"""

import django, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_project.settings")
django.setup()

from producers.models import Producer
from products.models import Product

# Map producer username -> list of products to create
PRODUCTS = {
    "avon.growers": [
        dict(name="Mixed Salad Leaves", description="A fresh blend of seasonal salad leaves grown along the Avon Valley. Perfect for summer salads.", price=2.50, stock=80, is_organic=False, unit_value=150, unit="g", category="vegetables", section="all", availability_mode="year_round"),
        dict(name="Courgettes", description="Tender courgettes hand-picked at the perfect size. Great for roasting or stir-frying.", price=1.80, stock=60, is_organic=False, unit_value=1, unit="kg", category="vegetables", section="all", availability_mode="seasonal", season_start_month=6, season_end_month=9),
        dict(name="Cherry Tomatoes", description="Sweet, vine-ripened cherry tomatoes bursting with flavour.", price=2.20, stock=100, is_organic=False, unit_value=500, unit="g", category="vegetables", section="all", availability_mode="seasonal", season_start_month=7, season_end_month=10),
        dict(name="Cucumber", description="Crisp, refreshing cucumbers grown in polytunnels along the Avon Valley.", price=1.00, stock=70, is_organic=False, unit_value=1, unit="each", category="vegetables", section="all", availability_mode="year_round"),
        dict(name="Spring Onions", description="Mild and crisp spring onions, sold in a generous bunch.", price=0.90, stock=90, is_organic=False, unit_value=1, unit="each", category="vegetables", section="all", availability_mode="seasonal", season_start_month=4, season_end_month=9),
    ],
    "bristol.organics": [
        dict(name="Organic Carrots", description="Certified organic carrots grown on the outskirts of Bristol. Naturally sweet and full of flavour.", price=1.60, stock=120, is_organic=True, unit_value=1, unit="kg", category="vegetables", section="all", availability_mode="year_round"),
        dict(name="Organic Spinach", description="Tender organic spinach leaves, freshly harvested. Ideal for salads or wilting into pasta.", price=2.80, stock=50, is_organic=True, unit_value=200, unit="g", category="vegetables", section="all", availability_mode="year_round"),
        dict(name="Organic Whole Milk", description="Full-fat organic milk from grass-fed cows. Delivered fresh.", price=1.40, stock=60, is_organic=True, unit_value=1, unit="l", category="dairy", section="all", availability_mode="year_round"),
        dict(name="Organic Broccoli", description="Firm, fresh organic broccoli heads. Great steamed, roasted or in stir-fries.", price=1.90, stock=80, is_organic=True, unit_value=1, unit="each", category="vegetables", section="all", availability_mode="year_round"),
        dict(name="Organic Kale", description="Hearty organic kale, packed with nutrients. Perfect for smoothies and soups.", price=2.10, stock=70, is_organic=True, unit_value=250, unit="g", category="vegetables", section="all", availability_mode="year_round"),
    ],
    "cotswold.fresh": [
        dict(name="Whole Milk", description="Fresh full-fat milk from Cotswold dairy herds. Creamy and delicious.", price=1.20, stock=100, is_organic=False, unit_value=2, unit="l", category="dairy", section="all", availability_mode="year_round"),
        dict(name="Mature Cheddar", description="Traditionally made mature cheddar from the Cotswold hills. Rich and crumbly.", price=4.50, stock=40, is_organic=False, unit_value=400, unit="g", category="dairy", section="all", availability_mode="year_round"),
        dict(name="Strawberry Jam", description="Award-winning strawberry jam made with Cotswold-grown fruit and just enough sugar.", price=3.20, stock=55, is_organic=False, unit_value=340, unit="g", category="preserves", section="all", availability_mode="year_round"),
        dict(name="Clotted Cream", description="Indulgent clotted cream made the traditional way. Perfect with scones.", price=2.80, stock=35, is_organic=False, unit_value=227, unit="g", category="dairy", section="all", availability_mode="year_round"),
        dict(name="Raspberry Conserve", description="Thick, fruity raspberry conserve with whole fruit pieces. Great on toast or yoghurt.", price=3.50, stock=45, is_organic=False, unit_value=340, unit="g", category="preserves", section="all", availability_mode="year_round"),
    ],
    "green.valley.farm": [
        dict(name="Sourdough Loaf", description="Slow-fermented sourdough baked fresh each morning on the farm. Crusty outside, chewy inside.", price=3.80, stock=30, is_organic=False, unit_value=1, unit="each", category="bakery", section="all", availability_mode="year_round"),
        dict(name="Wholemeal Bread", description="Hearty wholemeal loaf made with stone-ground flour. Nutritious and filling.", price=2.90, stock=40, is_organic=False, unit_value=1, unit="each", category="bakery", section="all", availability_mode="year_round"),
        dict(name="Seasonal Vegetable Box", description="A curated box of whatever is freshest from the farm that week. Sustainable and varied.", price=12.00, stock=20, is_organic=False, unit_value=1, unit="each", category="vegetables", section="seasonal", availability_mode="year_round"),
        dict(name="Apple & Pear Mix", description="Hand-picked mix of apples and pears from the farm orchard. Perfect for snacking or baking.", price=3.00, stock=60, is_organic=False, unit_value=1, unit="kg", category="fruits", section="all", availability_mode="seasonal", season_start_month=9, season_end_month=11),
        dict(name="Farmhouse Scones", description="Freshly baked plain scones, six per pack. Best served warm with jam and clotted cream.", price=3.50, stock=25, is_organic=False, unit_value=6, unit="pack", category="bakery", section="all", availability_mode="year_round"),
    ],
    "mendip.hills.farm": [
        dict(name="Parsnips", description="Earthy, sweet parsnips grown in the mineral-rich Mendip soil. Great roasted.", price=1.50, stock=90, is_organic=False, unit_value=1, unit="kg", category="vegetables", section="all", availability_mode="seasonal", season_start_month=10, season_end_month=3),
        dict(name="Heritage Beetroot", description="A mix of heritage beetroot varieties — golden, candy stripe and deep red. Stunning on any plate.", price=2.40, stock=50, is_organic=False, unit_value=500, unit="g", category="vegetables", section="seasonal", availability_mode="seasonal", season_start_month=7, season_end_month=11),
        dict(name="Red Onions", description="Large, firm red onions with a mild flavour. Great raw in salads or caramelised.", price=1.30, stock=110, is_organic=False, unit_value=1, unit="kg", category="vegetables", section="all", availability_mode="year_round"),
        dict(name="Potatoes (Maris Piper)", description="Classic Maris Piper potatoes — ideal for chips, mash or roasties.", price=2.00, stock=150, is_organic=False, unit_value=2, unit="kg", category="vegetables", section="all", availability_mode="year_round"),
        dict(name="Swede", description="Large, dense swede grown on the Mendip Hills. Perfect for soups, stews and mash.", price=1.10, stock=80, is_organic=False, unit_value=1, unit="each", category="vegetables", section="all", availability_mode="seasonal", season_start_month=10, season_end_month=3),
    ],
    "river.bend.nursery": [
        dict(name="Strawberries", description="Sun-ripened strawberries grown by the River Frome. Eaten the same day they're picked.", price=3.00, stock=40, is_organic=False, unit_value=400, unit="g", category="fruits", section="seasonal", availability_mode="seasonal", season_start_month=6, season_end_month=8),
        dict(name="Blackberries", description="Plump, juicy blackberries picked fresh from the bushes. Perfect for crumbles and jams.", price=2.50, stock=35, is_organic=False, unit_value=300, unit="g", category="fruits", section="seasonal", availability_mode="seasonal", season_start_month=8, season_end_month=10),
        dict(name="Fresh Basil", description="Fragrant potted basil grown in the nursery. Snip as needed for pasta, pizza and salads.", price=1.80, stock=60, is_organic=False, unit_value=1, unit="each", category="vegetables", section="all", availability_mode="year_round"),
        dict(name="Mixed Fresh Herbs", description="A bunch of seasonal herbs — rosemary, thyme, sage and parsley — grown together.", price=2.00, stock=45, is_organic=False, unit_value=1, unit="each", category="vegetables", section="all", availability_mode="year_round"),
        dict(name="Raspberries", description="Sweet, delicate raspberries from the nursery's soft fruit beds. Ideal for desserts.", price=3.20, stock=30, is_organic=False, unit_value=250, unit="g", category="fruits", section="seasonal", availability_mode="seasonal", season_start_month=7, season_end_month=9),
    ],
    "severn.side.produce": [
        dict(name="White Cabbage", description="Large, firm white cabbages grown on the Severn Estuary. Great for coleslaw or braising.", price=1.20, stock=100, is_organic=False, unit_value=1, unit="each", category="vegetables", section="all", availability_mode="year_round"),
        dict(name="Leeks", description="Long, clean leeks with a mild flavour. A staple for soups, pies and gratins.", price=1.80, stock=90, is_organic=False, unit_value=1, unit="kg", category="vegetables", section="all", availability_mode="seasonal", season_start_month=9, season_end_month=4),
        dict(name="Cauliflower", description="Dense, creamy cauliflower heads. Roast whole, rice it, or make a classic cheese sauce.", price=1.60, stock=70, is_organic=False, unit_value=1, unit="each", category="vegetables", section="all", availability_mode="year_round"),
        dict(name="Brussels Sprouts", description="Firm, nutty Brussels sprouts from the estuary fields. Best roasted with a little bacon.", price=1.90, stock=80, is_organic=False, unit_value=500, unit="g", category="vegetables", section="seasonal", availability_mode="seasonal", season_start_month=10, season_end_month=2),
        dict(name="Butternut Squash", description="Sweet, golden butternut squash grown in long polytunnel rows. Perfect for soups and curries.", price=2.20, stock=65, is_organic=False, unit_value=1, unit="each", category="vegetables", section="all", availability_mode="seasonal", season_start_month=9, season_end_month=12),
    ],
    "wye.valley.growers": [
        dict(name="Wildflower Honey", description="Raw, unfiltered honey from hives placed across the Wye Valley meadows. Light and aromatic.", price=5.50, stock=40, is_organic=False, unit_value=340, unit="g", category="preserves", section="all", availability_mode="year_round"),
        dict(name="Blackcurrant Jam", description="Award-winning blackcurrant jam made from Wye Valley-grown fruit. Deep, intense flavour.", price=3.80, stock=50, is_organic=False, unit_value=340, unit="g", category="preserves", section="all", availability_mode="year_round"),
        dict(name="Gooseberries", description="Sharp, juicy gooseberries picked fresh. Ideal for crumbles, fools and jam making.", price=2.60, stock=30, is_organic=False, unit_value=350, unit="g", category="fruits", section="seasonal", availability_mode="seasonal", season_start_month=6, season_end_month=8),
        dict(name="Mixed Berry Compote", description="A rich compote of blueberries, raspberries and blackcurrants. Delicious on porridge or yoghurt.", price=4.00, stock=35, is_organic=False, unit_value=300, unit="g", category="preserves", section="all", availability_mode="year_round"),
        dict(name="Elderflower Cordial", description="Hand-crafted elderflower cordial made with flowers foraged from the Wye Valley hedgerows.", price=4.50, stock=25, is_organic=False, unit_value=500, unit="ml", category="preserves", section="seasonal", availability_mode="seasonal", season_start_month=5, season_end_month=7),
    ],
}

created = 0
skipped = 0

for username, items in PRODUCTS.items():
    try:
        producer = Producer.objects.get(user__username=username)
    except Producer.DoesNotExist:
        print(f"  [SKIP] Producer not found: {username}")
        skipped += len(items)
        continue

    for item in items:
        if Product.objects.filter(producer=producer, name=item["name"]).exists():
            print(f"  [EXISTS] {producer.display_name} — {item['name']}")
            skipped += 1
            continue

        Product.objects.create(producer=producer, **item)
        print(f"  [OK] {producer.display_name} — {item['name']}")
        created += 1

print(f"\nDone. {created} products created, {skipped} skipped.")
