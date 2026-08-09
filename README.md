# Distributed Web Infrastructure

## 1. Overview

This project describes a three-server web infrastructure that hosts the website `www.foobar.com`.

The infrastructure consists of:

* 1 HAProxy load balancer
* 2 application servers
* 2 Nginx web servers
* 2 application servers
* 2 copies of the application code base
* 2 MySQL database servers
* 1 MySQL Primary database
* 1 MySQL Replica database

The architecture is designed to improve availability, distribute traffic, and provide database redundancy.

## 2. Infrastructure Diagram

```text
                              Internet
                                  |
                                  |
                          www.foobar.com
                                  |
                                  v
                         +----------------+
                         |     HAProxy    |
                         | Load Balancer  |
                         +----------------+
                            /          \
                           /            \
                          v              v
                +----------------+  +----------------+
                |    Server 1    |  |    Server 2    |
                |                |  |                |
                |    Nginx       |  |    Nginx       |
                |       |        |  |       |        |
                |       v        |  |       v        |
                | Application    |  | Application    |
                |    Server      |  |    Server      |
                |       |        |  |       |        |
                |       v        |  |       v        |
                | Application    |  | Application    |
                |     Files      |  |     Files      |
                |       |        |  |       |        |
                |       v        |  |       v        |
                | MySQL Primary  |  | MySQL Replica  |
                +----------------+  +----------------+
                         \              /
                          \            /
                           \          /
                            \        /
                           Replication
```

## 3. Components

### HAProxy

HAProxy is used as a load balancer.

It receives incoming requests from users and distributes them between the two application servers.

This prevents a single application server from receiving all traffic and allows both servers to process requests.

HAProxy can also perform health checks and stop sending requests to a server that is unavailable.

### Nginx

Each server contains an Nginx web server.

Nginx receives HTTP requests from HAProxy and forwards requests to the application server.

It can also serve static files efficiently.

### Application Server

The application server runs the actual `foobar.com` application.

It contains the business logic and processes requests received from Nginx.

Both servers contain an instance of the application so that either server can process incoming requests.

### Application Files

The application files contain the source code required to run the website.

The application code is deployed on both servers so that both application servers can independently run the application.

### MySQL

MySQL is used as the relational database management system.

It provides persistent storage for application data such as users, places, reviews, and other application entities.

The database is configured using a Primary-Replica architecture.

---

# 4. Load Balancing

## Distribution Algorithm

HAProxy is configured to use the **Round Robin** algorithm.

Round Robin distributes requests sequentially between the available servers.

For example:

```text
Request 1 -> Server 1
Request 2 -> Server 2
Request 3 -> Server 1
Request 4 -> Server 2
Request 5 -> Server 1
Request 6 -> Server 2
```

This provides a relatively even distribution of traffic when both servers have similar resources and capabilities.

HAProxy can also use health checks to detect unavailable servers. If a server becomes unavailable, HAProxy stops sending traffic to it.

---

# 5. Active-Active Configuration

This infrastructure uses an **Active-Active** setup.

Both application servers are active and process requests at the same time.

```text
                    HAProxy
                    /     \
                   /       \
                  v         v
             Server 1    Server 2
              ACTIVE      ACTIVE
```

This allows the infrastructure to use the resources of both servers simultaneously.

## Active-Active vs Active-Passive

### Active-Active

In an Active-Active configuration, multiple servers are active at the same time and process traffic simultaneously.

Advantages:

* Better resource utilization
* Higher capacity
* Better scalability
* Traffic can continue if one server fails

### Active-Passive

In an Active-Passive configuration, one server handles traffic while another server waits as a standby.

```text
                    HAProxy
                       |
                       v
                  Server 1
                   ACTIVE
                       |
                       X
                  Server 2
                  PASSIVE
```

If the active server fails, the passive server can become active.

The main difference is that in Active-Active both servers process traffic, while in Active-Passive the backup server normally waits for a failure.

---

# 6. MySQL Primary-Replica Architecture

The database uses a **Primary-Replica** architecture.

```text
                    Application
                         |
                         v
                  MySQL Primary
                         |
                         | Replication
                         v
                  MySQL Replica
```

The Primary database is responsible for write operations.

The Replica receives changes from the Primary through replication and maintains a copy of the Primary's data.

For example:

```text
Application
     |
     | INSERT / UPDATE / DELETE
     v
MySQL Primary
     |
     | Replication
     v
MySQL Replica
```

The Replica can be used primarily for read operations:

```text
SELECT
```

This can help distribute database workload.

If the Primary fails, the Replica can potentially be promoted to become the new Primary, depending on the failover configuration.

---

# 7. Primary vs Replica

The Primary and Replica have different roles from the application's perspective.

## Primary

The Primary database handles write operations:

```text
INSERT
UPDATE
DELETE
```

The application sends changes to the Primary.

The Primary then replicates those changes to the Replica.

## Replica

The Replica maintains a copy of the Primary database.

It can primarily be used for read operations:

```text
SELECT
```

For example:

```text
                    Application
                   /           \
                  /             \
             WRITE             READ
                |                |
                v                v
          MySQL Primary    MySQL Replica
                |
                | Replication
                v
          MySQL Replica
```

The application must be configured correctly to send writes to the Primary and reads to the appropriate Replica.

---

# 8. Why These Components Are Added

| Component            | Purpose                                          |
| -------------------- | ------------------------------------------------ |
| HAProxy              | Distributes incoming traffic between servers     |
| Nginx                | Handles HTTP requests and serves static files    |
| Application Server   | Runs the application and business logic          |
| Application Files    | Contains the website source code                 |
| MySQL Primary        | Handles database writes                          |
| MySQL Replica        | Maintains a replicated copy and can handle reads |
| Database Replication | Keeps the Replica synchronized with the Primary  |

Each component has a specific role in making the infrastructure more scalable and reliable.

---

# 9. Single Points of Failure

Although this architecture provides redundancy for the application servers, it still contains possible **Single Points of Failure (SPOF)**.

## HAProxy

There is only one HAProxy server.

If HAProxy fails:

```text
Internet
   |
   X
HAProxy
```

Users cannot reach either application server.

A production environment should use multiple load balancers with a failover mechanism to eliminate this SPOF.

## MySQL Primary

The MySQL Primary can also become a SPOF for write operations.

If the Primary fails and there is no automatic failover mechanism, the application may no longer be able to perform database writes.

A production architecture should implement database failover and potentially multiple database nodes.

---

# 10. Security Issues

This infrastructure has several security weaknesses.

## No Firewall

There is no firewall configured in the infrastructure.

Without a firewall, unnecessary ports and services may be exposed to the network.

A firewall should restrict access to only the ports and services that are required.

For example, the MySQL database should not be directly accessible from the public Internet.

## No HTTPS

The infrastructure does not use HTTPS.

HTTP traffic is not encrypted, which can expose sensitive information during communication between the client and the infrastructure.

A production environment should use HTTPS with TLS certificates.

```text
Client
   |
 HTTPS
   |
   v
HAProxy
   |
   v
Nginx
   |
   v
Application Server
```

HTTPS provides encryption and helps protect sensitive information such as authentication credentials and user data.

---

# 11. No Monitoring

The infrastructure does not contain a monitoring system.

Without monitoring, it is difficult to detect problems such as:

* Server failures
* High CPU usage
* High memory usage
* Database failures
* Application errors
* Network problems
* High traffic
* Disk space problems

A production infrastructure should include monitoring and alerting.

Monitoring should track the health and performance of:

* HAProxy
* Nginx
* Application servers
* MySQL Primary
* MySQL Replica
* Network resources

Alerts should notify administrators when important services become unavailable or performance drops below acceptable levels.

---

# 12. Infrastructure Limitations

This infrastructure improves availability compared with a single-server architecture, but it is not completely fault tolerant.

The main limitations are:

1. HAProxy is a Single Point of Failure.
2. MySQL Primary can be a Single Point of Failure for writes.
3. There is no firewall.
4. HTTPS is not configured.
5. There is no monitoring system.
6. Database failover is not automatic.
7. The infrastructure does not provide complete redundancy for every component.

A more advanced production architecture would add redundant load balancers, automatic database failover, firewalls, HTTPS, monitoring, and alerting.

---

# 13. Conclusion

The proposed three-server infrastructure uses HAProxy to distribute traffic between two application servers.

Each application server contains Nginx, an application server, the application files, and a MySQL database node.

HAProxy uses the Round Robin algorithm to distribute traffic between the active servers, making the application layer Active-Active.

MySQL uses a Primary-Replica architecture where the Primary handles writes and replicates changes to the Replica. The Replica can primarily handle read operations and can potentially be promoted if the Primary fails.

However, the architecture still has several weaknesses, including the HAProxy Single Point of Failure, the MySQL Primary dependency for writes, the lack of a firewall, the lack of HTTPS, and the lack of monitoring.

These issues would need to be addressed before using this architecture as a fully production-ready infrastructure.
