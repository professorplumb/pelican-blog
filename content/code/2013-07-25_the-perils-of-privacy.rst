The Perils of Privacy
#####################

:status: draft
:tags: github, community
:category: code
:summary: On why having too many private GitHub repositories can be self-defeating

One of the best aspects of the technology world is that it is closer to a pure meritocracy than almost any other
industry. [1]_  This is not, of course, to say that there aren't any `gender
<http://www.theatlantic.com/technology/archive/2013/01/a-simple-suggestion-to-help-phase-out-all-male-panels-at-tech-conferences/266837/>`_
or `race <http://www.newstatesman.com/sci-tech/2012/11/tech-has-white-dude-problem-and-it-doesnt-get-better-not-talking-about-it>`_
problems in IT: we clearly have a long way to go in those regards.

However, we do get at least one thing right.  More important than your networking skills, or how much money you have,
or where you went to school, is this: what have you **done**?  You can call yourself a rock star all day long, and drop
the names you got cards from at SXSW, but if your portfolio doesn't measure up you'll be forgotten faster than `the Back
to the Future animated series <http://www.youtube.com/watch?feature=player_embedded&v=t6sGq3tN8nA>`_.  Instead of "it's
not what you know, it's who you know," it's "By their code shall ye know them." [2]_ [3]_

Show Me The Objective-C
=======================

But how is a prospective employer, investor, or other evaluator to know just how hotshot you really are?  Whether that
single-page app on your resume was really written by you, or whether your claimed expertise in `Brainfuck
<http://www.muppetlabs.com/~breadbox/bf/>`_ is justified?  This is where modern public repository systems like `GitHub
<https://github.com>`_ and `Bitbucket <https://bitbucket.com>`_ really shine.  Anyone looking at code under your account
knows that you wrote it, or at least that it was uploaded using your private key.

But what if you don't have a Github profile?  Or what if you **do** but all your repositories are
private?  This is in fact exactly the situation I've been in for the past few years.  Take a look at my public Github
commit history as of today (July 25, 2013):

.. image:: |filename|../images/github-public.png

That one commit (of a `documentation patch <https://github.com/toastdriven/django-tastypie/pull/984>`_ for `django-tastypie
<https://github.com/toastdriven/django-tastypie>`_) looks mighty lonely there, doesn't it?

And now my private commit history (visible to me and members of my organization):

.. image:: |filename|../images/github-private.png

That's a lot of activity on a lot of private repositories.  I'm pretty proud of much of the code I've written (and, in
true perfectionist style, ambivalent about or downright disgusted with much of the rest.)  However, if you're an employer
looking for a gauge of my ability, or even just someone who followed the Github link from this blog to see if I know what
I'm talking about, you're not going to have any idea of that from the single public commit, a one-line documentation fix.

Let It All Hang Out
===================

So what to do about this?  If you're in this situation, here are three obvious but necessary steps to take.

1. Make your repositories public
    If they're your own projects, think long and hard about if and why you need them to be private.  Is it for secrecy's
    sake?  Anyone who wants to steal your code likely can, especially if it's for a browser or mobile device, so this is
    no protection against malicious attackers.  Even so, the extra visibility and scrutiny you can get when your code is
    public can make up for this risk.  Likewise, developers who are just learning can learn from your code, even if they
    just copy it.

    It's more complicated if the repository you're working on doesn't belong to you.  In this case you can
    try to convince the owner (usually a company) of the benefits of open source.  It doesn't have to be all their code,
    maybe just a few repositories.  Or refactor the business logic into a private repository, and open-source the
    surrounding framework.  (I am working on this last with my company, but it's an uphill battle.)

2. Contribute to open-source projects
    I know, this seems daunting.  I personally have lots of excuses for avoiding this: I'm too busy, I don't know the
    codebase, those people are a lot smarter than me.  All of these are true!  Especially the last one - because while
    I'm sitting here making excuses, they're writing the software that I happily and thankfully use.

    There are `millions of articles <https://www.google.com/search?q=how+to+get+started+contributing+to+open+source>`_
    written on how to get started contributing to open-source projects.  My favorite idea, though I don't remember where
    I read it, was to find an open-source project with poor documentation, and go fix it.  Every developer hates writing
    documentation, and when you're elbows deep in the bowels of a project you don't have the necessary remove to look at
    your project from the point of a neophyte.  This is where you (or I) come in: as we learn the ins and outs of a
    project we can update the documentation with instructions and examples which make sense from our point of view.
    From there, it's only a short jump to writing code.

3. Commit all the things
    Remember that silly little text-adventure game you wrote back in college?  Put it on Bitbucket!  That function you
    keep including in your projects because you keep needing it but for some godforsaken reason it's not in the standard
    libraries?  Make it a `Gist <https://gist.github.com>`_!  The todo list app you wrote while learning `Backbone
    <http://backbonejs.org/>`_ or `Angular <http://angularjs.org/>`_ or `Ember <http://emberjs.com/>`_?  Who cares that
    there are `thousands of them <https://github.com/search?q=todo>`_?

Wrapping Up
===========

I fully intend to put my code where my mouth is.  Once I'm done with the `graphing calculator series
<|filename|2013-07-07_graphing-calculator-part-1.rst>`_, I will post the final product to Github.  As I work on projects
involving open-source software, I will take more time out of my day to either fix or document the bugs and warts I find.
And I will keep working to make as many of my private projects public as possible.  You can keep me honest by checking
my `GitHub profile <https://github.com/professorplumb>`_.

Thanks for reading, and as always, your comments and questions are welcome.

Footnotes
---------

.. [1] Professional sports being the obvious exception.

.. [2] And now I can check "working a Bible reference into a paragraph with a '90s Saturday morning cartoon" off my
    bucket list.

.. [3] I'm well aware that this is (unfortunately) a rather idealized vision of tech.  It applies best, however, to the
    young, hungry hacker crew which is taking startup culture by storm.  It is my belief and hope that these people are
    our future.