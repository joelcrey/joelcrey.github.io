# Collapsible sections: with `collapsible: true` in the front matter of a page or post, every
# section under a heading of the largest level used in it (# if there is one, else ## or ###) becomes
# a block that opens and closes by clicking its title; smaller headings stay inside it. `collapsible: closed` starts them closed.
#
# The Markdown itself does not change, so the file still reads normally in Obsidian.

module CollapsibleSections
  HEADING = %r{<h([1-6])(\s[^>]*)?>.*?</h\1>}m

  def self.wrap(html, open)
    levels = html.scan(HEADING).map { |level, _| level.to_i }
    return html if levels.empty?
    top = levels.min
    out = +""
    inside = false
    rest = html
    while (m = rest.match(HEADING))
      level = m[1].to_i
      out << m.pre_match
      if level <= top
        out << "</details>\n" if inside
        out << %(<details class="md-section"#{open ? " open" : ""}><summary>#{m[0]}</summary>\n)
        inside = true
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
