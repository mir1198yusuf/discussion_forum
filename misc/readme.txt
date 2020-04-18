These diagrams are just rough sketched and original web pages might be little different.

during testing, I observed that in all test classes, setUpTestData() was executed for all test methods like setUp(). Maybe due to non-available of transactional support by database as django documentation states. So setUpTestData() and setUp() makes no difference HERE.

for markdown  editor reference was taken from this link : https://developpaper.com/implementation-of-beautiful-django-markdown-rich-text-app-plug-in/  