# Copyright (c) 2026, ALYF GmbH and contributors
# For license information, please see license.txt

import re

import frappe
from frappe import _
from frappe.model.document import Document

from compendium.docs import normalize_path


class CompendiumPage(Document):
	def validate(self):
		self.path = normalize_path(self.path or slugify(self.title))
		if not self.path:
			frappe.throw(_("Please set a path for this page"))

		duplicate = frappe.db.exists(
			self.doctype, {"language": self.language, "path": self.path, "name": ("!=", self.name)}
		)
		if duplicate:
			frappe.throw(
				_("{0} already documents the path {1} in this language").format(
					frappe.get_desk_link(self.doctype, duplicate), frappe.bold(self.path)
				),
				frappe.DuplicateEntryError,
			)


def slugify(title):
	"""`Getting Started` → `getting-started`, like the Markdown file names apps ship.

	Mirrored in compendium_page.js, which fills the path while the title is typed.
	"""
	return re.sub(r"[\W_]+", "-", (title or "").lower()).strip("-")
