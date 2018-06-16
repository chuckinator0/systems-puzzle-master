# Chuck's Solution for DevOps Puzzle

## A Golden Narrative

As an educator, I know the power of narrative to put learning into perspective. Constructing a narrative about an idea after the fact can be helpful for synthesizing the experience and shaping future learning. I think recording and paying attention to narrative can play a role in DevOps for teams of engineers to think about their thinking. I'll offer a narrative through the ideas of this puzzle that represents the thoughts of someone who thinks clearly and efficiently from the beginning.

The overall strucutre of the app is:

    [web browser on host machine]--port 8080--[nginx]--port 80--[flaskapp]--port 5432--[postgres]-[database volume]
The brackets represent containers or pieces of the system that communicate with one another. The dashes represent the connections between the containers. The first issue that arises is that we are unable to connect to the app via `http://localhost:8080`. One reason for this might be that the ports aren't set correctly, meaning there is a breakdown in communication between the containers somewhere. Combing through the code, we find that the ports aren't set correctly. Perhaps someone was testing with different ports and then didn't change it back. We might want to set a testing protocol so that this doesn't happen in the future. In `flaskapp.conf`, we need to set the port to `80` and we need to add `port=80` in the argument of `app.run` in `app.py`. Also note that in `docker-compose.yml`, the nginx port command was originally `80:8080`, which means to connect the internal `port 8080` to the host machine's `port 80`, but this is backwards. We want to connect the internal `port 80` to the host machine's `port 8080`, so we need to change `80:8080` to `8080:80` in the docker-compose file. Now, the ports should be correctly set between the containers, so we should be able to connect to localhost. Rebuilding the system in docker and running with the instructions given from the developer, sure enough, we are able to get to the main etsy-esque site.

The second issue is that upon pressing `Enter`, instead of the contents of the database being printed, only empty list items separated by commas are printed. This could mean that the database is filled with empty entries or the app isn't correctly displaying the database entries. Going over `app.py`, `database.py`, and `models.py` with a fine tooth comb alongside flask and sqlalchemy documentation and blog posts, we find that in `models.py`, the class `Items()` is supposed to have
    
    def __init__(self,name,quantity,description,date_added):
and

    def __repr__(self):
statements. The `__init__` statement initializes the class attributes so that they can be referenced in `app.py` to add user inputs to the database, and the `__repr__` statement tells flask how to represent data entries when queried. This enables the code in `app.py` to properly display the contents of the database upon successful submission.

## The Actual Process

Hindsight is 2020 (8080?). I made a lot of mistakes and went down a few wrong turns before figuring out how to make the app work. First, I spent entirely too long figuring out how docker works. I didn't realize at first that all the containers needed to be run together with `docker-compose up`, so I spent some time chasing errors that were only an issue because the containers weren't communicating. I also didn't realize at first that for codebase changes to take effect, I had to rebuiuld the image.

Next, I created a 504 error for myself. After I figured out how to set the ports correctly for nginx and flaskapp, I went too far and also changed the port between flaskapp and postgres. This ensured that flaskapp couldn't communicate with the database, causing a 504 error. In this process, I learned more about exposing and listening to ports in `.conf` files. I was able to determine that the miscommunication was between flaskapp and postgres by commenting out all references to the database and just returning `'Hello World'` upon successful submission of the form. This worked without 504 error, which helped me take my focus off of `app.py` and towards looking at the ports between the containers. I then looked more deeply into how the docker-compose file orchestrated communication between the different containers via ports.

Then, I combed flask and sqlalchemy documentation and blog posts to understand how each part of `database.py`, `app.py`, `models.py`, `forms.py` interact with each other. I had been ignoring the `__init__` and `__repr__` calls in the documentation because I thought they didn't pertain to my situation, but after reading a more detailed blog post that outlined the purpose of those calls, I realized that the `Items()` class needed to be initialized and needed a representation for queries.

There are many other small tweaks along the way that I left as comments in the code itself, and I can speak to those in more detail.

## Big Takeaways

One big takeaway is the importance of documention. It is important to have examples of "minimally viable code" and then understand how the app in question builds upon a minimally viable framework. Not only that, but when I have very little experience with a technology, it is important to find explanations of what specific functions do and what they look like in context. Some documentation is technically correct, but fails to give context or illustrative examples. Moreover, internal documentation is important. As part of an engineering team, it is essential to develop protocols for documenting a codebase in a clear, comprehensible way. Not only does this help others understand how a specific codebase works, but it's also illuminating for developers themselves to explain an idea "out loud". My teaching experience tells me that nothing clarifies one's thinking quite like preparing to explain an idea simply. This undoubtedly leads to a more structurally sound, more comprehensible codebase that is more conducive to collaborative feedback.

Another big takeaway is that I personally struggle when I don't have a colleague to bounce ideas around with. In many of the places where I wasted a lot of time poring over documentation, I could have been much more efficient with a short discussion with the developer or another colleague. An important part of working with a team of developers is to establish effective norms to balance collaborative against individual problem solving.

# Insight DevOps Engineering Systems Puzzle

## Table of Contents
1. [Understanding the puzzle](README.md#understanding-the-puzzle)
2. [Introduction](README.md#introduction)
3. [Puzzle details](README.md#puzzle-details)
4. [Instructions to submit your solution](README.md#instructions-to-submit-your-solution)
5. [FAQ](README.md#faq)

# Understanding the puzzle

We highly recommend that you take a few dedicated minutes to read this README in its entirety before starting to think about potential solutions. You'll probably find it useful to review the codebase and understand the system at a high-level before attempting to find specific bugs.

# Introduction

Imagine you're on an engineering team that is building an eCommerce site where users can buy and sell items (similar to Etsy or eBay). One of the developers on your team has put together a very simple prototype for a system that writes and reads to a database. The developer is using Postgres for the backend database, the Python Flask framework as an application server, and nginx as a web server. All of this is developed with the Docker Engine, and put together with Docker Compose.

Unfortunately, the developer is new to many of these tools, and is having a number of issues. The developer needs your help debugging the system and getting it to work properly.

# Puzzle details

The codebase included in this repo is nearly functional, but has a few bugs that are preventing it from working properly. The goal of this puzzle is to find these bugs and fix them. To do this, you'll have to familiarize yourself with the various technologies (Docker, nginx, Flask, and Postgres) enough to figure out  You definitely don't have to be an expert on these, but you should know them well enough to understand what the problem is.

Assuming you have the Docker Engine and Docker Compose already installed, the developer said that the steps for running the system is to open a terminal, `cd` into this repo, and then enter these two commands:

    docker-compose up -d db
    docker-compose run --rm flaskapp /bin/bash -c "cd /opt/services/flaskapp/src && python -c  'import database; database.init_db()'"

This "bootstraps" the PostgreSQL database with the correct tables. After that you can run the whole system with:

    docker-compose up -d

At that point, the web application should be visible by going to `localhost:8080` in a web browser. 

Once you've corrected the bugs and have the basic features working, commit the functional codebase to a new repo following the instructions below. As you debug the system, you should keep track of your thought process and what steps you took to solve the puzzle.

## Instructions to submit your solution
* Don't schedule your interview until you've worked on the puzzle 
* To submit your entry please use the link you received in your systems puzzle invitation
* You will only be able to submit through the link one time
* For security, we will not open solutions submitted via files
* Use the submission box to enter the link to your GitHub repo or Bitbucket ONLY
* Link to the specific repo for this project, not your general profile
* Put any comments in the README inside your project repo

# FAQ

Here are some common questions we've received. If you have additional questions, please email us at `devops@insightdata.com` and we'll answer your questions as quickly as we can (during PST business hours), and update this FAQ. Again, only contact us after you have read through the Readme and FAQ one more time and cannot find the answer to your question.

### Which Github link should I submit?
You should submit the URL for the top-level root of your repository. For example, this repo would be submitted by copying the URL `https://github.com/InsightDataScience/systems-puzzle` into the appropriate field on the application. **Do NOT try to submit your coding puzzle using a pull request**, which would make your source code publicly available.

### Do I need a private Github repo?
No, you may use a public repo, there is no need to purchase a private repo. You may also submit a link to a Bitbucket repo if you prefer.

### What sort of system should I use to run my program (Windows, Linux, Mac)?
You should use Docker to run and test your solution, which should work on any operating system. If you're unfamiliar with Docker, we recommend attending one of our Online Tech Talks on Docker, which you should've received information about in your invitation. Alternatively, there are ample free resources available on docker.com.

### How will my solution be evaluated?
While we will review your submission briefly before your interview, the main point of this puzzle is to serve as content for discussion during the interview. In the interview, we'll evaluate your problem solving and debugging skills based off how you solved this puzzle, so be sure to document your thought process.

### This eCommerce site is ugly...should I improve the design?  
No, you should focus on the functionality. Your engineering team will bring on a designer and front-end developer later in the process, so don't worry about that aspect in this puzzle. If you have extra time, it would be far better to focus on aspects that make the code cleaner and easier to use, like tests and refactoring.

### Should I use orchestration tools like Kubernetes?
While technologies like Kubernetes are quite powerful, they're likely overkill for the simple application in this puzzle. We recommend that you stick to Docker Compose for this puzzle.

