
## Contributor Code of Conduct

As contributors and maintainers of this project, and in the interest of fostering an open and welcoming community, we pledge to respect all people who contribute through reporting issues, posting feature requests, updating documentation, submitting pull requests or patches, and other activities.

We are committed to making participation in this project a harassment-free experience for everyone, regardless of level of experience, gender, gender identity and expression, sexual orientation, disability, personal appearance, body size, race, ethnicity, age, religion, or nationality.

Examples of unacceptable behavior by participants include:

* The use of sexualized language or imagery
* Personal attacks
* Trolling or insulting/derogatory comments
* Public or private harassment
* Publishing other's private information, such as physical or electronic addresses, without explicit permission
* Other unethical or unprofessional conduct.

Project maintainers have the right and responsibility to remove, edit, or reject comments, commits, code, wiki edits, issues, and other contributions that are not aligned to this Code of Conduct. By adopting this Code of Conduct, project maintainers commit themselves to fairly and consistently applying these principles to every aspect of managing this project. Project maintainers who do not follow or enforce the Code of Conduct may be permanently removed from the project team.

This code of conduct applies both within project spaces and in public spaces when an individual is representing the project or its community.

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by opening an issue or contacting one or more of the project maintainers.

This Code of Conduct is adapted from the [Contributor Covenant](http://contributor-covenant.org), version 1.2.0, available at [http://contributor-covenant.org/version/1/2/0/](http://contributor-covenant.org/version/1/2/0/)

---

# Opening Issues

## Bug Reports

**Required Materials:**

* Symbolicated Crash Report(s) 
* Example project that reproduces the issue

To properly address the bug I need as much contextual information about how to reproduce it as possible. This means crash report logs and example code that will reproduce the same issue are necessary for me to make progress with your report. 

NOTE: when creating the sample project that reproduces the issue it must be entirely self-contained. Please check-out any submodules or other dependencies and include them with the sample. To be able to take action on any particular problem I expect that when I download the sample I can open it in Xcode and hit "build". Thanks!

---

# Submitting Pull Requests
Pull requests are very welcome to this project, however I have a couple of guidelines that should be followed when submitting a pull request.

## Code Styling
Please use clang-format before performing any pull requests. Use the .clang-format file in this repo.


## Branching
Please make branch names `develop/brief-description` and include a full description of what the fixes and features are included. All commits should be run through the clang-format first, not following opening the PR. 