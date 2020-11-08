import json
import os
import re
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takto_api.settings')
django.setup(set_prefix='')
dir_path = os.path.dirname(os.path.realpath(__file__))


def create_categories():
    from takto_api.apps.business.models import Category

    categories = set()

    with open(f'{dir_path}/dev/yelp_dataset/yelp_academic_dataset_business.json') as yelp_business:

        for row in yelp_business:
            business = json.loads(row)

            if 'categories' in business and business['categories']:
                business_categories = [cat.strip() for cat in business['categories'].split(',')]
                categories.update(business_categories)

    return Category.objects.bulk_create([Category(name=name) for name in categories])


def create_business():
    from django.db import connection

    from takto_api.apps.business.models import Business

    business_buff = []
    categories_buff = []

    def flush():
        nonlocal business_buff, categories_buff

        business_buff = Business.objects.bulk_create(business_buff)

        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO "business_business_categories" ("business_id", "category_id") VALUES ' +
                ', '.join(
                    f'({business.id}, {category.id})'
                    for business, categories in zip(business_buff, categories_buff)
                    for category in categories
                ) +
                ' ON CONFLICT DO NOTHING'
            )

        result = len(business_buff)
        business_buff = []
        categories_buff = []
        return result

    category_by_name = {
        category.name: category
        for category in create_categories()
    }

    exists_business_ids = set(Business.objects.values_list('business_id', flat=True))

    with open(f'{dir_path}/dev/yelp_dataset/yelp_academic_dataset_business.json') as yelp_business:

        for row in yelp_business:
            business = json.loads(row)

            if business["business_id"] in exists_business_ids or len(business['state']) > 2:
                continue

            business_buff.append(Business(
                business_id=business['business_id'],
                name=business['name'],
                state=business['state'],
                city=business['city'],
                address=business['address'],
                postal_code=business['postal_code'],
                latitude=business['latitude'],
                longitude=business['longitude'],
                stars=business['stars'],
                review_count=business['review_count'],
                is_open=bool(business['is_open']) and business['hours'] is not None,
                attributes=business['attributes'],
                hours=business['hours'],
            ))

            if 'categories' in business and business['categories']:
                categories_buff.append([category_by_name[name.strip()] for name in business['categories'].split(',')])
            else:
                categories_buff.append([])

            if len(business_buff) > 1023:
                print('flush:', flush())

    print('flush:', flush())


def create_business_photos():
    from takto_api.apps.business.models import Business, Photo

    photo_buff = []

    def flush():
        nonlocal photo_buff

        Photo.objects.bulk_create(photo_buff)

        result = len(photo_buff)
        photo_buff = []
        return result

    business_by_id = {business.business_id: business for business in Business.objects.all()}
    print('load all business')

    with open(f'{dir_path}/dev/yelp_dataset/photos.json') as yelp_business:
        for row in yelp_business:
            photo = json.loads(row)
            photo_buff.append(Photo(
                photo_id=photo['photo_id'],
                caption=photo['caption'],
                label=photo['label'],
                business=business_by_id[photo['business_id']]
            ))

            if len(photo_buff) > 1023:
                print('flush:', flush())

    print('flush:', flush())


convert_values = {
    'yes': 'true',
    'yes_corkage': 'true',
    'no': 'false',
    'yes_free': 'free'
}


def write_csv():
    def prepare_string(value: str):
        value = value.lower()

        if value[0] == "'" and value[-1] == "'":
            value = value[1:-1]

        elif value[:2] == "u'" and value[-1] == "'":
            value = value[2:-1]

        return convert_values.get(value, value)

    with open(f'{dir_path}/dev/yelp_dataset/yelp_academic_dataset_business.json') as src, open(f'{dir_path}/business.csv', 'w') as dest:
        dest.write('business_id,name,starts,categories,attributes,latitude,longitude\n')

        for row in src:
            business = json.loads(row)

            business_id = business['business_id']
            name = re.sub(r'[^\w]+', '|', business['name']).lower()
            starts = business['stars']

            if business['categories']:
                categories = business['categories'].replace(", ", "|").lower()
            else:
                categories = ''

            if business['attributes']:
                attributes = '|'.join(
                    prepare_string(key) + '_' + prepare_string(value)
                    for key, value in business['attributes'].items()
                    if '{' not in value and prepare_string(value) != 'none'
                )
            else:
                attributes = ''

            latitude = business['latitude']
            longitude = business['longitude']

            dest.write(f'{business_id},"{name}",{starts},"{categories}","{attributes}",{latitude},{longitude}\n')


if __name__ == '__main__':
    # create_business()
    # create_business_photos()
    write_csv()
