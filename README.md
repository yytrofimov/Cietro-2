# CIERTO-2 - Flask + SqlAlchemy, NO API web app

## Stack

* Python Flask + gunicorn
* Custom validator on vanilla JS
* Python SQLAlchemy ORM + PostgreSQL
* Custom tokens generating (insted of JWS): Redis DB to store tokens
* (Bonus) Using of Poetry :)

## Description
The project was done as a homework assignment in the 2nd year of the Computer Science course at [Practicum](https://github.com/orgs/prakticum2k). The project was done as an *educational* one.

This project provides companies, for example, construction or repair companies, with convenient management of the use of their equipment. A certain company has equipment and employees who will use this equipment.
A company can start using the CIERTO-2 management completely remotely - either receive an invite code remotely after paying for services, or in the office. The company is registered using a personal invite code - it is tied to the company's identification number. The company is assigned an Administrator. Its basic capabilities are to remove and **add equipment**, **delete equipment**, as well as see **who is using what equipment at the moment**.
For now, regular workers can register themselves using a **company ID**. The basic capabilities of a worker are to see the company's **free equipment**, start using = **activate** the equipment through the **activation code** that is indicated on the equipment itself, and **deactivate** the equipment.


# ToDo
- **Gunicorn** as a WSGI server will be added
- **nginx** as a common HTTP server will be added
- Data in Redis DB in unstructured, so changes are on the way
- The task assumes the presence of an iOS application that performs the same function. Having two applications performing the same role allows communication with a common database. Now **all communication takes place in models**, but it will be moved to a separate **RESTFull API**.
- The structure will be redone using **Flask Blueprints**.
- A custom JS validator ( **forms** ) has been written on the user's side, but it will either be rewritten or replaced with third-party solutions, because the resulting solution was written in a hurry and turned out to be "crooked".
- Currently, there are only two user roles - Administrator and Worker. We need an implementation of the administrator of the entire site ( **Root user** ), with the ability to see and do absolutely everything, a **Support Worker**, with the ability to add companies, local company administrators.
- The implementation of **mailing** on behalf of the company will be placed in a separate API or in a subprocess, because now, according to the processing time of the password recovery link request, you can search for registered users' mails.
- **Frontend will be rewritten** in React / Angular / Vue .js. In current version: Error messages and success messages are placed in the **same danger class bootstrap div**, which is wrong and unusual for the user. **WAI-ARIA not respected :)**.
- The FlaskLogin extension is not usable, but the current authentication and authorization solution is a crutch. **Role-based authentication and authorization will be rewritten**.
- **An opportunity to buy Invitecode** will be added directly on the website.
- Communication with Redis inside models will be rewritten. Now all methods in model classes are public. When transferring logic to the API, **public interfaces will be written with authorization based on the role of the initiating user**.
