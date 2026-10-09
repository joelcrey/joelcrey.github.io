# Lets Markdown files use Obsidian-style math:
#   $x$      inline math
#   $$x$$    displayed math, even in the middle of a line
#   \$       a literal dollar sign
#
# kramdown (Jekyll's Markdown engine) only knows $$...$$, and decides inline vs
# display by whether it sits alone in a paragraph. This hook rewrites the source
# into that form before rendering. Code spans and fenced code blocks are skipped.
module ObsidianMath
  CODE = /(^```.*?^```|^~~~.*?^~~~|`[^`\n]*`)/m
  MATH = /\\\$|\$\$(.+?)\$\$|\$([^\s$](?:[^$\n]*?[^\s$\\])?)\$/m

  def self.convert(text)
    text.split(CODE).each_with_index.map { |chunk, i| i.odd? ? chunk : convert_math(chunk) }.join
  end

  def self.convert_math(text)
    text.gsub(MATH) do
      if Regexp.last_match(1)
        "\n\n$$#{raw(Regexp.last_match(1).strip)}$$\n\n"
      elsif Regexp.last_match(2)
        "$$#{raw(Regexp.last_match(2))}$$"
      else
        Regexp.last_match(0)
      end
    end
  end

  # Keep TeX like x^{{2}} from being read as Liquid.
  def self.raw(tex)
    tex.match?(/\{\{|\{%/) ? "{% raw %}#{tex}{% endraw %}" : tex
  end
end

Jekyll::Hooks.register [:pages, :documents], :pre_render do |doc|
  next unless %w[.md .markdown].include?(File.extname(doc.path).downcase)

  doc.content = ObsidianMath.convert(doc.content)
end
