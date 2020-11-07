import json
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takto_api.settings')
django.setup(set_prefix='')


def main():
    from takto_api.apps.business.models import Business, Category

    exists_business_ids = set(Business.objects.values_list('business_id', flat=True))

    with open('dev/yelp_dataset/yelp_academic_dataset_business.json') as yelp_business:
        business_buff = []
        categories_buff = []

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
                categories_buff.append([cat.strip() for cat in business['categories'].split(',')])
            else:
                categories_buff.append([])

            if len(business_buff) > 1023:
                business_buff = Business.objects.bulk_create(business_buff)

                Category.objects.bulk_create([
                    Category(business=business, name=category)
                    for business, categories in zip(business_buff, categories_buff)
                    for category in categories
                ])

                print('flush:', len(business_buff))
                business_buff = []
                categories_buff = []


if __name__ == '__main__':
    main()
