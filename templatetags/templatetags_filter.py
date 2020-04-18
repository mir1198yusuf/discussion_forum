from django import template
from urllib.parse import urlencode
import hashlib

register = template.Library()

@register.filter
def red_border_if_error_filter(field):
	"""
	This filter will give red border css class name if form field has errors
	"""
	if field.errors:
		return 'w3-border w3-border-red'
	else:
		return ''

@register.simple_tag(takes_context=True)
def get_pagination_values_3(context):
	"""
	This tag will return three numbers which should be present on pagination links
	according to current page number. will be called when no of pages > 3
	"""
	current_pageno = context.get('page_obj').number
	if current_pageno == 1:
		return (current_pageno, current_pageno+1, current_pageno+2)
	elif current_pageno == context.get('paginator').num_pages:
		return (current_pageno-2, current_pageno-1, current_pageno)
	else:
		return (current_pageno-1, current_pageno, current_pageno+1)

@register.simple_tag
def call_method(object, method_name, *args):
	"""
	This tag is used to call any method from template and pass arguments
	Pass method name as string
	"""
	method = getattr(object, method_name)
	#now method will have bound method of object class
	#so object.method is not needed direct method() will work
	return method(*args)

@register.filter
def gravatar_url(user):
	"""
	This filter will return a link for gravatar image of user
	https://simpleisbetterthancomplex.com/series/2017/10/09/a-complete-beginners-guide-to-django-part-6.html#gravatar
	https://en.gravatar.com/site/implement/images/python/
	https://en.gravatar.com/site/implement/images/django/
	"""
	email = user.email.lower().encode('utf-8')
	default = ''	#kept as blank to get default gravatar logo
	size = 48 
	url = 'https://www.gravatar.com/avatar/{md5}?{params}'.format(
		md5 = hashlib.md5(email).hexdigest(),
		params = urlencode({'d':default, 's':str(size)})
		)
	#url is something like - https://www.gravatar.com/avatar/d41d8cd98f04e9800998ecf8427e?d=&s=48
	return url

