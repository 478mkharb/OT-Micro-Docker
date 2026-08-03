# Appendix A - Complete API Reference

---

# Introduction

This appendix documents every REST API exposed by the OT-Micro-Docker platform.

Each endpoint includes:

- HTTP Method
- URL
- Description
- Request Body
- Response
- HTTP Status Codes
- Example Request
- Example Response

---

# Employee API

Base URL

```
http://localhost:8080
```

---

## Health Check

### Endpoint

```
GET /api/v1/employee/health
```

Purpose

Verify Employee API availability.

Response

```json
{
  "status":"UP"
}
```

Status Codes

| Code | Meaning |
|-------|----------|
|200|Healthy|

---

## Create Employee

```
POST /api/v1/employee
```

Request

```json
{
  "id":"EMP001",
  "name":"Mukesh",
  "email":"abc@gmail.com",
  "department":"IT"
}
```

Success

```
201 Created
```

---

## Get Employee

```
GET /api/v1/employee/{id}
```

---

## Update Employee

```
PUT /api/v1/employee/{id}
```

---

## Delete Employee

```
DELETE /api/v1/employee/{id}
```

---

# Attendance API

Base URL

```
http://localhost:8081
```

---

## Health

```
GET /api/v1/attendance/health
```

---

## Mark Attendance

```
POST /api/v1/attendance
```

---

## List Attendance

```
GET /api/v1/attendance
```

---

## Get Attendance By Employee

```
GET /api/v1/attendance/{id}
```

---

# Salary API

Base URL

```
http://localhost:8082
```

---

## Health

```
GET /actuator/health
```

---

## Create Salary

```
POST /salary
```

---

## Update Salary

```
PUT /salary/{id}
```

---

## Get Salary

```
GET /salary/{id}
```

---

# Notification API

Base URL

```
http://localhost:8085
```

---

## Health

```
GET /api/v1/notification/health
```

---

## Send Notification

```
POST /api/v1/notification/send/all
```

Purpose

Trigger notification processing.

---

# Swagger URLs

| Service | URL |
|----------|-----|
|Employee|http://localhost:8080/swagger/index.html|
|Attendance|http://localhost:8081/apidocs|
|Salary|http://localhost:8082/swagger-ui/index.html|
|Notification|http://localhost:8085/apidocs|
