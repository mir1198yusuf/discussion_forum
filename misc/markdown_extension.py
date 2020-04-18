#https://github.com/Python-Markdown/markdown/blob/master/docs/change_log/release-3.0.md#safe_mode-and-html_replacement_text-keywords-deprecated

from markdown.extensions import Extension 

class EscapeHTML(Extension):
	def extendMarkdown(self, md):
		md.preprocessors.deregister('html_block')
		md.inlinePatterns.deregister('html')

#this is alt to safe_mode='escape' of markdown as suggested in link