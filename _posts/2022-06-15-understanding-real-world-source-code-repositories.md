---
title:  "Understanding Real World Source Code Repositories"
author: Howard Lau
excerpt_separator: <!--more-->
---

It sounds like a haunting task understanding real-world large-scale source code repositories for less-experienced junior programmers. If you are the junior ones and attempting to figure out a large project, you are likely to get lost in the intertwined code labyrinth. Therefore, we have to rely on some guidance to find a way out. Here are what I learnt after reading hundreds of such projects.

<!--more-->

## Read the Docs
First of all, you have to at least read through the README of a project, or the main wiki page. In this stage, you need to get familiar with what kind of this software is, what is it for and on what platforms this software runs. 

## Run the Code
The next step is to get the code running. This means you have to set up the development environment properly, compile the code successfully and finally spawn the process. You should install build and run dependencies, and build tools. Although it sounds quite easy, this is the most tedious and error-prone process. You must be careful of dealing with different versions of dependencies and compilers. Sometimes they conflict with system-wide installations so you have to make a local installation. Large projects are very picky about versions, not even a minor difference tolerated. 

This process aims to ensure that all compile-time generated files are properly written so that the editor or IDE can provides normal code browsing functionalities like jumping to definition. What's more, this ensures that you can use your favourite debugger to step run the code later on. Some code can only be run on specific hardware platforms. If you encounter such code and you don't have the corresponding hardware, you are unlucky and can only read the code with your eyes.

Usually, server-side programs are the easiest, which just requires you to write some configurations and you are ready to go. Client-side programs are a little more complex because they are usually paired with server-side programs that need to be run at first. But if it is a command line tool or a GUI application, chances are that they don't need a server. Libraries are somehow troublesome to run because no executables are compiled. Therefore, you should look for something like examples directory in the project, which will be compiled to executables so that you can run them. Moreover, developers usually write extensive automatic test cases during library development, so you can try to run these test code as well.

## Find the Goal
When things have been settled down, ask yourself which part of the project you are interested in. Source code is not a book, you can't pick it up and just start reading from the first page. It's almost infeasible for any programmer to understand all of a large project at the beginning. 

There must be some kind of goal limiting your scope. For instance, if you are curious about the implementation of a feature, then you just need to focus on that feature. If you are fixing a bug, you may focus on reproduction of the issue. Even though you may have no goal at the moment, it's always better to start from a specific point.

## Study the Interfaces
A well-structured software often define concise abstractions of their functionalities clearly in the form of interfaces, which are a good starting point. Interfaces are usually function declarations, so you can focus on which feature relates to which set of interfaces.

In this step, you should find out on which interfaces you should focus on and where they are called. This gives you a rough insight of the framework of the feature. 

## Set the Breakpoints
Code is written for running, not for reading. It is much easier to comprehend the code when it is running. Therefore, before you start looking into implementations, make sure you have set breakpoints on functions of your interest. If you are just experimenting with the code, just set the breakpoint at entry function such as `main`. Then, just run the program and wait until breakpoints are triggered. In this way, any runtime-specific arguments or derived classes are determined. Otherwise, you may have difficulties finding which class is the one the function calls.

When you stop at the breakpoints, you can at first look at the call stack, the path along which your interested functions are called. Oftentimes, the precedented functions prepares proper contexts and arguments for the function that does the real work. You can trace back along the call stack to see if there is any important functions that are related to the feature. What's more, if you find the program stopped at such intermediate functions, you can make use of step run and step in functionalities provided by debuggers to pinpoint the real function.

For libraries, the same principle applies. The only difference is that you should debug examples or tests.

## Take-home Message
Large projects are composed with numerous related but relatively independent small pieces of programs. The principle is that you should comprehend it in a progressive way, from abstract to concrete and from specific to general. And remember that a running program is much easier 
to understand than static pieces of code.