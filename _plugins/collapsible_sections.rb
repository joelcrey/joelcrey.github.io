# Collapsible sections: with `collapsible: true` in the front matter of a page or post, every
# section under a `##` heading becomes a block that opens and closes by clicking its title.
# `###` and smaller headings stay inside it; a `#` heading ends it and stays as it is.
# `collapsible: closed` starts the blocks closed.
#
# The Markdown itself does not change, so the file still reads normally in Obsidian.

module CollapsibleSections
  HEADING = %r{<h([1-6])(\s[^>]*)?>.*?</h\1>}m

  def self.wrap(html, open)
    out = +""
    inside = false
    rest = html
    while (m = rest.match(HEADING))
      level = m[1].to_i
      out << m.pre_match
      if level == 2
        out << "</details>\n" if inside
        out << %(<details class="md-section"#{open ? " open" : ""}><summary>#{m[0]}</summary>\n)
        inside = true
      elsif level == 1
        out << "</details>\n" if inside
        out << m[0]
        inside = false
      else
        out << m[0]
      end
      rest = m.post_match
    end
    out << rest
    out << "</details>\n" if inside
    out
  end
end

Jekyll::Hooks.register [:pages, :documents], :post_convert do |doc|
  setting = doc.data["collapsible"]
  next unless setting
  next unless doc.respond_to?(:extname) && %w[.md .markdown].include?(doc.extname)
  doc.content = CollapsibleSections.wrap(doc.content, setting.to_s != "closed")
end
