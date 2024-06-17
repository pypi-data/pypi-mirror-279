*****
Trops
*****

.. image:: https://img.shields.io/pypi/v/trops
   :target: https://pypi.org/project/trops/
   :alt: PyPI Package

.. image:: https://img.shields.io/badge/license-MIT-brightgreen.svg
   :target: LICENSE
   :alt: Repository License

Trops is a command-line tool designed for tracking system operations on destributed Linux systems. It keeps a log of executed commands and modified files, being helpful for developing Ansible roles, Dockerfiles, and similar tasks.

It aims for solving these challenges:

- Keeping track of when and what has been done on which host (for which issue)
- Note-taking for solo system administrators of destributed systems
- "Potentially" bridging the gap between Dev and Ops

Prerequisites
=============

- OS: Linux
- Shell: Bash or Zsh
- Python: 3.8 or higher
- Git: 2.28 or higher

Installation
============

Ubuntu::

    sudo apt install python3 python3-pip git
    sudo pip3.11 install trops

Rocky::

    sudo dnf install python3.11 python3.11-pip git
    sudo pip3.11 install trops

Miniconda::

    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    chmod +x Miniconda3-latest-Linux-x86_64.sh
    ./Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda3
    $HOME//miniconda3/bin/conda install git
    $HOME/miniconda3/bin/pip install trops
    mkdir $HOME/bin
    cd $HOME/bin
    ln -s ../miniconda3/bin/git git
    ln -s ../miniconda3/bin/trops trops
    export PATH=$HOME/bin:$PATH # Add this line to your .bashrc

Quickstart
==========

Activate trops::

    export TROPS_DIR="/path/to/your/trops"
    test -d $TROPS_DIR || mkdir -p $TROPS_DIR

    # for Bash
    eval "$(trops init bash)"
    # for Zsh
    eval "$(trops init zsh)"

Create a trops environment(e.g. myenv)::

    trops env create myenv

Turn on/off background tracking::

    # Turn on
    ontrops myenv

    # Turn off
    offtrops

If you turn it on, every command will be logged, and editing a file will be commited to its git repo ($TROPS_DIR/repo/<env>.git). So try installing or compiling some application, and then type trops log command::

    # Get your work done, and then check log
    trops log

    # Or pass the output to Trops KouMyo(km), 
    # which unclutters and shows log as a table
    trops log | trops km

If you want to use Github or GitLab as a remote private repository, I think it is a good idea.
You can link your Trops' bare git repository to a remote git repository by this::

    # At creation
    trops env create --git-remote=git@github.com:username/repository_name.git myenv

    # or update
    ontrops myenv
    trops env update --git-remote=git@github.com:username/repository_name.git

Now you can make your system operation as an issue-driven project. So create an issue on your 
Github/GitLab Issue -- like "Install barfoo #1" -- and then set the issue number as a tag 
on your Trops like this::

    # '#<issue number>'
    ttags '#1'

    # repo_name#<number>
    ttags repo_name#1

Once your work is done, try this::

    # Save the log as a markdown table
    trops log | trops km --save

    # And then, push your trops' commits to the remote repository
    trops repo push

As you can see on your issue page, what you've done is linked to the issue you tagged.
And you can find the markdown table from that page.

And now, you can start working on automating what you've interactively done by using Ansible,
Salt, Chef, Puppet, or whatever tools down the line.

So, Trops helps you easily try new things, and you don't have to worry about forgetting what
you've done. And then, once you've got used to it, it will actually help you organize your 
day-to-day multitasking, which is probably something that a lot of system admins cannot avoid.

Contributing
============

If you have a problem, please `create an issue <https://github.com/kojiwell/trops/issues/new>`_ or a pull request.

1. Fork it ( https://github.com/kojiwell/trops/fork )
2. Create your feature branch (``git checkout -b my-new-feature``)
3. Commit your changes (``git commit -am 'Add some feature'``)
4. Push to the branch (``git push origin my-new-feature``)
5. Create a new Pull Request