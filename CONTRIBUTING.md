# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit
helps.

## DCO signoff
We require you to agree to the [Developer Certificate of Origin](DCO) when submitting changes to this project.

To do this, simply ensure that all of your commits are signed-off using the git sign-off feature:

```shell
$ git commit -s -m "Making changes!"
```

## Types of Contributions
You can contribute in many ways:

### Report Bugs

Report bugs at https://github.com/Metaswitch/announcer/issues.

If you are reporting a bug, please include:

- Your operating system name and version.
- Any details about your local setup that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

### Write Documentation

announcer could always use more documentation, whether as part of the
official announcer docs, in docstrings, or even on the web in blog posts,
articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at https://github.com/Metaswitch/announcer/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.

## Get Started!

Ready to contribute? Here's how to set up `announcer` for local development.

1. Fork the `announcer` repo on GitHub.

2. Clone your fork locally::

    ```shell
    $ git clone git@github.com:your_name_here/announcer.git
    ```

3. Install your local copy into a virtualenv.

    ```shell
    $ cd announcer/
    $ python3 -m venv venv
    $ pip install uv
    $ uv pip install -e .
    ```

4. Create a branch for local development::

    ```shell
    $ git checkout -b name-of-your-bugfix-or-feature
    ```

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the
   tests using tox.

    ```shell
    $ tox
    ```

6. Commit your changes (ensuring they are signed-off) and push your branch to GitHub::

    ```shell
    $ git add .
    $ git commit -s -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature
    ```

7. Submit a pull request through the GitHub website.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.md.
3. The pull request should work for Python >=3.7.

## Tips

To run a subset of pytest tests:

```shell
$ py.test tests/test_announce.py
```
