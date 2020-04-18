from django.test import TestCase
from tests.sample_loginform import SampleLogin_Form
from templatetags.templatetags_filter import *
from django.template import Template, Context
from django.core.paginator import Paginator
from tests.sample_class import SampleClass

class TemplateTagsFilters_Test(TestCase):

	"""
	1. check if red_border_if_error_filter is working properly
	2. check if get_pagination_values_3 tag is working properly
	3. check if call_method tag is working properly
	"""

	def test_1(self):
		"""
		the reason we are not using any form url because the output returns by filter might be present in the html code w/o intervention of filter say if someone has used red border class directly
		so we have create a new form class and check if it is/is not returning red border class on 3 types of data
		 1. unbounded form (no data)		2. bounded data + valid data 	3. bounded data + invalid data
		"""
		loginform_data_invalid = {'name':'', 'password':''}
		loginform_data_valid = {'name':'abc', 'password':'thisisabcpassword123'}
		loginform_unbound = SampleLogin_Form()
		loginform_bound_valid = SampleLogin_Form(loginform_data_valid)
		loginform_bound_invalid = SampleLogin_Form(loginform_data_invalid)
		##form.fields.get_field('name') -> give form.Charfield w/o data , but only with properties
		##form.__getitem__('name') or form['name'] -> give actual html field with data if passed, error if any
		# 1. Unbounded form -> there should be no errors so no red border css class name
		self.assertEqual('', red_border_if_error_filter(loginform_unbound['name']))
		self.assertEqual('', red_border_if_error_filter(loginform_unbound['password']))
		# 2. Bounded form + valid data -> there should be no errors so no red border css class name
		self.assertEqual('', red_border_if_error_filter(loginform_unbound['name']))
		self.assertEqual('', red_border_if_error_filter(loginform_unbound['password']))
		# 3. Bounded form + invalid data -> should give red border css class name as it has errors
		self.assertEqual('w3-border w3-border-red', red_border_if_error_filter(loginform_bound_invalid['name']))
		self.assertEqual('w3-border w3-border-red', red_border_if_error_filter(loginform_bound_invalid['password']))

	def test_2(self):
		#this template tag will be called when no of pages > 3
		queryset = [1,2,3,4,5,6,7,8]	
		paginator = Paginator(queryset, 2)
		#paginator.num_pages = 4 :  1 2 3 4 
		template = Template('{% load custom_tags_filters %} {% get_pagination_values_3 as pagination_list %}')
		#case 1 :when current  page is 1
		page_obj = paginator.page(1)
		context = Context({'paginator':paginator, 'page_obj':page_obj})
		template.render(context)
		self.assertSequenceEqual(context.get('pagination_list'), (1,2,3))
		#case 2 :when current  page is 2
		page_obj = paginator.page(2)
		context = Context({'paginator':paginator, 'page_obj':page_obj})
		template.render(context)
		self.assertSequenceEqual(context.get('pagination_list'), (1,2,3))
		#case 3 :when current  page is 3
		page_obj = paginator.page(3)
		context = Context({'paginator':paginator, 'page_obj':page_obj})
		template.render(context)
		self.assertSequenceEqual(context.get('pagination_list'), (2,3,4))
		#case 4 :when current  page is 4
		page_obj = paginator.page(4)
		context = Context({'paginator':paginator, 'page_obj':page_obj})
		template.render(context)
		self.assertSequenceEqual(context.get('pagination_list'), (2,3,4))

	def test_3(self):
		obj = SampleClass()
		template = Template('{% load custom_tags_filters %} {% call_method obj "samplemethod" 1 2 3 as datalist %}')
		context = Context({'obj':obj})
		template.render(context)
		self.assertSequenceEqual(context.get('datalist'), (1,2,3))