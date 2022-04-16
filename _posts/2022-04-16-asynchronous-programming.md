---
title:  "Asynchronous Programming: Three Easy Pieces and Three Hard Pieces"
author: Howard Lau
excerpt_separator: <!--more-->
---

Asynchronous programming (aka. event-driven programming) allows us to handle a large number of concurrent tasks with low overhead and a small number of threads. For those who have not yet got used to this programming paradigm, asynchronous programming may be something magical and horrifying. In fact, it is just all about three easy pieces. Yet what makes it really difficult are another three hard pieces. 

<!--more-->

## Three Easy Pieces

### States

You may have learned socket programming, where you treat TCP connections like files and just use sychrounous API to read (receive) or write (send) data. When the connection is still open and the peer hasn't sent any data yet, your program will "hang" on the read call until some bytes are available. Although this seems like sychronous programming, it is the OS that actually masquerades all the asynchrony. 

What happens when your program "hangs"? The OS will check the receive buffer of the connection, find it empty, save the **states** of the program and pause it to save power. Obviously, the OS needs some way to wake up the program when the connection is ready to receive more data. The program will be put in the **wait queue** of the socket. When bytes arrive, the OS will process the network packets and wake up processes in the wait queue. In other words, the OS **calls back** the program. The program will then resume itself from where it left off. 

This works well at first when you don't have too many connections to deal with. However, when you have a lot of connections, say ten thousands, this will be intolerably inefficient and slow. Context switching is a time-consuming process. The CPU has to switch back and forth between kernel mode and user mode via interrupts. Even worse, every time a different process is scheduled, the TLB cache is flushed, causing a huge performance penalty.

So why not just let the asychrony surfaces back to the user mode program? After all, we can save and recover the states ourselves. But what does "states" mean? You may have already learned that the OS actually saves the registers to the memory and protects the private process memory (especially call stack) by switching page tables. States are just that simple. The programs needs only to remember the progress it has made.

Naturally, you may think that we can save registers and the call stack to somewhere, and jumps to some other function to do some other work. That's exactly how a **stackful coroutine** works. On Linux, you can use `ucontext` to do context switching in user space. 

Wait, what is a coroutine? Well, a coroutine means a **cooperative** routine. In fact, you can treat it as a routine that remembers something itself and can be suspended and resumed.

For illustration, a coroutine can be as simple as follows:

```c
int counter() {
    static int i = 0;
    return i++;
}
```

When you call it the first time, it just returns 0. However, the variable `i` is not destroyed because it is a static variable. So the function is more like a `for`-loop incrementing a counter. When the function returns, it is suspended. The next time you call it, the function is resumed and the counter is incremented by one. Afterwards, the function is suspended again, returning the control flow to the caller. 

In this example, the state is actually a mere integer. But in real life, the state can be anything. For example, it can be a pointer to a structure that contains more complicated data.

So why bother saving a lot of registers when saving only a integer is enough? That's how a **stackless coroutine** works. It just saves the states it needs, and nothing more than that. It just looks like a **state machine**, which reads from the states and decides what to do next depending on the input and the current state. 

In real world, the state machine is usually constructed by the compiler for you. For instance, Javascript lets you mark a function as a coroutine by using the keyword `async` and seperate states using the keyword `await`. Many other languages have similar keywords.

This is the first easy piece of asynchronous programming. Just remember three keywords: **state**, **stackful coroutine**, **stackless coroutine**.

### Callback

In real world, coroutines do not suspend for no reasons. They suspend because they have no more work to do and have to wait for some external events. For example, as mentioned in the synchronous programming case, a coroutine may have to wait for a network packet to arrive. Before it suspends, it tells somebody it is interested in network events and pass a **callback** that is invoked when the specific event happens. When the callback is invoked, the coroutine just picks up the states it saved and continues its work. This can also be regarded as a **continuation point**.

This is the second easy piece of asynchronous programming. Just remember three keywords: **callback**, **event**, **continuation**.

But who's that somebody? 

### Scheduler

The scheduler is the one who takes care of which coroutine is interested in what event. In fact, it is just a loop, constantly asking the OS whether any events have happened. If so, it just finds the relevant coroutine and use **callback** it saves earlier to resume it. Usually, the scheduler is implemented as a **event loop**.

A event loop is as simple as follows:

```
for ever {
    events = get_events();
    for each event in events {
        coroutine = find_coroutine(event);
        resume(coroutine);
    }
}
```

The event loop is usually shared by all coroutines so that they can register or unregister interested event.

That's the last easy piece of asynchronous programming. Just remember two keywords: **scheduler**, **event loop**.

## Three Hard Pieces

### Lifetime

Things get harder if a coroutine needs to use something external. For example, it may need to use an array to store some results. The array may not be destroyed until the coroutine no longer require access to it. Therefore, you must be careful to make sure every object created outside the coroutine outlive it. Otherwise, invalid memory accesses may happend and crash your program.

Languages with GC make things a lot easier because the runtime does all the dirty work for you. But it is really painful to use coroutine in languages without GC such as C, C++ and Rust.

Fortunately, the Rust compiler checks all the life time for you and warns you when you do it wrong. Unfortuantely, if you plan to write asychronous programs in C++, you must be really careful not to mess things up.

### Synchronization

Synchronization is a nightmare when writing multi-threaded programs. Asychronous programming makes it even trickier. For example, the OS may want a mutex to be unlocked by the same thread which locks it. But there can be multiple schedulers running on different threads, so coroutines may migrate among several threads. If you intend to hold a mutex lock across `await`, you would absolutely need something like a `AsyncMutex` so that the scheduler can properly unlock the mutex.

### Cancellation

Assume that you are writing a server programming serving web pages. An impatient user may click the "cancel" button before a time-consuming database operation finishes or an unlucky user is accidentally disconnected, rendering the result useless. In this case, we had better cancel the database operation to save server resources.

However, implementing cancellation is way more difficult as it requires you to keep track of EVERYTHING involved in a request and invoke extra functions to cancel them when a cancel request is received. For example, you may need to cancel the database operation, the network connection, the disk I/O, the file I/O, the memory allocation, etc. You need a way to **propagate** the cancel signal along the call chain. If you forget to release some resources or some coroutines miss the signal, you will waste time or money doing useless operations. 

There are some common ways of implementing cancellation, one of which is the `select` paradigm. By using `select`, the coroutine not only waits for the event it is interested in, but also the cancel signal. Whichever comes first, the coroutine will be resumed to handle that event.