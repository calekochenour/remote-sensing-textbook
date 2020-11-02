# Set phony targets
.PHONY: all push-main clean-book build-book publish-book

# Set Jupyter Book folder
jupyter_book = content/

# Set commit messages
# github_main_commit_message = "Add workflow for [WORKFLOW NAME]"
# github_pages_commit_message = "Add workflow for [WORKFLOW NAME]"
github_main_commit_message = "Refine syntax"
github_pages_commit_message = "Refine syntax"

# Push all files to main; clean, build, and publish book to GitHub Pages
all: push-main publish-book

# Clean contents of the book
clean-book:
	jupyter-book clean $(jupyter_book)

# Build book
build-book: clean-book
	jupyter-book build $(jupyter_book)

# Publish book build to GitHub Pages branch
publish-book: build-book
	ghp-import -n -p -f -m $(github_pages_commit_message) $(jupyter_book)_build/html

# Push all content/ and notebook/ files to main branch
push-main:
	git add $(jupyter_book) notebooks/
	git commit -m $(github_main_commit_message)
	git push origin master
