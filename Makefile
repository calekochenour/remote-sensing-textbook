# Set phony targets
.PHONY: all push-content-notebooks clean-book build-book push-book

# Set commit messages
gh_main_commit_message = "Add workflow for [WORKFLOW NAME]"
gh_pages_commit_message = "Add workflow for [WORKFLOW NAME]"

# Clean, build, and push book, and push all files
all: push-content-notebooks push-book

# Clean contents of the book
clean-book:
	jupyter-book clean content/

# Build book
build-book: clean-book
	jupyter-book build content/

# Push book build to GitHub Pages branch
push-book: build-book
	ghp-import -n -p -f -m $(gh_pages_commit_message) content/_build/html

# Push all content/ and notebook/ files to main branch
push-content-notebooks:
	git add content/ notebooks/
	git commit -m $(gh_main_commit_message)
	git push origin master
