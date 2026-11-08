# Lets Markdown files use Obsidian-style internal links:
#   [[note]]                 link to the post or page whose file is note.md, shown by its title
#   [[note|text]]            the same, shown as "text"
#   [[note#Heading]]         link to a heading of that note ([[#Heading]] for this note)
#   ![[picture.png]]         an image anywhere in the site (![[picture.png|300]]: 300 pixels wide)
#   [text](note.md)          Obsidian's Markdown-style links to notes work too
#
# Notes are found by file name (with or without the date of a post, or with a folder path).
# A link to a note that is not on the site (an unpublished draft, say) is shown as plain text.
# Math ($...$, so k[[x]] is safe) and code are left alone.
require "cgi"

module ObsidianLinks
  CODE = /^```.*?^```|^~~~.*?^~~~|`[^`\n]*`/m
  MATH = /\\\$|\$\$.+?\$\$|\$[^\s$](?:[^$\n]*?[^\s$\\])?\$/m
  WIKI = /(!?)\[\[([^\[\]\n|#^]*)(?:#([^\[\]\n|]*))?(?:\|([^\[\]\n]*))?\]\]/
  MDLINK = /(?<!!)\[([^\[\]\n]*)\]\((?!https?:|mailto:)([^()\s]+?\.md)(#[^()\s]*)?\)/
  # Whichever starts first wins, so $k[[x]]$ stays math and [[note#Heading with $x$]] is a link
  TOKEN = /(?<code>#{CODE})|(?<wiki>#{WIKI})|(?<md>#{MDLINK})|(?<math>#{MATH})/m

  class << self
    attr_accessor :notes, :files, :baseurl

    def index(site)
      self.baseurl = site.config["baseurl"].to_s
      self.notes = {}
      docs = site.collections.values.flat_map(&:docs) + site.pages
      docs.each do |doc|
        next unless doc.respond_to?(:path) && %w[.md .markdown].include?(File.extname(doc.path).downcase)
        rel = doc.relative_path.sub(/\.(md|markdown)\z/i, "")
        name = File.basename(rel)
        [rel, rel.sub(%r{\A_[^/]+/}, ""), name, name.sub(/\A\d{4}-\d{2}-\d{2}-/, "")].each do |key|
          notes[key.downcase] ||= doc
        end
      end
      self.files = {}
      site.static_files.each do |f|
        files[f.relative_path.sub(%r{\A/}, "").downcase] ||= f
        files[File.basename(f.relative_path).downcase] ||= f
      end
    end

    def convert(text, doc)
      text.gsub(TOKEN) do
        m = Regexp.last_match
        if m[:wiki]
          w = m[:wiki].match(WIKI)
          embed, target, heading, label = w[1], w[2].strip, w[3]&.strip, w[4]&.strip
          embed == "!" && image?(target) ? image(target, label) : link(target, heading, label, doc)
        elsif m[:md]
          l = m[:md].match(MDLINK)
          note = find(CGI.unescape(l[2]).sub(/\.md\z/i, ""))
          heading = l[3] && CGI.unescape(l[3].delete_prefix("#"))
          note ? "[#{l[1]}](#{url(note, heading)})" : m[0]
        else
          m[0]
        end
      end
    end

    def link(target, heading, label, doc)
      note = target.empty? ? doc : find(target)
      # Without |text, show the title of the note (not its file name), and the heading if any
      name = target.empty? ? nil : (note && note.data["title"]) || target
      text = label || [name, heading].reject { |s| s.nil? || s.empty? }.join(" › ")
      return escape(text) unless note
      "[#{escape(text)}](#{url(note, heading)})"
    end

    def find(target)
      key = target.sub(%r{\A\.?/}, "").downcase
      notes[key] || notes[File.basename(key)]
    end

    def url(note, heading)
      base = note.url.end_with?(".html") || note.url.end_with?("/") ? note.url : "#{note.url}.html"
      anchor = heading && !heading.empty? ? "##{slug(heading)}" : ""
      "#{baseurl}#{base}#{anchor}"
    end

    # The id kramdown (GFM input) gives a heading
    def slug(heading)
      heading.strip.downcase.gsub(/[^\p{Word}\- ]/u, "").tr(" ", "-")
    end

    def image?(target)
      target.match?(/\.(png|jpe?g|gif|svg|webp)\z/i)
    end

    def image(target, label)
      f = files[target.downcase] || files[File.basename(target).downcase]
      return escape(target) unless f
      src = "#{baseurl}#{f.relative_path.sub(%r{\A/?}, '/')}"
      # ![[picture.png|300]] or ![[picture.png|300x200]] sets the size, as in Obsidian
      if (size = label.to_s.match(/\A(\d+)(?:x(\d+))?\z/))
        attrs = %( width="#{size[1]}") + (size[2] ? %( height="#{size[2]}") : "")
        return "![](#{src}){:#{attrs}}"
      end
      "![#{escape(label.to_s)}](#{src})"
    end

    # Escape Markdown in link text, but not inside its math
    def escape(text)
      text.split(/(#{MATH})/m).each_with_index.map do |part, i|
        i.odd? ? part : part.gsub(/([\[\]*_])/) { "\\#{$1}" }
      end.join
    end
  end
end

Jekyll::Hooks.register :site, :pre_render do |site|
  ObsidianLinks.index(site)
end

Jekyll::Hooks.register [:pages, :documents], :pre_render, priority: :high do |doc|
  next unless %w[.md .markdown].include?(File.extname(doc.path).downcase)

  doc.content = ObsidianLinks.convert(doc.content, doc)
end
