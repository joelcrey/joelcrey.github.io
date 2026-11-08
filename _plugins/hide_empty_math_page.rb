# The Math stuff page (math.md) is only built when there is a math post to list; without one it
# would be an empty page. The menu link is hidden the same way, in _includes/header.html.
# Drafts count only when they are shown (`jekyll serve --drafts`), so the local preview still has it.

Jekyll::Hooks.register :site, :post_read do |site|
  next if site.posts.docs.any? { |post| post.data["categories"].include?("math") }

  site.pages.reject! { |page| page.relative_path == "math.md" }
end
