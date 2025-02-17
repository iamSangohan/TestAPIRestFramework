<<<<<<< HEAD
from django.urls import reverse, reverse_lazy
from rest_framework.test import APITestCase

from shop.models import Category, Product


class ShopAPITestCase(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='Fruits', active=True)
        Category.objects.create(name='Legumes', active=False)
        
        cls.product = cls.category.products.create(name='Ananas', active=True)
        cls.category.products.create(name='Banane', active=False)

        cls.category_2 = Category.objects.create(name='Légumes', active=True)
        cls.product_2 = cls.category_2.products.create(name='Tomate', active=True)

    def format_datetime(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


class TestCategory(ShopAPITestCase):
    url = reverse_lazy('category-list')
    
    def test_detail(self):
        url_detail = reverse('category-detail', kwargs={'pk': self.category.pk})
        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, 200)
        
        excepted = {
            'id': self.category.pk,
            'name': self.category.name,
            'date_created': self.format_datetime(self.category.date_created),
            'date_updated': self.format_datetime(self.category.date_updated),
            'products': self.get_product_detail_data(self.category.products.filter(active=True)),
        }
        self.assertEqual(excepted, response.json())
    
    def test_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
        excepted = [
            {
                'id' : category.pk,
                'name' : category.name,
                'date_created' : self.format_datetime(category.date_created),
                'date_updated' : self.format_datetime(category.date_updated),
            } for category in [self.category, self.category_2]
        ]
        self.assertEqual(excepted, response.json())
        
    def test_create(self):
        self.assertFalse(Category.objects.exists())
        response = self.client.post(self.url, data={'name': 'Nouvelle catégorie'})
        self.assertEqual(response.status_code, 405)
        self.assertFalse(Category.objects.exists())
        

class TestProduct(ShopAPITestCase):
    
    url = reverse_lazy('product-list')
    
    def test_detail(self):
        url_detail = reverse('product-detail', kwargs={'pk': self.product.pk})
        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, 200)
        
        excepted = {
            'id': self.product.pk,
            'name': self.product.name,
            'date_created': self.format_datetime(self.product.date_created),
            'date_updated': self.format_datetime(self.product.date_updated),
            'products': self.get_product_detail_data(self.product.products.filter(active=True)),
        }
        self.assertEqual(excepted, response.json())

    def get_product_detail_data(self, products):
        return [
            {
                'id': product.pk,
                'name': product.name,
                'date_created': self.format_datetime(product.date_created),
                'date_updated': self.format_datetime(product.date_updated),
                'category': product.category_id
            } for product in products
        ]

    def test_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_product_detail_data([self.product, self.product_2]), response.json())

    def test_list_filter(self):
        response = self.client.get(self.url + '?category_id=%i' % self.category.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_product_detail_data([self.product]), response.json())

    def test_create(self):
        product_count = Product.objects.count()
        response = self.client.post(self.url, data={'name': 'Nouvelle catégorie'})
        self.assertEqual(response.status_code, 405)
        self.assertEqual(Product.objects.count(), product_count)

    def test_delete(self):
        response = self.client.delete(reverse('product-detail', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 405)
        self.product.refresh_from_db()
=======
from django.urls import reverse_lazy, reverse
from rest_framework.test import APITestCase

from shop.models import Category, Product


class ShopAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='Fruits', active=True)
        Category.objects.create(name='Légumes', active=False)

        cls.product = cls.category.products.create(name='Ananas', active=True)
        cls.category.products.create(name='Banane', active=False)

        cls.category_2 = Category.objects.create(name='Légumes', active=True)
        cls.product_2 = cls.category_2.products.create(name='Tomate', active=True)

    def format_datetime(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def get_article_list_data(self, articles):
        return [
            {
                'id': article.pk,
                'name': article.name,
                'date_created': self.format_datetime(article.date_created),
                'date_updated': self.format_datetime(article.date_updated),
                'product': article.product_id
            } for article in articles
        ]

    def get_product_list_data(self, products):
        return [
            {
                'id': product.pk,
                'name': product.name,
                'date_created': self.format_datetime(product.date_created),
                'date_updated': self.format_datetime(product.date_updated),
                'category': product.category_id,
            } for product in products
        ]

    def get_category_list_data(self, categories):
        return [
            {
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'date_created': self.format_datetime(category.date_created),
                'date_updated': self.format_datetime(category.date_updated),
            } for category in categories
        ]


class TestCategory(ShopAPITestCase):

    url = reverse_lazy('category-list')

    def test_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['results'], self.get_category_list_data([self.category, self.category_2]))

    def test_create(self):
        category_count = Category.objects.count()
        response = self.client.post(self.url, data={'name': 'Nouvelle catégorie'})
        self.assertEqual(response.status_code, 405)
        self.assertEqual(Category.objects.count(), category_count)


class TestProduct(ShopAPITestCase):

    url = reverse_lazy('product-list')

    def test_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_product_list_data([self.product, self.product_2]), response.json()['results'])

    def test_list_filter(self):
        response = self.client.get(self.url + '?category_id=%i' % self.category.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_product_list_data([self.product]), response.json()['results'])

    def test_create(self):
        product_count = Product.objects.count()
        response = self.client.post(self.url, data={'name': 'Nouvelle catégorie'})
        self.assertEqual(response.status_code, 405)
        self.assertEqual(Product.objects.count(), product_count)

    def test_delete(self):
        response = self.client.delete(reverse('product-detail', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 405)
        self.product.refresh_from_db()
>>>>>>> upstream/P2C4_exercice
