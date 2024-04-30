syscall    dl_signal(
      sid32        sem        /* ID of semaphore to signal    */
    )
{
    intmask mask;            /* Saved interrupt mask        */
    struct    sentry *semptr;        /* Ptr to sempahore table entry    */

    mask = disable();
    if (isbadsem(sem)) {
        restore(mask);
        return SYSERR;
    }
    semptr= &semtab[sem];
    if (semptr->sstate == S_FREE) {
        restore(mask);
        return SYSERR;
    }
    if ((semptr->scount++) < 0) {    /* Release a waiting process */
        pid32 pid = dequeue(semptr->squeue);
        removeEdge(pid, sem+NPROC); process is no longer waiting on semaphore
        ready(pid);
    }
    else {
       removeEdge(sem+NPROC, getpid()); semaphore is no longer controlled by process
    }
    restore(mask);
    return OK;
}