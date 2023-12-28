# Problems to Solve Before Starting Implementation

Before our project comes to life, we need to think about how to divide tasks.
This will be an important factor for smooth collaboration as we have several
tasks that may take us more time. Examples of such tasks include coding for
server communication or front-end development. None of the team members have
extensive experience in these areas, so we will assume that it will take us a
lot of time.

Another problem is the selection of languages/environments/tools on which we
will base our program. Due to the wide range of functionalities, we will need to
use multiple technologies. Communication between different segments may be a
challenge, so before starting implementation, we need to carefully consider what
we want to use. We are inclined towards popular solutions as they often have
ready-made plugins/frameworks that allow communication with other technologies
and have extensive support.

# Description of Constraints

The most important constraint imposed is the time constraint. We need to deliver
specific parts of the program within the designated time, so we cannot afford
delays at any stage of the project (fortunately, we have contingency plans that
can help us stay within the time frame).

A directly limiting factor for the application is that the server will not be
running all the time - it will only be launched during testing. This means that
experts will not have access to historical ranking results. It is an
inconvenience that we need to consider, but it should not hinder the final
testing during the laboratories.

# Project Methodology

Considering the project structure and constraints (mainly time), we will adopt
the waterfall methodology. With detailed guidelines regarding specific aspects
of the project, we can develop a precise action plan from the beginning. We
acknowledge that we will deliver a functional version of the application quite
late, but we do not see any other options, so we will stick to this methodology.

# General Description of Architectural Assumptions

## Main Plan

The application will consist of several components (database, expert web
application, admin web application, ranking results generation program) that
will require different programming tools. One of them is FastAPI - a framework
that allows the creation of RESTful API interfaces in Python. We will use SQLite
to implement the database. To limit the number of programming languages, the
ranking results calculation program will also be implemented in Python (using
the Numpy library for faster computations). The front-end of the web
applications will be implemented in Rust using WebAssembly technology.

An element of the project that is not imposed in advance is the method of
sharing rankings with experts. Our idea for solving this issue is to send tokens
- an expert who receives a specific token will be able to participate in the
ranking and view its results. The token can be shared, for example, via email.

## Contingency Plan

If the implementation of the database connection using the FastAPI framework
fails, we plan to use Django, which is the most popular solution for working
with databases in Python.

If we fail to implement the system for sending tokens to experts, we plan to
allow experts to authenticate themselves via email. After logging in, experts
will see a list of rankings available to them in which they can participate.

# Detailed Description of Architecture

**Link to the code repository:**
<https://github.com/funsafe-math/ranking_project>

## DATABASE

The database diagram is presented in Figure [1](#fig:database). By implementing
it in this way, we will be able to store historical ranking data. Individual
tables will be implemented in Python with the help of the Pydantic library.


![[]{#fig:database label="fig:database"}Database Schema
](Pictures/10000201000003640000032FB1B8D35E8021B7E0.png){#fig:database
width="90%"}

## SERVER (ADMIN)

The admin will manage the server, in which the database will be implemented (along with functions for its management). This means that the expert application and the ranking calculation program will need to communicate with the admin to obtain information about the rankings. Despite the fact that the server logic and the database will share some code files, they will have separate functions and will inherit from different classes, thus maintaining the overall architectural scheme (see Figure [2](#fig:architecture)).

![[]{#fig:architecture label="fig:architecture"}High level architecture
plan (DB and Admin colaboration)](Pictures/10000201000002710000017D1497C621F04447B6.png){#fig:architecture
width="70%"}

## CLIENT (EXPERT)

The client application will be based on similar assumptions to the admin application - its front-end and back-end will be implemented using the same languages and libraries. This will enable seamless communication between the admin and the expert.

## FRONT-END

Ultimately, our program should be accessible to clients and admins from mobile devices, so we will implement the front-end of the web applications in Rust. The frontend project for the web applications (two expert views and one admin view) is visible in Figure [3](#fig:gui). In the final version, the admin will also have an appropriate view to share the ranking with experts, but this view will need to be adapted to the sharing strategy we will ultimately implement.

![[]{#fig:gui label="fig:gui"}GUI concept](Pictures/10000201000004180000018B4A3831CB6AABDC44.png){#fig:gui
width="90%"}

# Glossary of Terms

- Alternative: Possibility, choice among different options
- Criterion: A characteristic by which comparison of alternatives is made
- Expert: A person with knowledge and experience in a particular field, evaluating rankings
- Evaluation: An expert's opinion on the comparison of alternatives in the context of a specific criterion
- Ranking: A set of alternatives evaluated in a specific context