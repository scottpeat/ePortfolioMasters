# Unit 9 – RESTful API Development Activity

## MSc Computer Science | University of Essex (Online)
### Module: Software Engineering Project Management

---

## Overview

This activity involved creating and interacting with a RESTful API using Python's Flask and Flask-RESTful libraries. The API manages user records and supports full CRUD operations: **Create (POST)**, **Read (GET)**, **Update (PUT)**, and **Delete (DELETE)**. Responses to each question are recorded below as part of my ePortfolio submission.

---

## The API Code (`api.py`)

The following code was used, sourced from [Codeburst](https://codeburst.io/this-is-how-easy-it-is-to-create-a-rest-api-8a25122ab1f3):

```python
from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

users = [
    {
        "name": "James",
        "age": 30,
        "occupation": "Network Engineer"
    },
    {
        "name": "Ann",
        "age": 32,
        "occupation": "Doctor"
    },
    {
        "name": "Jason",
        "age": 22,
        "occupation": "Web Developer"
    }
]

class User(Resource):
    def get(self, name):
        for user in users:
            if(name == user["name"]):
                return user, 200
        return "User not found", 404

    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        for user in users:
            if(name == user["name"]):
                return "User with name {} already exists".format(name), 400

        user = {
            "name": name,
            "age": args["age"],
            "occupation": args["occupation"]
        }
        users.append(user)
        return user, 201

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        for user in users:
            if(name == user["name"]):
                user["age"] = args["age"]
                user["occupation"] = args["occupation"]
                return user, 200

        user = {
            "name": name,
            "age": args["age"],
            "occupation": args["occupation"]
        }
        users.append(user)
        return user, 201

    def delete(self, name):
        global users
        users = [user for user in users if user["name"] != name]
        return "{} is deleted.".format(name), 200

api.add_resource(User, "/user/<string:name>")

app.run(debug=True)
```

---

## Question 1 – Running the API

**Question:** Run the `api.py` code. Take a screenshot of the terminal output. What command did you use to compile and run the code?

**Answer:**

The API was executed from the terminal using the following command:

```bash
python3 api.py
```

Python does not require a separate compilation step — it is an interpreted language, so this single command both interprets and runs the script.

**Expected terminal output:**

```
 * Serving Flask app 'api'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: XXX-XXX-XXX
```

Flask's built-in development server starts on `http://127.0.0.1:5000` (localhost, port 5000). The `debug=True` flag enables automatic reloading on code changes and provides an interactive debugger in the browser, which is useful during development but should **never** be used in production.

> 📸 *[Screenshot of terminal output to be inserted here]*

---

## Question 2 – Retrieving an Existing User (Ann)

**Question:** Run the following command at the terminal prompt: `w3m http://127.0.0.1:5000/user/Ann`. What happens when this command is run, and why?

**Answer:**

`w3m` is a text-based web browser that can be used from the terminal to make HTTP GET requests and render responses.

Running `w3m http://127.0.0.1:5000/user/Ann` sends a **GET** request to the `/user/Ann` endpoint of the running Flask API.

**What happens:**

The API's `get()` method is invoked with `name = "Ann"`. It iterates through the `users` list and finds a matching record. It returns the following JSON response with an HTTP **200 OK** status:

```json
{
    "name": "Ann",
    "age": 32,
    "occupation": "Doctor"
}
```

**Why:** Ann exists in the pre-populated `users` list, so the condition `if(name == user["name"])` evaluates to `True`, and her record is returned successfully. The `200` status code indicates a successful HTTP request.

> 📸 *[Screenshot of w3m terminal output to be inserted here]*

---

## Question 3 – Requesting a Non-Existent User (Adam)

**Question:** Run the following command at the terminal prompt: `w3m http://127.0.0.1:5000/user/Adam`. What happens when this command is run, and why?

**Answer:**

Running `w3m http://127.0.0.1:5000/user/Adam` sends a **GET** request to the `/user/Adam` endpoint.

**What happens:**

The API's `get()` method is invoked with `name = "Adam"`. It iterates through the entire `users` list and finds no match. It then returns:

```
"User not found"
```

with an HTTP **404 Not Found** status code.

**Why:** Adam does not exist in the `users` list. The loop exhausts all records without finding a name match, so the fallback `return "User not found", 404` is reached. The `404` status code is the standard HTTP response indicating that the requested resource could not be located on the server.

> 📸 *[Screenshot of w3m terminal output to be inserted here]*

---

## Question 4 – Capability Provided by the Flask Library

**Question:** What capability is achieved by the Flask library?

**Answer:**

**Flask** is a lightweight Python micro-framework for building web applications and APIs. In the context of this activity, it provides the following core capabilities:

| Capability | Description |
|---|---|
| **HTTP routing** | Maps URL patterns (e.g. `/user/<string:name>`) to Python functions or classes, enabling RESTful endpoint design. |
| **Request handling** | Parses incoming HTTP requests (GET, POST, PUT, DELETE) and makes request data (headers, body, query parameters) available within handler methods. |
| **Response construction** | Automatically serialises Python dictionaries to JSON responses, including appropriate HTTP status codes. |
| **Development server** | Provides a built-in WSGI development server (`app.run()`) so the API can be tested locally without additional infrastructure. |
| **Extensibility** | Acts as a foundation for extensions such as **Flask-RESTful** (used here), which adds the `Resource` class abstraction to map HTTP methods directly to class methods (`get`, `post`, `put`, `delete`). |

Together, Flask and Flask-RESTful provide a minimal but complete framework for building RESTful APIs that adhere to standard HTTP conventions and status codes (200, 201, 400, 404, etc.).

---

## Architecture Evolution Activity

### From Microservices to Contemporary Cloud-Native Architectures: An Extension of Salah et al. (2016)

---

#### Introduction

Salah et al. (2016) traced the evolution of software architecture from monolithic systems through Service-Oriented Architecture (SOA) to the then-emerging paradigm of microservices. This section extends that evolutionary narrative, examining the technologies and architectural patterns that have emerged since 2016 and which now represent the dominant paradigm in enterprise software engineering.

---

#### Phase 5: Microservices Maturation and Containerisation (2014–2018)

The microservices pattern, though conceptualised earlier, achieved widespread adoption between 2014 and 2018, driven primarily by the mainstreaming of **containerisation** technologies — most notably **Docker** (released 2013) and **Kubernetes** (released by Google in 2014, open-sourced in 2015).

Docker enabled developers to package microservices as portable, lightweight containers, resolving the "works on my machine" problem that had long complicated deployment. Kubernetes emerged as the de facto **container orchestration** platform, automating the deployment, scaling, and management of containerised applications across clusters of machines.

This period also saw the codification of key microservices best practices:
- **Domain-Driven Design (DDD)** informed service boundary definition (Evans, 2003; Newman, 2015).
- **The Twelve-Factor App** methodology provided guidelines for building scalable, maintainable services.
- **API gateways** (e.g. Kong, AWS API Gateway) emerged as a pattern to manage routing, authentication, and rate limiting at the service mesh boundary.

---

#### Phase 6: Serverless and Function-as-a-Service (2016–Present)

Parallel to microservices maturation, **serverless computing** emerged as an evolution that abstracted infrastructure management further. Platforms such as **AWS Lambda** (2014), **Google Cloud Functions** (2016), and **Azure Functions** (2016) enabled developers to deploy individual functions rather than services, with billing tied to execution time rather than reserved capacity.

This **Function-as-a-Service (FaaS)** model pushed the decomposition of applications to its logical extreme — individual operations as independently deployable, elastically scaling units — while eliminating operational overhead entirely for certain workloads.

However, serverless introduced its own challenges: cold start latency, vendor lock-in, and the difficulty of managing distributed state across ephemeral function instances.

---

#### Phase 7: Service Mesh and Cloud-Native Architecture (2018–Present)

As microservices deployments scaled to hundreds or thousands of services, inter-service communication, observability, and security became pressing concerns. The **service mesh** pattern — exemplified by **Istio** and **Linkerd** — addressed this by introducing a sidecar proxy (e.g. Envoy) alongside each service instance to handle traffic management, mutual TLS authentication, and telemetry collection transparently.

The **Cloud Native Computing Foundation (CNCF)** formalised this era's architecture under the banner of **cloud-native**, defined by four principles: containerisation, dynamic orchestration, microservices orientation, and continuous delivery. Tools such as **Prometheus** (monitoring), **Jaeger** (distributed tracing), and **Argo CD** (GitOps-based continuous deployment) became standard components of the cloud-native stack.

---

#### Phase 8: AI-Augmented and Event-Driven Architectures (2022–Present)

The most recent evolutionary phase has been shaped by two forces: the mainstreaming of **large language models (LLMs)** and the widespread adoption of **event-driven architecture (EDA)**.

**Event-driven architecture**, built on message brokers such as **Apache Kafka** and **AWS EventBridge**, decouples services through asynchronous event streams rather than synchronous REST calls. This improves resilience and scalability, particularly for high-throughput systems.

**AI-augmented architectures** represent the frontier: microservices increasingly incorporate LLM-powered components (e.g. via APIs such as OpenAI or Anthropic's Claude) for natural language processing, code generation, and intelligent routing. The emerging **agentic architecture** pattern — where AI agents autonomously invoke tools and APIs to complete multi-step tasks — represents a potential next phase, blurring the boundary between software services and autonomous AI systems.

---

#### Summary Table: Architectural Evolution Extended

| Phase | Period | Key Technologies | Primary Driver |
|---|---|---|---|
| Monolithic | Pre-2000 | Single deployable unit | Simplicity |
| SOA | 2000–2010 | SOAP, ESB, WSDL | Enterprise integration |
| REST & Web APIs | 2005–2015 | HTTP, JSON, REST | Web scalability |
| Microservices | 2012–2018 | Docker, Kubernetes, API Gateway | Deployment agility |
| Serverless / FaaS | 2016–present | AWS Lambda, Cloud Functions | Operational efficiency |
| Cloud-Native / Service Mesh | 2018–present | Istio, Envoy, CNCF stack | Operational scale |
| AI-Augmented / Event-Driven | 2022–present | Kafka, LLMs, Agentic APIs | Intelligence & resilience |

---

#### References

Evans, E. (2003) *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Addison-Wesley.

Fowler, M. and Lewis, J. (2014) *Microservices*. Available at: https://martinfowler.com/articles/microservices.html (Accessed: 20 June 2026).

Newman, S. (2015) *Building Microservices*. O'Reilly Media.

Salah, T., Zemerly, M.J., Yeun, C.Y., Al-Qutayri, M. and Al-Hammadi, Y. (2016) 'The evolution of distributed systems towards microservices architecture', *11th International Conference for Internet Technology and Secured Transactions (ICITST)*, pp. 318–325.

The Twelve-Factor App (2017) Available at: https://12factor.net (Accessed: 20 June 2026).

---

## Reflections

This activity provided practical exposure to REST API design using Flask, reinforcing theoretical knowledge from the module's reading on service-oriented and microservices architectures. Implementing the four HTTP verbs (GET, POST, PUT, DELETE) against a resource endpoint (`/user/<name>`) demonstrated how the RESTful constraint of **uniform interface** is applied in practice.

The architecture evolution extension activity consolidated understanding of how architectural paradigms have continued to shift since Salah et al.'s 2016 review — from containerisation and orchestration, through serverless, to the current frontier of AI-augmented and event-driven systems. These trends will directly inform the team's API design choices for the Unit 11 submission.

---

*ePortfolio entry prepared as part of MSc Computer Science, University of Essex Online.*
