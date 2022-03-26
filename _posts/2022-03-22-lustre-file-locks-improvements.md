---
title:  Lustre File Locks Improvements
author: Howard Lau
excerpt_separator: <!--more-->
---

Derived from VAX distributed lock manager, Lustre file system locks consist of six modes (NL, CR, CW, PR, PW, EX). The locks are organized in separate namespaces, e.g. metadata namespace and object namespace. Locks are requested when I/O operations are initiated. The locks are managed by different servers (OSS, MDS...) and are requested by clients (OSC, MDC...). However, Lustre performs poorly when multiple processes writing a single shared file in strides. 

## Problems of Normal Write Locks

The write locks are automatically expanded by server when requested. For example, client A wants to write the 0, 3, 6 MB of a file and client B wants to write the 1, 4, 7 MB of the file. Although they are writing non overlapped intervals, there still exists a lock contention problem. To illustrate, when client A requests the write lock for 0-1 MB of the file, the server grants it the lock, expanded to the whole file. Later when client B requests the write lock for 1-2 MB of the file, the server cancels the lock granted to client A and grants client B the lock, also expanded to a whole file. This causes a false conflicting problem. Even worse, disabling lock expansion does not help due to the extra round-trip time incurred for more lock requests.

<!--more-->
## Group Locking

Group locking enabled for a file requests Lustre not to acquire write locks. It is the application that is responsible for maintaining consistency of the file since the file system is no longer providing the guarantees. This also means the reads and writes on the file do not conform to POSIX standards.

## Lockahead

Lockahead provides the user space with new APIs that allow applications request locks on specific extents explicitly separated from I/O operations. The locks are not allowed to expand. In this way, if applications know their access patterns beforehand, they can avoid false lock conflicts by acquiring the locks exactly. Moreover, lock requests are sent asynchronously in parallel, so that the round-trip time in effect is equal to that requesting one lock. Obviously, modifications to application code are required to take the advantage of lockahead.

## Overstriping
Normally, Lustre will place the stripes alternately on each OST, resulting in one stripe per OST. Why do we limit that there can be only one stripe on each OST? Overstriping simply makes use of the flexibility of Lustre's layered design, allowing more than one stripes are stored on each OST. Compared to the methods above, overstriping does not require applications adapt to the new features. It can just reuse the existing tools like `lfs setstripe` and is as easy as to set the stripe count greater than the OST count for files. Implementing overstriping is also simple, which only involves in removing sanity checks in the Lustre code that prevents users from setting a stripe count greater than the OST count.

## References
[Lustre Lockahead: Early experience and performance using optimized locking](https://cug.org/proceedings/cug2017_proceedings/includes/files/pap141s2-file1.pdf)

[Exploring Lustre Overstriping For Shared File Performance on Disk and Flash](https://cug.org/proceedings/cug2019_proceedings/includes/files/pap136s2-file1.pdf)

[Shared File Performance Improvements in Lustre](https://wiki.lustre.org/images/f/f9/Shared-File-Performance-in-Lustre_Farrell.pdf)