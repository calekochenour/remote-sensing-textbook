# Set phony targets
.PHONY: all push-main clean-book build-book publish-book

# Set Jupyter Book folder
jupyter_book = content/

# Set commit message
github_commit_message = "Add bibliography"

# Clean, build, and publish book to GitHub Pages; push all files to main
all: publish-book push-main

# Clean contents of the book
clean-book:
	jupyter-book clean $(jupyter_book)

# Build book
build-book: clean-book
	jupyter-book build $(jupyter_book)

# Publish book build to GitHub Pages branch
publish-book: build-book
	ghp-import -n -p -f -m $(github_commit_message) $(jupyter_book)_build/html

# Push all content/ files to main branch
push-main:
	git add $(jupyter_book)
	git commit -m $(github_commit_message)
	git push origin master
