---
title:  Lustre File Locks Improvements
author: Howard Lau
excerpt_separator: <!--more-->
---
Derived from VAX distributed lock manager, Lustre file system locks consist of six modes (NL, CR, CW, PR, PW, EX). The locks are organized in separate namespaces, e.g. metadata namespace and object namespace. Locks are requested when I/O operations are initiated. The locks are managed by different servers (OSS, MDS...) and are requested by clients (OSC, MDC...). However, Lustre performs poorly when multiple processes writing a single shared file in strides.  

<!--more-->
## Problems of Normal Write Locks

The write locks are automatically expanded by server when requested. For example, client A wants to write the 0, 3, 6 MB of a file and client B wants to write the 1, 4, 7 MB of the file. Although they are writing non overlapped intervals, there still exists a lock contention problem. To illustrate, when client A requests the write lock for 0-1 MB of the file, the server grants it the lock, expanded to the whole file. Later when client B requests the write lock for 1-2 MB of the file, the server cancels the lock granted to client A and grants client B the lock, also expanded to a whole file. This causes a false conflicting problem. Even worse, disabling lock expansion does not help due to the extra round-trip time incurred for more lock requests.

## Group Locking

Group locking enabled for a file requests Lustre not to acquire write locks. It is the application's responsibility to maintain consistency of the file since the file system is no longer providing the guarantees. This also means the reads and writes on the file do not conform to POSIX standards.

## Lockahead

Lockahead provides the user space with new APIs that allow applications request locks on specific extents explicitly separated from I/O operations. The locks are not allowed to expand. In this way, if applications know their access patterns beforehand, they can avoid false lock conflicts by acquiring the locks exactly. Moreover, lock requests are sent asynchronously in parallel, so that the round-trip time in effect is equal to that requesting one lock. 

## References

[Lustre Lockahead: Early experience and performance using optimized locking](https://cug.org/proceedings/cug2017_proceedings/includes/files/pap141s2-file1.pdf)

[Shared File Performance Improvements](https://wiki.lustre.org/images/f/f9/Shared-File-Performance-in-Lustre_Farrell.pdf)